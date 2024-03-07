""" Class for loading calibration file, determining calibration 
    offset, and calculating adjusted presentation level.

    Written by: Travis M. Moore
"""

############
# IMPORTS  #
############
# Import system packages
import os

# Import custom modules
from app_assets import audio


#########
# MODEL #
#########
class CalModel:
    """ Write provided dictionary to .csv
    """
    def __init__(self, sessionpars):
        self.sessionpars = sessionpars


    def get_cal_file(self):
        """ Load specified calibration file
        """
        print("calmodel: Locating calibration file...")
        if self.sessionpars['cal_file'].get() == 'cal_stim.wav':
            self.cal_file = audio.CALSTIM_WAV
            file_exists = os.access(self.cal_file, os.F_OK)
            if not file_exists:
                raise AttributeError
        else: # Custom file was provided
            self.cal_file = self.sessionpars['cal_file'].get()

        print(f"calmodel: Using {self.cal_file}")


    def calc_offset(self):
        """ Calculate adjusted presentation level
        """
        # Calculate SLM offset
        print("\ncalmodel: Calculating new presentation level...")
        slm_offset = self.sessionpars['slm_reading'].get() - self.sessionpars['cal_level_dB'].get()
        self.sessionpars['slm_offset'].set(slm_offset)
        # Provide console feedback
        print(f"calmodel: Starting level (dB FS): " +
              f"{self.sessionpars['cal_level_dB'].get()}")
        print(f"calmodel: SLM reading (dB): " +
              f"{self.sessionpars['slm_reading'].get()}")
        print(f"calmodel: SLM offset: {self.sessionpars['slm_offset'].get()}")

        # SLM offset not yet saved!
        # This must happen in controller using: self._save_sessionpars()


    def calc_level(self, desired_level_dB):
        # Calculate presentation level
        self.sessionpars['desired_level_dB'].set(desired_level_dB)
        scaled_level = desired_level_dB - self.sessionpars['slm_offset'].get()
        self.sessionpars['adjusted_level_dB'].set(scaled_level)
        print(f"\ncalmodel: Desired level in dB: " +
              f"{self.sessionpars['desired_level_dB'].get()}")
        print(f"calmodel: SLM offset: {self.sessionpars['slm_offset'].get()}")
        print(f"calmodel: Adjusted level (dB): " +
            f"{self.sessionpars['adjusted_level_dB'].get()}")

        # Calculated level not yet saved! 
        # This must happen in controller using: self._save_sessionpars()
