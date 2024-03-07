""" Class to check current version number against latest version 
    library on Starfile. If upgrade is available, display
    a message. If upgrade is mandatory, show warning and 
    kill app. 

    Written by: Travis M. Moore
    Created: Apr 11, 2023
"""

###########
# Imports #
###########
# Data science
import pandas as pd


#########
# BEGIN #
#########
class VersionChecker:
    """ Class to check current version number against latest version 
        library on Starfile. If upgrade is available but not mandatory,
        return TRUE and display a message. If upgrade is mandatory, 
        return FALSE, display a message, and kill app. 
    """
    def __init__(self, lib_path, app_name, app_version):
        self.lib_path = lib_path
        self.app_name = app_name
        self.app_version = app_version
        self.status = None

        # Import version library to cross-reference
        print(f"\nversionmodel: Checking current version...")
        try:
            self.import_version_library(self.lib_path)
        except FileNotFoundError:
            print(f"versionmodel: Could not read from version library!")
            self.status = 'library_inaccessible'
            return

        # Check version number
        self.check_for_updates()


    def check_for_updates(self):
        """ Check app version against latest available version from library.
        """
        # Retrieve app record from library 
        bools = self.version_library['name']==self.app_name
        status = self.version_library[bools]

        # Check whether current version matches version library
        try:
            if status.iloc[0]['version'] != self.app_version:
                print('versionmodel: New version available!')
                if status.iloc[0]['mandatory'] == 'yes':
                    self.status = 'mandatory'
                elif status.iloc[0]['mandatory'] == 'no':
                    self.status = 'optional'

                # Assign latest version number to public attribute
                self.new_version = status.iloc[0]['version']

            else:
                print("versionmodel: You are up to date!")
                self.status = 'current'
        except IndexError:
            print("versionmodel: Cannot retrieve version number!")
            print(f"versionmodel: '{self.app_name}' cannot be found in the " +
                  "version library!")
            self.status = 'app_not_found'


    def import_version_library(self, lib_path):
        """ Load version library
        """
        # Download version library for crossreferencing
        try:
            self.version_library = pd.read_csv(lib_path)
        except FileNotFoundError:
            raise FileNotFoundError
