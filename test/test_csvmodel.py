""" Tests for csvmodel. """

###########
# Imports #
###########
# Import testing packages
from unittest import TestCase
from unittest import mock
from unittest.mock import patch

# Import GUI packages
import tkinter as tk

# Import system packages
import os
from datetime import datetime
import csv

# Import custom modules
from models import csvmodel


#########
# Begin #
#########
class TestCSVModel(TestCase):
    """ Unit tests for csvmodel.
    """

    def setUp(self):
        """ Create necessary mocks and variables. Automatically 
            runs before each test. 
        """
        # Need a root for tk variables to work
        self.root = tk.Tk()

        # Fake sessionpars
        self.fake_sessionpars = {
            'subject': tk.StringVar(value='999'),
            'condition': tk.StringVar(value='test'),
            'matrix_file_path': tk.StringVar(value='mock_matrix.csv'),
            'audio_files_dir': tk.StringVar(value='sample_audio_dir'),
            'repetitions': tk.IntVar(value=2),
            'randomize': tk.IntVar(value=0)
        }

        # Instantiate CSVModel object
        self.c = csvmodel.CSVModel(self.fake_sessionpars)

        # Create a temporary file for testing
        self.test_file_path = 'test_data/test_file.csv'


    def tearDown(self):
        """ Delete objects from setUp. Automatically runs
            after each test.
        """
        del self.root
        del self.fake_sessionpars
        
        if self.c.file.exists():
            self.c.file.unlink()
        del self.c


    @patch('models.csvmodel.datetime')
    def test_init_with_datetime_mock(self, mock_datetime):
        """ Instantiate a csvmodel object and check the datetime
            stamp and filename.
        """
        # Static date for testing
        mock_datetime.now.return_value = datetime(2023, 12, 5, 11, 52)

        # Instantiate object
        c = csvmodel.CSVModel(self.fake_sessionpars)

        # Assertions
        self.assertEqual(self.c.data_directory, "Data")
        self.assertEqual(c.datestamp, "2023_Dec_05_1152")
        self.assertEqual(c.filename, "999_test_2023_Dec_05_1152.csv")


    def test__check_data_directory_exists(self):
        """ Test when directory already exists.
        """
        # Create temp directory
        test_dir = 'TempData'
        os.mkdir(test_dir)

        # Update object to point to temp directory
        self.c.data_directory = 'TempData'

        # Check the data directory
        self.c._check_data_directory()

        # Clean up
        if os.path.exists(test_dir):
            os.rmdir(test_dir)


    def test__check_data_directory_create_dir(self):
        """ Test the appropriate directory is created when 
            the directory does not already exist.
        """
        # Create temp directory for testing
        test_dir = 'TempData'

        # Ensure directory does not yet exist
        self.assertFalse(os.path.exists(test_dir))

        # Modify data directory in CSVModel to point to temp dir
        self.c.data_directory = test_dir

        # Call _check_data_directory function
        self.c._check_data_directory()

        # Assertions
        self.assertTrue(os.path.exists(test_dir))

        # Clean up
        if os.path.exists(test_dir):
            os.rmdir(test_dir)


    @patch('models.csvmodel.os.mkdir', 
           side_effect=OSError("Mocked os.mkdir failure"))
    def test__check_data_directory_failure(self, mock_mkdir):
        """ Test that OSError is raised when mkdir fails.
        """
        # Create temp directory for testing
        test_dir = 'TempData'
        self.assertFalse(os.path.exists(test_dir))

        # Modify data directory in CSVModel to point to temp dir
        self.c.data_directory = test_dir

        with self.assertRaises(OSError, msg="Mocked os.mkdir failure"):
            self.c._check_data_directory()

        if os.path.exists(test_dir):
            os.rmdir(test_dir)








    @mock.patch('models.csvmodel.os.access', return_value=True)
    def test__check_write_access_successful(self, mock_access):
        self.c._check_write_access()
        mock_access.assert_has_calls([
            mock.call(self.c.file, mock.ANY),
            mock.call(self.c.file.parent, mock.ANY)
        ])


    # @patch('models.csvmodel.os.access', side_effect=PermissionError)
    # def test__check_write_access_access_denied(self, mock_access):
    #     """ Test that PermissionError is raised when os.access fails.
    #     """
    #     with self.assertRaises(PermissionError):
    #         self.c._check_write_access()




    @mock.patch('models.csvmodel.os.access', side_effect=[False, False, True])
    def test__check_write_access_parent_not_writeable(self, mock_access):
        with self.assertRaises(PermissionError):
            self.c._check_write_access()
        mock_access.assert_has_calls([
            mock.call(self.c.file, mock.ANY),
            mock.call(self.c.file.parent, mock.ANY)
        ])


    @mock.patch('models.csvmodel.os.access', side_effect=[True, False, True])
    def test__check_write_access_write_access_denied(self, mock_access):
        with self.assertRaises(PermissionError):
            self.c._check_write_access()
        mock_access.assert_has_calls([
            mock.call(self.c.file, mock.ANY),
            mock.call(self.c.file.parent, mock.ANY)
        ])


    @mock.patch('models.csvmodel.os.access', side_effect=[True, True, False])
    def test__check_write_access_write_access_denied(self, mock_access):
        with self.assertRaises(PermissionError):
            self.c._check_write_access()
        mock_access.assert_has_calls([
            mock.call(self.c.file, mock.ANY),
            mock.call(self.c.file.parent, mock.ANY)
        ])







    # @mock.patch('models.csvmodel.os.access', side_effect=[False, True])
    # def test_save_record_file_access_denied(self, mock_access):
    #     data = {'field1': 'value1', 'field2': 'value2'}
        
    #     # Call the method and expect a PermissionError
    #     with self.assertRaises(PermissionError):
    #         self.c.save_record(data)

    #     # Ensure os.access is called twice with the expected arguments
    #     mock_access.assert_has_calls([
    #         mock.call(self.c.file, mock.ANY),
    #         mock.call(self.c.file.parent, mock.ANY)
    #     ])


    def test_save_record_header_not_rewritten(self):
        # Mock the _check_write_access method
        with mock.patch.object(
            self.c, '_check_write_access'
        ) as mock_check_write_access:
            
            # Test data
            test_data1 = {'field1': 'value1', 'field2': 'value2'}
            test_data2 = {'field1': 'value3', 'field2': 'value4'}

            # Call the save_record method twice with different sets of data
            with mock.patch.object(
                self.c, '_check_data_directory'
            ) as mock_check_data_dir:
                self.c.save_record(test_data1)
                mock_check_data_dir.assert_called_once()

            with mock.patch.object(
                self.c, '_check_data_directory'
            ) as mock_check_data_dir:
                self.c.save_record(test_data2)
                mock_check_data_dir.assert_called_once()

            # Ensure _check_write_access is called twice (once for each
            # save_record call)
            mock_check_write_access.assert_has_calls(
                [mock.call()] * 2
            )

            # Check if the file was created and contains the correct data
            self.assertTrue(self.c.file.exists())

            # Read the actual content from the file using csv.DictReader
            with open(self.c.file, 'r') as file:
                reader = csv.DictReader(file)
                actual_rows = list(reader)

            # Check if the header matches the keys of the first test data
            self.assertEqual(
                reader.fieldnames, list(test_data1.keys())
            )

            # Check if both sets of data are present in the same order as
            # written
            self.assertEqual(actual_rows, [test_data1, test_data2])

            # Check if the content is well-formed CSV
            try:
                csv.reader(open(self.c.file, 'r').read().splitlines(), delimiter=',')
            except csv.Error as e:
                self.fail(f"The actual content is not well-formed CSV: {e}")