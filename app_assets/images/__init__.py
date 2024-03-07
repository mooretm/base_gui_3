""" Paths to image resources.
"""

###########
# Imports #
###########
# System imports
from pathlib import Path

#############
# Constants #
#############
IMAGE_DIRECTORY = Path(__file__).parent

##########
# Images #
##########
# Taskbar
LOGO_FULL_PNG = IMAGE_DIRECTORY / 'logo_icons' / 'logo_full.png'
LOGO_FULL_ICO = IMAGE_DIRECTORY / 'logo_icons' / 'logo_full.ico'
# LOGO_26x32 = IMAGE_DIRECTORY / 'logo3_26x32.png'
# LOGO_97x120 = IMAGE_DIRECTORY / 'logo_97x120.png'
# LOGO_FULL = IMAGE_DIRECTORY / 'logo3_full.ico'

# File menu
SETTINGS_ICON = IMAGE_DIRECTORY / 'menu_icons' / 'gear-wide-connected.png'
PLAY_ICON = IMAGE_DIRECTORY / 'menu_icons' / 'play-fill.png'
#QUIT_ICON = IMAGE_DIRECTORY / 'x-circle.png'

# Tools menu
AUDIO_ICON = IMAGE_DIRECTORY / 'menu_icons' /  'speaker.png'
CALIBRATION_ICON = IMAGE_DIRECTORY / 'menu_icons' /  'sliders2-vertical.png'

# Help menu
ABOUT_ICON = IMAGE_DIRECTORY / 'menu_icons' /  'info-square.png'
HELP_ICON = IMAGE_DIRECTORY / 'menu_icons' /  'file-earmark-text.png'
CHANGELOG_ICON = IMAGE_DIRECTORY / 'menu_icons' / 'list-task.png'

# Misc
SEARCH_ICON = IMAGE_DIRECTORY / 'search.png'
SUBMIT_ICON = IMAGE_DIRECTORY / 'check-circle.png'
