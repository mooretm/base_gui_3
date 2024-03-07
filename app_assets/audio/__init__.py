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
AUDIO_DIRECTORY = Path(__file__).parent

###############
# Audio Files #
###############
# Calibration
CALSTIM_WAV = AUDIO_DIRECTORY / 'calibration' / 'cal_stim.wav'
