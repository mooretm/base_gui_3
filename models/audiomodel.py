""" Audio class for handling .wav files.
"""

###########
# Imports #
###########
# Import data science packages
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

# Import system packages
import os
from pathlib import Path

# Import audio packages
import soundfile as sf
import sounddevice as sd

# Import custom modules
from exceptions import audio_exceptions


#########
# BEGIN #
#########
class Audio:
    """ Class for use with .wav files.
    """

    def __init__(self, audio, **kwargs):
        """ Create audio object using file path or signal array
            audio: a Path object from pathlib, or a numpy array
            kwargs: must provide a sampling rate when passing an array
        """
        # Assign public attributes
        self.audio = audio

        # Print message to console
        self.msg = "Begin Audio Event"
        print('')
        print('*' * len(self.msg))
        print(self.msg)
        print('*' * len(self.msg))

        # If AUDIO argument is a Path, import .wav file;
        if isinstance(audio, Path):
            self._import_wav_file()

        # If AUDIO is an array, assign it to signal
        # and grab provided sampling rate
        elif isinstance(audio, np.ndarray):
            print("audiomodel: Found audio ndarray object")
            self.signal = self.audio
            try:
                self.fs = kwargs['sampling_rate']
            except: 
                print("audiomodel: A sampling rate must be provided " +
                      "with numpy array signals!")
                raise audio_exceptions.MissingSamplingRate()
        else:
            print("audiomodel: Unrecognized audio type")
            raise audio_exceptions.InvalidAudioType(type(self.audio))

        # Get audio details
        self._get_audio_details()


    def _import_wav_file(self):
        print(f"audiomodel: Loading {os.path.basename(self.audio)}...")

        # Parse file path
        self.directory = os.path.split(self.audio)[0]
        self.name = os.path.basename(self.audio)

        # Read audio file
        file_exists = os.access(self.audio, os.F_OK)
        if not file_exists:
            print("audiomodel: Audio file not found!")
            raise FileNotFoundError
        else:
            self.signal, self.fs = sf.read(self.audio)
            print(f"audiomodel: Sampling rate: {self.fs}")


    def _get_audio_details(self):
        # Get number of channels
        try:
            self.num_channels = self.signal.shape[1]
        except IndexError:
            self.num_channels = 1
        self.channels = np.array(range(1, self.num_channels+1))
        print(f"audiomodel: Number of channels in signal: {self.num_channels}")

        # Assign audio file attributes
        self.dur = len(self.signal) / self.fs
        self.t = np.arange(0, self.dur, 1/self.fs)
        print(f"audiomodel: Duration: {np.round(self.dur, 2)} seconds " +
            f"({np.round(self.dur/60, 2)} minutes)")

        # Get data type
        self.data_type = self.signal.dtype
        print(f"audiomodel: Data type: {self.data_type}")
        print("audiomodel: Done")


    def stop(self):
        """ Stop audio presentation.
        """
        sd.stop()


    def play(self, level=None, device_id=None, routing=None):
        """ Assign device id. Truncate audio/routing, if necessary,
            based on number of audio device channels. Set level.
        """
        # Initialization
        self.level = level
        self.device_id = device_id
        self.routing = routing

        print("\naudiomodel: Preparing for playback...")

        # Create a temporary audio file to modify
        self.temp = self.signal.copy()
        self.temp = self.temp.astype(np.float32)
        print(f"audiomodel: Data type converted to {self.temp.dtype}")

        # Assign default sounddevice settings
        try:
            self._set_defaults()
        except sd.PortAudioError:
            print("audiomodel: Invalid audio device!")
            raise audio_exceptions.InvalidAudioDevice(self.device_id)

        # Check channel routing
        if (self.num_channels != len(self.routing)) or (not self.routing):
            print("audiomodel: Invalid channel routing!")
            raise audio_exceptions.InvalidRouting(
                self.num_channels, self.routing)

        # Set level
        self._set_level()

        # Check for clipping after level has been applied
        try:
            self._check_clipping()
        except audio_exceptions.Clipping:
            print("audiomodel: Level caused clipping!")
            raise

        # Truncate audio file channels and routing, if necessary, 
        # based on available audio device channels
        self._check_channels_and_routing()

        # Present audio
        print("audiomodel: Attempting to present audio")
        sd.play(self.temp, mapping=self.routing)
        print("audiomodel: Done")
        print('*' * len(self.msg))


    #####################
    # Play Helper Funcs #
    #####################
    def _set_defaults(self):
        """ Set default sounddevice settings based on provided values.
        """
        # Assign audio device default
        try:
            sd.default.device = self.device_id
            print(f"audiomodel: Audio device: " + 
              f"{sd.query_devices(sd.default.device)['name']}")
        except sd.PortAudioError:
            raise
        
        # Get number of available audio device channels
        self.num_outputs = sd.query_devices(sd.default.device)['max_output_channels']
        print(f"audiomodel: Device outputs: {self.num_outputs}")

        # Assign audio device sampling rate based on 
        # provided audio sampling rate
        sd.default.samplerate = self.fs


    def _check_channels_and_routing(self):
        # Check that audio device has enough channels for audio
        if self.num_outputs < self.num_channels:
            print(f"\naudiomodel: {self.num_channels}-channel file, but "
                f"only {self.num_outputs} audio device output channels!")
            print("audiomodel: Dropping " +
                f"{self.num_channels - self.num_outputs} audio file channels")
            
            # Update audio file and channel routing dimensions to 
            # match number of available audio device outputs
            self.temp = self.temp[:, 0:self.num_outputs]
            self.routing = self.routing[:self.temp.shape[1]]
        
        print(f"audiomodel: Audio shape: {self.temp.shape}")


    def _set_level(self):  
        """ Set presentation level and check for clipping.
        """
        if self.level == None:
            # Normalize if no level is provided
            print("audiomodel: No level provided; normalizing to +/-1")
            if self.num_channels > 1:
                for chan in range(0, self.num_channels):
                    # Remove DC offset
                    self.temp[:, chan] = self.temp[:, chan] - np.mean(self.temp[:, chan])
                    # Normalize
                    self.temp[:, chan] = self.temp[:, chan] / np.max(np.abs(self.temp[:, chan]))
                    # account for num channels
                    self.temp[:, chan] = self.temp[:, chan] / self.num_channels 
            elif self.num_channels == 1:
                # Remove DC offset
                self.temp = self.temp - np.mean(self.temp)
                # Normalize
                self.temp = self.temp / np.max(np.abs(self.temp))
                # account for num channels
                self.temp = self.temp / 1
        else:
            # Convert level in dB to magnitude
            mag = self.db2mag(self.level)
            print(f"audiomodel: Adjusted Level (dB): {self.level}")
            print(f"audiomodel: Multiplying signal by: {np.round(mag,2)}")
            # Apply scaling factor to self.temp
            self.temp = self.temp * mag


    def _check_clipping(self):
        """ Plot clipped waveform for visual inspection.
        """
        if np.max(np.abs(self.temp)) > 1:
            # Raise exception to prevent playback
            raise audio_exceptions.Clipping


    def plot_waveform(self, title=None):
        """ Plot all channels overlaid.
        """
        # Create time base
        dur = len(self.temp) / self.fs
        t = np.arange(0, dur, 1/self.fs)
        plt.plot(t, self.temp)
        plt.title(title)
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.axhline(y=1, color='red', linestyle='--')
        plt.axhline(y=-1, color='red', linestyle='--')
        plt.show()


    ###########################
    # Signal Processing Funcs #
    ###########################
    def db2mag(self, db):
        """ 
            Convert decibels to magnitude. Takes a single
            value or a list of values.
        """
        # Must use this form to handle negative db values!
        try:
            mag = [10**(x/20) for x in db]
            return mag
        except:
            mag = 10**(db/20)
            return mag


    def mag2db(self, mag):
        """ 
            Convert magnitude to decibels. Takes a single
            value or a list of values.
        """
        try:
            db = [20 * np.log10(x) for x in mag]
            return db
        except:
            db = 20 * np.log10(mag)
            return db


    def rms(self, sig):
        """ 
            Calculate the root mean square of a signal. 
            
            NOTE: np.square will return invalid, negative 
                results if the number excedes the bit 
                depth. In these cases, convert to int64
                EXAMPLE: sig = np.array(sig,dtype=int)

            Written by: Travis M. Moore
            Last edited: Feb. 3, 2020
        """
        theRMS = np.sqrt(np.mean(np.square(sig)))
        return theRMS


    def setRMS(self, sig, amp, eq='n'):
        """
            Set RMS level of a 1-channel or 2-channel signal.
        
            SIG: a 1-channel or 2-channel signal
            AMP: the desired amplitude to be applied to 
                each channel. Note this will be the RMS 
                per channel, not the total of both channels.
            EQ: takes 'y' or 'n'. Whether or not to equalize 
                the levels in a 2-channel signal. For example, 
                a signal with an ILD would lose the ILD with 
                EQ='y', so the default in 'n'.

            EXAMPLE: 
            Create a 2 channel signal
            [t, tone1] = mkTone(200,0.1,30,48000)
            [t, tone2] = mkTone(100,0.1,0,48000)
            combo = np.array([tone1, tone2])
            adjusted = setRMS(combo,-15)

            Written by: Travis M. Moore
            Created: Jan. 10, 2022
            Last edited: May 17, 2022
        """
        if len(sig.shape) == 1:
            rmsdb = self.mag2db(self.rms(sig))
            refdb = amp
            diffdb = np.abs(rmsdb - refdb)
            if rmsdb > refdb:
                sigAdj = sig / self.db2mag(diffdb)
            elif rmsdb < refdb:
                sigAdj = sig * self.db2mag(diffdb)
            # Edit 5/17/22
            # Added handling for when rmsdb == refdb
            elif rmsdb == refdb:
                sigAdj = sig
            return sigAdj

        elif len(sig.shape) == 2:
            rmsdbLeft = self.mag2db(self.rms(sig[0]))
            rmsdbRight = self.mag2db(self.rms(sig[1]))

            ILD = np.abs(rmsdbLeft - rmsdbRight) # get lvl diff

            # Determine lvl advantage
            if rmsdbLeft > rmsdbRight:
                lvlAdv = 'left'
                #print("Adv: %s" % lvlAdv)
            elif rmsdbRight > rmsdbLeft:
                lvlAdv = 'right'
                #print("Adv: %s" % lvlAdv)
            elif rmsdbLeft == rmsdbRight:
                lvlAdv = None

            #refdb = amp - 3 # apply half amp to each channel
            refdb = amp
            diffdbLeft = np.abs(rmsdbLeft - refdb)
            diffdbRight = np.abs(rmsdbRight - refdb)

            # Adjust left channel
            if rmsdbLeft > refdb:
                sigAdjLeft = sig[0] / self.db2mag(diffdbLeft)
            elif rmsdbLeft < refdb:
                sigAdjLeft = sig[0] * self.db2mag(diffdbLeft)
            # Adjust right channel
            if rmsdbRight > refdb:
                sigAdjRight = sig[1] / self.db2mag(diffdbRight)
            elif rmsdbRight < refdb:
                sigAdjRight = sig[1] * self.db2mag(diffdbRight)

            # If there is a lvl difference to maintain across channels
            if eq == 'n':
                if lvlAdv == 'left':
                    sigAdjLeft = sigAdjLeft * self.db2mag(ILD/2)
                    sigAdjRight = sigAdjRight / self.db2mag(ILD/2)
                elif lvlAdv == 'right':
                    sigAdjLeft = sigAdjLeft / self.db2mag(ILD/2)
                    sigAdjRight = sigAdjRight * self.db2mag(ILD/2)

            sigBothAdj = np.array([sigAdjLeft, sigAdjRight])
            return sigBothAdj
