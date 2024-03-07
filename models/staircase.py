""" Adaptive staircase class for psychophysical experiments.

    Written by: Travis M. Moore
    Modeled after StairHandler from PsychoPy
    Created: June 06, 2023
    Last edited: December 21, 2023
"""

###########
# Imports #
###########
# Import data science packages
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})


###################
# Staircase Class #
###################
class Staircase:
    def __init__(self, start_val, step_sizes, nUp, nDown, nTrials,
                 nReversals, rapid_descend, min_val, max_val):

        # Assign arguments to attributes
        self.current_level= start_val
        self.step_sizes = step_sizes
        self.up_arg = nUp
        self.down_arg = nDown
        self.nTrials = nTrials
        self.nReversals = nReversals
        self.rapid_descend = rapid_descend
        self.min_val = min_val
        self.max_val = max_val

        # Assign up/down rule based on rapid_descend
        if rapid_descend:
            self.nUp = 1
            self.nDown = 1
        else:
            self.nUp = self.up_arg
            self.nDown = self.down_arg

        # Make sure there are sufficient number of reversals
        # to run through the list of step sizes
        if self.nReversals < len(self.step_sizes):
            msg = f"The number of reversals must be equal to or greater "\
                f"than the number of step sizes.\nFound {len(step_sizes)} "\
                f"step sizes, but {nReversals} reversal(s)."
            print(msg)
            raise ValueError(msg)

        # Additional attributes
        self.scores = []
        self._level_tracker = []
        self._step_index = 0
        self._trial_num = 0
        self._n_back = self.nDown + 1
        self.status = True # True for go, and False for stop

        # Create DataWrangler to hold data points
        self.dw = DataWrangler()


    def add_data_point(self, response):
        """ Instantiate a new DataPoint using the DataWrangler.
            Update variables with available trial data.
        """
        # Instantiate new data point object
        dp = self.dw.new_data_point()

        # Update variables
        dp.trial_number = self._trial_num
        dp.level = self.current_level
        dp.response = response

        return dp


    def _handle_response(self, response):
        """ Score and log response and level tracker."""
        # Score response
        if response == 1:
            print("staircase: Correct")
            # Log response
            self.scores.append(1)
            # Update level tracker
            self._level_tracker.append(1)
        elif response == -1:
            # Log response
            self.scores.append(-1)
            # Update level tracker
            self._level_tracker.append(-1)
            print("staircase: Incorrect")
        else:
            print("staircase: Invalid response!")


    def _calc_reversals(self):
        """ Determine whether a reversal has occurred."""
        # Create variables
        correct_vals = np.ones(self.nDown)
        reversal_1 = np.append(correct_vals, -1)
        reversal_2 = np.insert(correct_vals, 0, -1)

        # Check for reversals
        if np.array_equal(self.scores[-self._n_back:], reversal_1) or \
        np.array_equal(self.scores[-self._n_back:], reversal_2):
            return True
        else:
            return False


    def _calc_next_step_size(self):
        """ Determine the next step size to use based on the number
            of reversals. If _step_sizes is a list, a new value will 
            be selected on each reversal. 
        """
        # Grab the step_sizes value where index == number of reversals
        self._step_index = len(self.dw._get_reversals())

        # Use last step_sizes value if the number of reversals exceed
        # the number of available step sizes
        if self._step_index >= len(self.step_sizes):
            self._step_index = len(self.step_sizes) - 1


    def _calc_level(self):
        """ Calculate the next presentation level based on previous 
            performance.
        """
        # Must use np.array_equal(A,B) to test for shape and elements
        # Using any()/all() results in weird behavior with different 
        # length arrays and/or empty arrays
        print(f"level tracker: {self._level_tracker}")
        print(f"nDown: {np.ones(self.nDown)}")
        if np.array_equal(self._level_tracker, np.ones(self.nDown)):
            self.current_level -= self.step_sizes[self._step_index]
            self._level_tracker = []
        elif -1 in self._level_tracker:
            self.current_level += self.step_sizes[self._step_index]
            self._level_tracker = []

        # Make sure levels stay within the provided limits
        if self.current_level > self.max_val:
            self.current_level = self.max_val
        elif self.current_level < self.min_val:
            self.current_level = self.min_val


    def _increase_trial_num(self):
        """ Increase the trial counter by 1."""
        self._trial_num += 1


    def _check_up_down_rule(self):
        """ Update up/down values to those provided after
            first reversal, if rapid_descend == True.
        """
        # Provide feedback to console
        revs = self.dw._get_reversals()
        print(f"staircase: Total # of reversals: {len(revs)}")

        # Update up/down rule after first reversal
        if self.rapid_descend:
            if len(revs) >= 1:
                self.nUp = self.up_arg
                self.nDown = self.down_arg
                self._n_back = self.nDown + 1


    def _check_for_end_of_staircase(self):
        """ Check whether the minimum number of trials and reversals
            has been met. If yes, end task.
        """
        # Trial stopping rule reached?
        if self._trial_num >= self.nTrials:
            # Reversal stopping rule reached?
            if len(self.dw._get_reversals()) >= self.nReversals:
                self.status = False
                print(f"\n\nstaircase: Task complete!\n")


    def add_response(self, response):
        """ Log current level. 
            Score and log response and level tracker.
            Check for reversals.
            Calculate next level.
            Increase trial counter.
        """
        # Begin feedback to console
        print(f"\nstaircase: Trial number: {self._trial_num}")

        # Instantiate new DataPoint via the DataWrangler
        dp = self.add_data_point(response)

        # Score and log response
        self._handle_response(response)

        # Check for reversal
        dp.reversal = self._calc_reversals()

        # Calculate next step size: must precede _calc_level!!
        self._calc_next_step_size()

        # Calculate next level: must follow _calc_next_step_size!!
        self._calc_level()

        # Display DataPoint trial parameters
        print(f"staircase: {dp.__dict__}")

        # Check that up/down values update after rapid descend
        if self.rapid_descend:
            self._check_up_down_rule()

        # Check for end of staircase 
        self._check_for_end_of_staircase()

        # Increase trial counter - must come last!!
        self._increase_trial_num()


    ############
    # Plotting #
    ############
    def _make_attribute_list(self, data_points, attr):
        """ Iterate through the provided list of data_points 
            and create lists of the specified value.
        """
        attr_list = []
        for obj in data_points:
            output = getattr(obj, attr)
            attr_list.append(output)
        
        return attr_list


    def plot_data(self):
        """ Organize data by response type and reversal.
            Plot color-coded data and return average of
            last n reversals.
        """
        # ALL DATA
        x_all = self._make_attribute_list(self.dw.datapoints, 'trial_number')
        y_all = self._make_attribute_list(self.dw.datapoints, 'level')
        plt.plot(x_all, y_all, color='k', linestyle='dashed')

        # CORRECT RESPONSES
        correct = self.dw._get_correct()
        x_correct = self._make_attribute_list(correct, 'trial_number')
        y_correct = self._make_attribute_list(correct, 'level')
        plt.plot(x_correct, y_correct, color="green", linestyle="none", 
                 marker='o', label="Correct")

        # INCORRECT RESPONSES
        incorrect = self.dw._get_incorrect()
        x_incorrect = self._make_attribute_list(incorrect, 'trial_number')
        y_incorrect = self._make_attribute_list(incorrect, 'level')
        plt.plot(x_incorrect, y_incorrect, color='red', linestyle='none',
                 marker='o', label="Incorrect")

        # REVERSALS
        reversals = self.dw._get_reversals()
        x_rev = self._make_attribute_list(reversals, 'trial_number')
        y_rev = self._make_attribute_list(reversals, 'level')
        plt.plot(x_rev, y_rev, marker='o', ms=15, markeredgewidth=3, 
                 linestyle='none', color='k', fillstyle='none', 
                 label="Reversal")

        # Plot labels
        plt.xlabel("Trial Number")
        plt.ylabel("Level (dB SPL)")
        plt.title(f"Average of last {len(reversals)-1} reversals: " +
                  f"{np.round(np.mean(y_rev[-(len(reversals)-1):]), 2)}")
        plt.legend()
        plt.show()
        plt.close()


######################
# Data Point Classes #
######################
class DataPoint:
    """ Individual object containing all data for a given trial.
        Works with DataWrangler class.
    """
    def __init__(self):
        self.trial_number = None
        self.level = None
        self.response = None
        self.reversal = None


class DataWrangler:
    """ Represent a collection of data points that can be searched."""
    def __init__(self):
        """Initialize a DataWrangler with an empty list."""
        self.datapoints = []


    def new_data_point(self):
        """ Create new DataPoint object and append to list."""
        dp = DataPoint()
        self.datapoints.append(dp)
        return dp


    def _get_correct(self):
        """ Return a list of all DataPoint objects with a correct response."""
        return [datum for datum in self.datapoints if datum.response == 1]


    def _get_incorrect(self):
        """ Return a list of all DataPoint objects with an incorrect 
            response.
        """
        return [datum for datum in self.datapoints if datum.response == -1]


    def _get_reversals(self):
        """ Find all data points that match the given filter."""
        return [datum for datum in self.datapoints if datum.reversal]
