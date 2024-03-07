""" Unit tests for Staircase class. 

    Written by: Travis M. Moore
    Created: December 13, 2023
    Last edited: December 21, 2023
"""

###########
# Imports #
###########
# Import testing packages
from unittest import TestCase
from unittest import mock

# Import custom modules
from models import staircase


###################
# STAIRCASE TESTS #
###################
class TestStaircase(TestCase):
    def setUp(self):
        """ Create Staircase.
        """
        # Create staircase
        self.s = staircase.Staircase(
            start_val=60,
            step_sizes=[8,4],
            nUp=1,
            nDown=2,
            nTrials=10,
            nReversals=2,
            rapid_descend=False,
            min_val=50,
            max_val=80
        )

        self.s_rapid = staircase.Staircase(
            start_val=60,
            step_sizes=[2,1],
            nUp=1,
            nDown=2,
            nTrials=10,
            nReversals=2,
            rapid_descend=True,
            min_val=50,
            max_val=80
        )


    def tearDown(self):
        del self.s
        del self.s_rapid


    ########################
    # INITIALIZATION TESTS #
    ########################
    def test_staircase_parameters_on_init(self):
        """ Test that arguments are assigned correctly.
        """
        # Assertions
        self.assertEqual(self.s.current_level, 60)
        self.assertEqual(self.s.step_sizes, [8,4])
        self.assertEqual(self.s.nUp, 1)
        self.assertEqual(self.s.nDown, 2)
        self.assertEqual(self.s.nTrials, 10)
        self.assertEqual(self.s.nReversals, 2)
        self.assertEqual(self.s.rapid_descend, False)
        self.assertEqual(self.s.min_val, 50)
        self.assertEqual(self.s.max_val, 80)


    def test_staircase_default_attributes_on_init(self):
        """ Test that public attribute defaults are correct.
        """
        # Assertions
        self.assertEqual(self.s.scores, [])
        self.assertEqual(self.s._level_tracker, [])
        self.assertEqual(self.s._step_index, 0)
        self.assertEqual(self.s._trial_num, 0)
        self.assertEqual(self.s._n_back, 3)


    def test_staircase_init_too_few_reversals(self):
        """ Raise ValueError if nReversals is less than
            the number of provided steps.
        """
        # Assertions
        with self.assertRaises(ValueError):
            # Create staircase
            s = staircase.Staircase(
                start_val=60,
                step_sizes=[8,8,4,4],
                nUp=1,
                nDown=2,
                nTrials=10,
                nReversals=2,
                rapid_descend=True,
                min_val=50,
                max_val=80
            )


    def test_staircase_init_too_few_reversals(self):
        """ Raise ValueError if nReversals is less than
            the number of provided steps.
        """
        with self.assertRaises(ValueError):
            # Create staircase
            s = staircase.Staircase(
                start_val=60,
                step_sizes=[8,8,4,4],
                nUp=1,
                nDown=2,
                nTrials=10,
                nReversals=2,
                rapid_descend=True,
                min_val=50,
                max_val=80
            )


    def test_staircase_init_rapid_descend_true(self):
        """ Up/down rule should default to 1/1 when rapid_descend
            is True.
        """
        # Assertions
        self.assertEqual(self.s_rapid.nUp, 1)
        self.assertEqual(self.s_rapid.nDown, 1)


    #################
    # RAPID DESCEND #
    #################
    @mock.patch('models.staircase.DataWrangler._get_reversals')
    def test__check_up_down_rule_no_reversals(self, mock_reversals):
        """ Check that up/down/nBack values == 1/1/2 """
        # Force number of reversals to 0
        mock_reversals.return_value = []

        # Call function
        self.s_rapid._check_up_down_rule()

        # Assertions
        self.assertEqual(self.s_rapid.nUp, 1)
        self.assertEqual(self.s_rapid.nDown, 1)
        self.assertEqual(self.s_rapid._n_back, 2)


    @mock.patch('models.staircase.DataWrangler._get_reversals')
    def test__check_up_down_rule_one_reversal(self, mock_reversals):
        """ Check that up/down/nBack values == 1/2/3 """
        # Force number of reversals to 1
        mock_reversals.return_value = [1]

        # Call function
        self.s_rapid._check_up_down_rule()

        # Assertions
        self.assertEqual(self.s_rapid.nUp, 1)
        self.assertEqual(self.s_rapid.nDown, 2)
        self.assertEqual(self.s_rapid._n_back, 3)


    @mock.patch('models.staircase.DataWrangler._get_reversals')
    def test__check_up_down_rule_two_reversals(self, mock_reversals):
        """ Check that up/down/nBack values == 1/2/3 """
        # Force number of reversals to 2
        mock_reversals.return_value = [1, 1]

        # Call function
        self.s_rapid._check_up_down_rule()

        # Assertions
        self.assertEqual(self.s_rapid.nUp, 1)
        self.assertEqual(self.s_rapid.nDown, 2)
        self.assertEqual(self.s_rapid._n_back, 3)


    def test_rapid_descend_no_reversal_one_correct(self):
        # Add one correct reponse
        self.s_rapid.add_response(1)
        
        # Assertions
        self.assertEqual(self.s_rapid.nUp, 1)
        self.assertEqual(self.s_rapid.nDown, 1)
        self.assertEqual(self.s_rapid.current_level, 58)


    def test_rapid_descend_no_reversal_two_correct(self):
        # Add two correct reponses
        responses = [1, 1]
        for response in responses:
            self.s_rapid.add_response(response)
        
        # Assertions
        self.assertEqual(self.s_rapid.nUp, 1)
        self.assertEqual(self.s_rapid.nDown, 1)
        self.assertEqual(self.s_rapid.current_level, 56)


    def test_rapid_descend_no_reversal_one_incorrect(self):
        # Add one incorrect reponse
        responses = [-1]
        for response in responses:
            self.s_rapid.add_response(response)
        
        # Assertions
        self.assertEqual(self.s_rapid.nUp, 1)
        self.assertEqual(self.s_rapid.nDown, 1)
        self.assertEqual(self.s_rapid.current_level, 62)


    def test_rapid_descend_no_reversal_two_incorrect(self):
        # Add two incorrect reponses
        responses = [-1, -1]
        for response in responses:
            self.s_rapid.add_response(response)
        
        # Assertions
        self.assertEqual(self.s_rapid.nUp, 1)
        self.assertEqual(self.s_rapid.nDown, 1)
        self.assertEqual(self.s_rapid.current_level, 64)


    def test_rapid_descend_one_reversal(self):
        # Cause one reversal
        responses = [1, 1, 1, 1, -1]
        for response in responses:
            self.s_rapid.add_response(response)

        # Assertions
        self.assertEqual(self.s_rapid.nUp, 1)
        self.assertEqual(self.s_rapid.nDown, 2)
        self.assertEqual(self.s_rapid.current_level, 53)


    def test_rapid_descend_two_reversals(self):
        # Cause two reversals
        responses = [1, 1, -1, 1, 1, -1]
        for response in responses:
            self.s_rapid.add_response(response)
        
        # Assertions
        self.assertEqual(self.s_rapid.nUp, 1)
        self.assertEqual(self.s_rapid.nDown, 2)
        self.assertEqual(self.s_rapid.current_level, 57)


    ###########
    # SCORING #
    ###########
    def test__handle_response_one_correct(self):
        # Add response to staircase
        response = 1
        self.s._handle_response(response)

        # Assertions
        self.assertEqual(self.s.scores, [1])
        self.assertEqual(self.s._level_tracker, [1])


    def test__handle_response_two_correct(self):
        # Add two correct responses to staircase
        responses = [1, 1]
        for response in responses:
            self.s._handle_response(response)

        # Assertions
        self.assertEqual(self.s.scores, [1, 1])
        self.assertEqual(self.s._level_tracker, [1, 1])


    def test__handle_response_one_incorrect(self):
        # Add response to staircase
        response = -1
        self.s._handle_response(response)

        # Assertions
        self.assertEqual(self.s.scores, [-1])
        self.assertEqual(self.s._level_tracker, [-1])


    def test__handle_response_two_incorrect(self):
        # Add two incorrect responses to staircase
        responses = [-1, -1]
        for response in responses:
            self.s._handle_response(response)

        # Assertions
        self.assertEqual(self.s.scores, [-1, -1])
        self.assertEqual(self.s._level_tracker, [-1, -1])


    #############
    # REVERSALS #
    #############
    def test__calc_reversals_yes_1(self):
        # Update scores attribute
        self.s.scores = [1, 1, -1]
        output = self.s._calc_reversals()

        # Assertions
        self.assertEqual(output, True)


    def test__calc_reversals_yes_2(self):
        # Update scores attribute
        self.s.scores = [-1, 1, 1]
        output = self.s._calc_reversals()

        # Assertions
        self.assertEqual(output, True)


    def test__calc_reversals_all_correct(self):
        # Update scores attribute
        self.s.scores = [1, 1, 1]
        output = self.s._calc_reversals()

        # Assertions
        self.assertEqual(output, False)


    def test__calc_reversals_all_incorrect(self):
        # Update scores attribute
        self.s.scores = [-1, -1, -1]
        output = self.s._calc_reversals()

        # Assertions
        self.assertEqual(output, False)


    def test__calc_reversals_no_1(self):
        # Update scores attribute
        self.s.scores = [-1, 1, -1]
        output = self.s._calc_reversals()

        # Assertions
        self.assertEqual(output, False)


    def test__calc_reversals_no_2(self):
        # Update scores attribute
        self.s.scores = [1, -1, 1]
        output = self.s._calc_reversals()

        # Assertions
        self.assertEqual(output, False)


    #######################
    # calc_next_step_size #
    #######################
    @mock.patch('models.staircase.DataWrangler._get_reversals')
    def test__calc_next_step_size_no_reversals(self, mock_reversals):
         # Force no reversals
         mock_reversals.return_value = []

        # Calculate next step size
         self.s._calc_next_step_size()

         # Assertions
         self.assertEqual(self.s._step_index, 0)


    @mock.patch('models.staircase.DataWrangler._get_reversals')
    def test__calc_next_step_size_one_reversal(self, mock_reversals):
         # Force one reversal
         mock_reversals.return_value = [1]

        # Calculate next step size
         self.s._calc_next_step_size()

         # Assertions
         self.assertEqual(self.s._step_index, 1)


    @mock.patch('models.staircase.DataWrangler._get_reversals')
    def test__calc_next_step_size_two_reversals(self, mock_reversals):
         # Force two reversals
         mock_reversals.return_value = [1, 1]

        # Calculate next step size
         self.s._calc_next_step_size()

         # Assertions
         # Typically the _step_index should equal the number of 
         # reversals, but since there are only two values in 
         # step_sizes, the last legal index value is repeated
         self.assertEqual(self.s._step_index, 1)


    #################
    # LEVEL SETTING #
    #################
    def test__calc_level_incorrect_1(self):
        # Update level tracker
        self.s._level_tracker = [-1]
        self.s._calc_level()

        # Assertions
        self.assertEqual(self.s.current_level, 68)


    def test__calc_level_incorrect_2(self):
        # Update level tracker
        self.s._level_tracker = [1, -1]
        self.s._calc_level()

        # Assertions
        self.assertEqual(self.s.current_level, 68)


    def test__calc_level_correct_1(self):
        # Update level tracker
        self.s._level_tracker = [1]
        self.s._calc_level()

        # Assertions
        self.assertEqual(self.s.current_level, 60)


    def test__calc_level_correct_2(self):
        # Update level tracker
        self.s._level_tracker = [1, 1]
        self.s._calc_level()

        # Assertions
        self.assertEqual(self.s.current_level, 52)


    def test__calc_level_over_max(self):
        # Update level tracker
        self.s._level_tracker = [-1]

        # Update current level
        self.s.current_level = 78

        self.s._calc_level()

        # Assertions
        self.assertEqual(self.s.current_level, 80)


    def test__calc_level_under_min(self):
        # Update level tracker
        self.s._level_tracker = [1, 1]

        # Update current level
        self.s.current_level = 51

        self.s._calc_level()

        # Assertions
        self.assertEqual(self.s.current_level, 50)


    ########
    # MISC #
    ########
    def test_increase_trial_num_once(self):
        # Increase trial number one time
        self.s._increase_trial_num()

        # Assertions
        self.assertEqual(self.s._trial_num, 1)


    def test_increase_trial_num_twice(self):
        # Increase trial number one time
        self.s._increase_trial_num()
        self.s._increase_trial_num()

        # Assertions
        self.assertEqual(self.s._trial_num, 2)


    @mock.patch('models.staircase.DataWrangler._get_reversals')
    def test__check_for_end_of_staircase_trials_pass(self, mock_reversals):
        # No reversals
        mock_reversals.return_value = []

        # Trials stopping rule met
        self.s._trial_num = 100

        self.s._check_for_end_of_staircase()

        self.assertEqual(self.s.status, True)


    @mock.patch('models.staircase.DataWrangler._get_reversals')
    def test__check_for_end_of_staircase_reversals_pass(self, mock_reversals):
        # Reversal stopping rule met
        mock_reversals.return_value = [1,1,1,1]

        # Trials do not meet rule
        self.s._trial_num = 1

        self.s._check_for_end_of_staircase()

        self.assertEqual(self.s.status, True)


    @mock.patch('models.staircase.DataWrangler._get_reversals')
    def test__check_for_end_of_staircase_neither_pass(self, mock_reversals):
        # Reversal do not meet rule
        mock_reversals.return_value = [1]

        # Trials do not meet rule
        self.s._trial_num = 1

        self.s._check_for_end_of_staircase()

        self.assertEqual(self.s.status, True)


    @mock.patch('models.staircase.DataWrangler._get_reversals')
    def test__check_for_end_of_staircase_both_pass(self, mock_reversals):
        # Reversal do not meet rule
        mock_reversals.return_value = [1, 1, 1, 1]

        # Trials do not meet rule
        self.s._trial_num = 100

        self.s._check_for_end_of_staircase()

        self.assertEqual(self.s.status, False)


    #####################
    # Integration Tests #
    #####################
    def test_add_response_one_correct(self):
        # Add one correct response to staircase
        response = 1
        self.s.add_response(response)

        # Assertions
        self.assertEqual(self.s.current_level, 60)
        self.assertEqual(self.s.scores, [1])
        self.assertEqual(self.s._level_tracker, [1])


    def test_add_response_two_correct(self):
        # Add two correct responses
        responses = [1, 1]
        for response in responses:
            self.s.add_response(response)
        
        # Assertions
        self.assertEqual(self.s.current_level, 52)
        self.assertEqual(self.s.scores, [1, 1])

        # _level_tracker should reset after two correct responses
        self.assertEqual(self.s._level_tracker, [])

        # The current_level should be updated based on the step_sizes
        self.assertEqual(self.s.current_level, 52)

        # No reversals should have occurred
        self.assertEqual(len(self.s.dw._get_reversals()), 0)


    def test_add_response_three_correct(self):
        # Add three correct responses
        responses = [1, 1, 1]
        for response in responses:
            self.s.add_response(response)
        
        # Assertions
        self.assertEqual(self.s.scores, [1, 1, 1])

        # _level_tracker should reset after two correct responses
        self.assertEqual(self.s._level_tracker, [1])

        # The current_level should be updated based on the step_sizes
        self.assertEqual(self.s.current_level, 52)

        # No reversals should have occurred
        self.assertEqual(len(self.s.dw._get_reversals()), 0)


    def test_add_response_one_incorrect(self):
        # Add one incorrect response to staircase
        response = -1
        self.s.add_response(response)

        # Assertions
        # Current level
        self.assertEqual(self.s.current_level, 68)

        # List of scores
        self.assertEqual(self.s.scores, [-1])

        # _level_tracker should reset after one incorrect response
        self.assertEqual(self.s._level_tracker, [])

        # No reversals should have occurred
        self.assertEqual(len(self.s.dw._get_reversals()), 0)


    def test_add_response_two_incorrect(self):
        # Add two incorrect responses
        responses = [-1, -1]
        for response in responses:
            self.s.add_response(response)

        levels = [obj.level for obj in self.s.dw.datapoints]
        
        # Assertions
        self.assertEqual(levels, [60, 68])
        self.assertEqual(self.s.scores, [-1, -1])

        # _level_tracker should reset after one incorrect response
        self.assertEqual(self.s._level_tracker, [])

        # The next level should be updated based on the step_sizes
        self.assertEqual(self.s.current_level, 76)

        # No reversals should have occurred
        self.assertEqual(len(self.s.dw._get_reversals()), 0)


    def test_correct_incorrect_reversal(self):
        # Add two correct responses and one incorrect response
        responses = [1, 1, -1]
        for response in responses:
            self.s.add_response(response)
        
        levels = [obj.level for obj in self.s.dw.datapoints]

        # Assertions
        self.assertEqual(levels, [60, 60, 52])
        self.assertEqual(self.s.scores, [1, 1, -1])

        # _level_tracker should reset after one incorrect response
        self.assertEqual(self.s._level_tracker, [])

        # The  next current_level should be updated based on the step_sizes
        self.assertEqual(self.s.current_level, 56)

        # One reversal should have occurred
        self.assertEqual(len(self.s.dw._get_reversals()), 1)


    def test_incorrect_correct_reversal(self):
        # Add one incorrect response and two correct responses
        responses = [-1, 1, 1]
        for response in responses:
            self.s.add_response(response)
        
        # Get levels from each DataPoint
        levels = [obj.level for obj in self.s.dw.datapoints]
        
        # Assertions
        self.assertEqual(levels, [60, 68, 68])
        self.assertEqual(self.s.scores, [-1, 1, 1])

        # _level_tracker should reset after two correct responses
        self.assertEqual(self.s._level_tracker, [])

        # The next current_level should be updated based on the step_sizes
        self.assertEqual(self.s.current_level, 64)

        # One reversal should have occurred
        self.assertEqual(len(self.s.dw._get_reversals()), 1)


    def test_incorrect_correct_no_reversal(self):
        # Add one incorrect response and one correct response
        responses = [-1, 1]
        for response in responses:
            self.s.add_response(response)
        
        # Get levels from each DataPoint
        levels = [obj.level for obj in self.s.dw.datapoints]
        
        # Assertions
        self.assertEqual(levels, [60, 68])
        self.assertEqual(self.s.scores, [-1, 1])

        # _level_tracker should reset after two correct responses
        self.assertEqual(self.s._level_tracker, [1])

        # The next current_level should be updated based on the step_sizes
        self.assertEqual(self.s.current_level, 68)

        # No reversals should have occurred
        self.assertEqual(len(self.s.dw._get_reversals()), 0)


    def test_correct_incorrect_no_reversal(self):
        # Add one correct response and one incorrect response
        responses = [1, -1]
        for response in responses:
            self.s.add_response(response)

        # Get levels from each DataPoint
        levels = [obj.level for obj in self.s.dw.datapoints]

        # Assertions
        self.assertEqual(levels, [60, 60])
        self.assertEqual(self.s.scores, [1, -1])

        # _level_tracker should reset after two correct responses
        self.assertEqual(self.s._level_tracker, [])

        # The next current_level should be updated based on the step_sizes
        self.assertEqual(self.s.current_level, 68)

        # No reversals should have occurred
        self.assertEqual(len(self.s.dw._get_reversals()), 0)


