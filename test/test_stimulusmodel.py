""" Tests for stimulusmodel """

###########
# Imports #
###########
# Import testing packages
import unittest
from unittest.mock import patch, mock_open

# Import GUI packages
import tkinter as tk

# Import misc packages
import random

# Import custom modules
from models.stimulusmodel import StimulusModel


#########
# Begin #
#########    
class TestStimulusModel(unittest.TestCase):
    """ Unit tests for StimulusModel class.
    """

    def setUp(self):
        """ Create necessary mocks and variables. Automatically 
            runs before each test. 
        """
        # Need a root for tk variables to work
        self.root = tk.Tk()

        # Mock file with data
        self.fake_data_file = mock_open(
            read_data=(
                "audio_file,pres_level\r\n" # Header
                "stim_1.wav,75\r\n" # Row 1
                "stim_2.wav,70\r\n" # Row 2
            )
        )

        # Fake sessionpars
        self.sessionpars = {
            'matrix_file_path': tk.StringVar(value='mock_matrix.csv'),
            'audio_files_dir': tk.StringVar(value='sample_audio_dir'),
            'repetitions': tk.IntVar(value=2),
            'randomize': tk.IntVar(value=0)
        }


    def tearDown(self):
        """ Delete objects from setUp. Automatically runs
            after each test.
        """
        del self.root
        del self.fake_data_file
        del self.sessionpars


    def test_import_matrix_file(self):
        """ Test whether mock matrix file is imported correctly.
        """
        # Set sessionpars
        sessionpars = self.sessionpars
        reps = 10
        sessionpars['repetitions'].set(reps)

        # Expected output after adding audio paths
        expected_audio_names = [
            'sample_audio_dir\\stim_1.wav', 
            'sample_audio_dir\\stim_2.wav'
        ]

        # Expected levels
        expected_levels = [75, 70]

        # Create class instance and test
        with patch('builtins.open', self.fake_data_file):
            # Create an instance of StimulusModel
            stimulus_model = StimulusModel(sessionpars)

            # Make sure '_matrix_file' attribute was created
            self.assertIsNotNone(stimulus_model._matrix_file)
            # Test '_matrix_file' df shape based on mock file
            self.assertEqual(stimulus_model._matrix_file.shape, (2,2))
            # Test '_matrix_file' values (read original file: 1 presentation)
            self.assertEqual(stimulus_model._matrix_file.iloc[:, 0].tolist(), expected_audio_names)

            # Make sure 'matrix' attribute was created
            self.assertIsNotNone(stimulus_model.matrix)
            # Test 'matrix' df shape based on mock file
            self.assertEqual(stimulus_model.matrix.shape, (20,2))
            # Test 'matrix' values (after repetitions: final output)
            self.assertEqual(stimulus_model.matrix.iloc[:,0].tolist(), expected_audio_names*reps)

            # Test presentation levels
            self.assertEqual(stimulus_model.matrix.iloc[:,1].tolist(), expected_levels*reps)


    def test__randomize_called(self):
        """ _randomized should be called when 
            sessionpars['randomize'] == 1
        """
        # Set sessionpars
        sessionpars = self.sessionpars
        sessionpars['randomize'].set(1)

        # Create class instance and test
        with patch('builtins.open', self.fake_data_file):
            with patch('random.shuffle') as fake_shuffle:
                stimulus_model = StimulusModel(sessionpars)

                # Test that _randomize was called
                fake_shuffle.assert_called_once()


    def test__randomize_not_called(self):
        """ _randomized should NOT be called when 
            sessionpars['randomize'] == 0
        """
        # Set sessionpars
        sessionpars = self.sessionpars
        sessionpars['randomize'].set(0)

        # Create class instance and test
        with patch('builtins.open', self.fake_data_file):
            with patch('random.shuffle') as fake_shuffle:
                stimulus_model = StimulusModel(sessionpars)

                # Test that _randomize was not called
                fake_shuffle.assert_not_called()


    def test_zero_repetitions(self):
        """ Test that repetitions of '0' or 'None' are
            converted to '1'.
        """
        # Set sessionpars
        sessionpars = self.sessionpars
        sessionpars['randomize'].set(0)
        sessionpars['repetitions'].set(0)

        # Create class instance and test
        with patch('builtins.open', self.fake_data_file):
            stimulus_model = StimulusModel(sessionpars)

            self.assertEqual(stimulus_model.matrix.shape, (2,2))


    def test__randomize_values(self):
        """ Test whether the presentation levels are in 
            a given order after randomizing with a set seed.
        """
        # Modify sessionpars to set repetitions and enable randomization
        sessionpars = self.sessionpars
        sessionpars['repetitions'].set(3)
        sessionpars['randomize'].set(1)

        # Create local random number generator with fixed seed
        rng = random.Random(40)

        with patch('builtins.open', self.fake_data_file):
            with patch('random.shuffle', side_effect=lambda x, r=rng: r.shuffle(x)):
                stimulus_model = StimulusModel(sessionpars)
                
                self.assertEqual(stimulus_model.matrix.iloc[:,1].tolist(), [70,70,75,70,75,75])


if __name__ == '__main__':
    unittest.main()
