""" Global functions.
"""

###########
# Imports #
###########
# Import system packages
import sys
import os


#########
# Funcs #
#########
def resource_path(relative_path):
    """ Create the absolute path to compiled resources
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def truncate_path(long_path):
    """ Truncate path (if necessary) and return 
        shortened path for display
    """
    if len(long_path) >= 60:
        short = '...' + long_path[-55:]
        return short
    else:
        if long_path == "":
            return 'Please select a file'
        else:
            return long_path
