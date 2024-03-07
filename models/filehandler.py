""" Classes to write data to various file types. 

    Author: Travis M. Moore
    Created: March 07, 2024
    Last edited: March 07, 2024
"""

############
# IMPORTS  #
############
# System
import csv
from pathlib import Path
import os


######################
# Generic File Class #
######################
class FileHandler:
    """ Generic file class to be inherited by specific file type classes. """
    def __init__(self, filename, **kwargs):
        """ Check filename extension matches child class.

                :params: filename: name of CSV file with extension
                :kwargs: data_dir_name: custom data directory 
        """
        # Test for valid extension in filename
        if not filename.endswith(self.ext):
            raise Exception("Invalid file format!")
        
        # Assign variables
        self.filename = filename

        # Look for kwargs
        if 'data_directory' in kwargs:
            self.data_directory = kwargs['data_directory']
        else:
            self.data_directory = "Data"


    def _check_for_data_folder(self):
        """ Check for existing data folder. Create a data folder if
            it doesn't currently exist.
        """
        data_dir_exists = os.access(self.data_directory, os.F_OK)
        if not data_dir_exists:
            print(f"\nfilehandler: {self.data_directory} directory not " +
                "found! Creating it...")
            os.makedirs(self.data_directory)
            print(f"filehandler: Successfully created {self.data_directory} " +
                  "directory!")
            

    def _create_file_path(self):
        """ Create file path from filename and data_directory. """
        self.file = Path(os.path.join(self.data_directory, self.filename))


    def _check_write_access(self):
        """ Check for write access to store CSV. """
        file_exists = os.access(self.file, os.F_OK)
        parent_writable = os.access(self.file.parent, os.W_OK)
        file_writable = os.access(self.file, os.W_OK)
        if (
            (not file_exists and not parent_writable) or
            (file_exists and not file_writable)
        ):
            msg = f"\nfilehandler: Permission denied accessing file: \
                {self.filename}"
            raise PermissionError(msg)
        
    
    def _write(self, data):
        """ To be overridden by File class. """
        pass


    def save(self, data):
        """ Save a dictionary of data to .csv file. """
        # Create data directory if it does not exist
        self._check_for_data_folder()

        # Create full path
        self._create_file_path()

        # Check for write access
        try:
            self._check_write_access()
        except PermissionError:
            raise

        # Write data to file
        self._write(data)


##############################
# Specific File Type Classes #
##############################
class CSVFile(FileHandler):
    """ Specific file type: CSV. """
    # Extension checked by FileHandler
    ext = "csv"

    def _write(self, data):
        """ Write dict data to CSV. Check for existing file to determine 
            whether or not to include header when writing to CSV.
        """
        print(f"\nfilehandler: Attempting to write {self.filename} " +
               f"to {self.file} as CSV file...")
        #print(f"filehandler: data to save:\n{data}")

        try:
            # Write file
            newfile = not self.file.exists()
            with open(self.file, 'a', newline='') as fh:
                csvwriter = csv.DictWriter(fh, fieldnames=data.keys())
                if newfile:
                    csvwriter.writeheader()
                csvwriter.writerow(data)
            print("filehandler: Data successfully written!")
        except AttributeError as e:
            print(f"filehandler: {e}")
