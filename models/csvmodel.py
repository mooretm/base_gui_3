""" Class to write data to .csv
"""

############
# IMPORTS  #
############
# Import system packages
import csv
from pathlib import Path
from datetime import datetime
import os


#########
# MODEL #
#########
class CSVModel:
    """ Write provided dictionary to .csv
    """
    def __init__(self, sessionpars):
        self.sessionpars = sessionpars

        # Generate date stamp
        self.datestamp = datetime.now().strftime("%Y_%b_%d_%H%M")

        # Create file name
        subject = self.sessionpars['subject'].get()
        condition = self.sessionpars['condition'].get()
        self.filename = f"{subject}_{condition}_{self.datestamp}.csv"

        # Create data directory name
        self.data_directory = "Data"

        # Create file path
        self.file = Path(os.path.join(self.data_directory, self.filename))


    def _check_data_directory(self):
        """ Check whether data directory exists.
        """
        data_dir_exists = os.access(self.data_directory, os.F_OK)
        if not data_dir_exists:
            try:
                print(f"\ncsvmodel: {self.data_directory} directory not " +
                    "found! Creating it...")
                os.mkdir(self.data_directory)
                print(f"csvmodel: Successfully created " +
                    f"{self.data_directory} directory!")
            except OSError:
                msg = (
                    f"\ncsvmodel: Could not find or create " 
                    f"'{self.data_directory}' directory"
                )
                raise OSError(msg)
        else:
            print(f"\ncsvmodel: Found data directory")


    def _check_write_access(self):
        """ Check whether path and file are writeable.
        """
        # Check for write access to store csv
        file_exists = os.access(self.file, os.F_OK)
        parent_writable = os.access(self.file.parent, os.W_OK)
        file_writable = os.access(self.file, os.W_OK)
        if (
            (not file_exists and not parent_writable) or
            (file_exists and not file_writable)
        ):
            msg = (
                f"\ncsvmodel: Permission denied accessing "
                f"file: {self.filename}"
            )
            raise PermissionError(msg)


    def save_record(self, data):
        """ Save a dictionary of data to .csv file 
        """
        # Verify or create data directory
        self._check_data_directory()

        # Check write access
        self._check_write_access()

        # Write data to .csv
        newfile = not self.file.exists()
        with open(self.file, 'a', newline='') as fh:
            csvwriter = csv.DictWriter(fh, fieldnames=data.keys())
            if newfile:
                csvwriter.writeheader()
            csvwriter.writerow(data)
        print("\ncsvmodel: Record successfully saved!")