###################
# DATAPOINT TESTS #
###################
class TestDataPoint(TestCase):
    def setUp(self):
        pass


    def tearDown(self):
        pass


    ########################
    # INITIALIZATION TESTS #
    ########################
    def test_datapoint_class_init(self):
        # Create a DataPoint object
        dp = staircase.DataPoint()

        # Assertions
        self.assertEqual(dp.trial_number, None)
        self.assertEqual(dp.level, None)
        self.assertEqual(dp.response, None)
        self.assertEqual(dp.reversal, None)

    """ 
        Test the values of the DataPoint attributes after calling
        add_data_point. This requires creating a staircase to 
        populate _trial_num, current_level and response, as well
        as a DataWrangler.
    """


######################
# DATAWRANGLER TESTS #
######################
class TestDataWrangler(TestCase):
    def setUp(self):
        # Create empty DataWrangler
        self.dw = staircase.DataWrangler()
        # Create filled DataWrangler
        self.dw_full = staircase.DataWrangler()

        # Create DataPoints and add response and reversals
        trials = [0, 1, 2, 3, 4, 5, 6]
        levels = [80, 80, 76, 76, 72, 72, 76]
        scores = [1, 1, -1, 1, -1, 1, 1]
        reversals = [False, False, True, False, False, True, False]
        for ii, score in enumerate(scores):
            self.dw_full.new_data_point()
            self.dw_full.datapoints[ii].trial_number = trials[ii]
            self.dw_full.datapoints[ii].level = levels[ii]
            self.dw_full.datapoints[ii].response = score
            self.dw_full.datapoints[ii].reversal = reversals[ii]

        # Create staircase to access _make_attribute_list function
        self.dwt_stair = staircase.Staircase(
            start_val=60,
            step_sizes=[8,4],
            nUp=1,
            nDown=2,
            nTrials=10,
            nReversals=2,
            rapid_descend=True,
            min_val=50,
            max_val=80
        )


    def tearDown(self):
        del self.dw
        del self.dw_full


    def test_DataWrangler_on_init(self):
        """ Test datapoints list is empty on intitialization."""
        self.assertEqual(len(self.dw.datapoints), 0)


    def test_new_data_point_one_point(self):
        # Create one new DataPoint
        self.dw.new_data_point()

        # Assertions
        self.assertEqual(len(self.dw.datapoints), 1)


    def test_new_data_point_two_points(self):
        # Create one new DataPoint
        self.dw.new_data_point()
        self.dw.new_data_point()

        # Assertions
        self.assertEqual(len(self.dw.datapoints), 2)


    def test__get_correct(self):
        # Call get_correct function
        correct_responses = self.dw_full._get_correct()

        # Assertions
        # Seven DataPoints were added
        self.assertEqual(len(self.dw_full.datapoints), 7)

        # Five DataPoints were correct
        self.assertEqual(len(correct_responses), 5)


    def test__get_incorrect(self):
        # Call get_incorrect function
        incorrect_responses = self.dw_full._get_incorrect()

        # Assertions
        # Seven DataPoints were added
        self.assertEqual(len(self.dw_full.datapoints), 7)

        # Five DataPoints were incorrect
        self.assertEqual(len(incorrect_responses), 2)


    def test__get_reversals(self):
        # Call get_correct function
        reversals = self.dw_full._get_reversals()

        # Assertions
        # Seven DataPoints were added
        self.assertEqual(len(self.dw_full.datapoints), 7)

        # Two reversals
        self.assertEqual(len(reversals), 2)


    #######################
    # make_attribute_list #
    #######################
    def test__make_attribute_list_trial_nums(self):
        # Get list of trial numbers
        all_trials = self.dwt_stair._make_attribute_list(
            self.dw_full.datapoints, 'trial_number')

        # Assertions
        self.assertEqual(all_trials, [0,1,2,3,4,5,6])


    def test__make_attribute_list_levels(self):
        # Get list of levels
        all_levels = self.dwt_stair._make_attribute_list(
            self.dw_full.datapoints, 'level')

        self.assertEqual(all_levels, [80, 80, 76, 76, 72, 72, 76])


    def test__make_attribute_list_responses(self):
        # Get list of responses
        all_responses = self.dwt_stair._make_attribute_list(
            self.dw_full.datapoints, 'response')

        self.assertEqual(all_responses, [1, 1, -1, 1, -1, 1, 1])


    def test__make_attribute_list_reversals(self):
        # Get list of reversals
        all_reversals = self.dwt_stair._make_attribute_list(
            self.dw_full.datapoints, 'reversal')

        # Assertions
        self.assertEqual(
            all_reversals, 
            [False, False, True, False, False, True, False]
            )


    ##################
    # add_data_point #
    ##################
    def test_add_data_point_attribute_vals(self):
        self.dwt_stair._trial_num = 10
        self.dwt_stair.current_level = 65

        self.dwt_stair.add_data_point(1)

        self.assertEqual(
            self.dwt_stair.dw.datapoints[-1].trial_number, 
            10
        )

        self.assertEqual(
            self.dwt_stair.dw.datapoints[-1].level, 
            65
        )

        self.assertEqual(
            self.dwt_stair.dw.datapoints[-1].response, 
            1
        )
