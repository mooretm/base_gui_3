""" Class for importing matrix file and preparing trials.
"""

# Import data science packages
import pandas as pd

# Import system packages
import random
import os
from pathlib import Path


#########
# BEGIN #
#########
class StimulusModel:
    def __init__(self, sessionpars):
        
        # Assign variables
        self.sessionpars = sessionpars

        #####################
        # Sequence of Funcs #
        #####################
        # Import matrix file and add full audio paths
        self._load_matrix()
        self._add_full_audio_paths()

        # Make trial repetitions
        self._do_reps()

        # If specified, randomize trials
        if self.sessionpars['randomize'].get() == 1:
            self._randomize()


    def _load_matrix(self):
        try:
            print('\nstimulusmodel: Reading matrix file')
            # Create private attribute of raw matrix file
            self._matrix_file = pd.read_csv(
                self.sessionpars['matrix_file_path'].get()
            )
        except FileNotFoundError:
            print('stimulusmodel: File not found!')
            raise


    def _add_full_audio_paths(self):
        """ Add the audiodir from sessionpars to audio file 
            names in raw matrix file.
        """
        # Get audio files directory
        audio_dir = Path(self.sessionpars['audio_files_dir'].get())

        for row in self._matrix_file.index:
            # Create full path to audio file
            full_path = os.path.join(
                audio_dir, self._matrix_file.iloc[row,0]
            )

            # Update name in _matrix_file df
            self._matrix_file.iloc[row,0] = full_path


    def _do_reps(self):
        """ Repeat matrix file trials according to the number 
            specified in File>Session.
        """
        # Create a copy of private raw matrix import
        # to preserve it and avoid multiple versions issues
        self.matrix = self._matrix_file.copy()

        # Make sure there is at least 1 'repetition'
        if (self.sessionpars['repetitions'].get() == 0) or \
            (self.sessionpars['repetitions'].get() == None):
            self.sessionpars['repetitions'].set(1)

        # Create repeated trials
        print('stimulusmodel: Creating trial repetitions')        
        self.matrix = pd.concat(
            [self.matrix] * self.sessionpars['repetitions'].get(), 
            ignore_index=True
        )


    def _randomize(self):
        """ Randomize trials in self.matrix.
        """
        print('stimulusmodel: Randomizing trials')
        # Get trial numbers from matrix df index
        trials = list(self.matrix.index)

        # Shuffle (in place)
        random.shuffle(trials)

        # Create new df column with shuffled trial order
        self.matrix['order'] = trials

        # Sort by new order column
        self.matrix.sort_values(by='order', inplace=True)

        # Remove order column
        self.matrix.drop('order', axis=1, inplace=True)

        # Reset index
        self.matrix.reset_index(drop=True, inplace=True)
