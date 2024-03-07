""" Paths to README resources.
"""

###########
# Imports #
###########
# System imports
from pathlib import Path


#############
# Constants #
#############
README_DIRECTORY = Path(__file__).parent


###############
# README File #
###############
README_HTML = README_DIRECTORY / 'README.html'
README_MD = README_DIRECTORY / 'README.md'


##############
# Change Log #
##############
CHANGELOG_HTML = README_DIRECTORY / 'CHANGELOG.html'
CHANGELOG_MD = README_DIRECTORY / 'CHANGELOG.md'
