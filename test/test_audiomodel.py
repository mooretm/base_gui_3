""" Tests for audiomodel. 

    Written by: Travis M. Moore
    Created: September 14, 2023
    Last edited: September 14, 2023
"""

###########
# Imports #
###########
# Import testing packages
import unittest
from unittest import TestCase
from unittest import mock

# Import data science packages
import numpy as np
import pandas as pd

# Import audio packages
#import soundfile as sf

# Import system packages
from pathlib import Path

# Import custom modules
from models import audiomodel
from exceptions import audio_exceptions


#########
# Begin #
#########
def mkTone(freq, dur, phi=0, fs=48000):
    """ Create a pure tone. Returns the signal 
        AND the time base. 

        FREQ: frequency in Hz
        DUR: duration in SECONDS
        PHI: phase in DEGREES
        FS: sampling rate

        EXAMPLE: [t, sig] = (500,0.2,0,48000)
    """
    phi = np.deg2rad(phi) # to radians
    t = np.arange(0,dur,1/fs) # time base
    sig = np.sin(2*np.pi*freq*t+phi)
    return [t, sig]


class TestAudioModel(TestCase):
    def setUp(self):
        # Create mono audio array
        t, self.mono_array = mkTone(500, 1, 0, 48000)

        # Create stereo audio array
        self.stereo_array = np.array([np.repeat(self.mono_array, 2)])
        self.stereo_array = self.stereo_array.reshape(48000, 2)

        # Create eight-channel audio array
        self.eightchan_array = np.array([np.repeat(self.mono_array, 8)])
        self.eightchan_array = self.eightchan_array.reshape(48000, 8) 


    def tearDown(self):
        del self.mono_array
        del self.stereo_array
        del self.eightchan_array


    # Import numpy arrays #
    def test_import_valid_mono_array(self):
        # Create audio object
        self.a_mono = audiomodel.Audio(self.mono_array, sampling_rate=48000)
        # Number of channels
        self.assertEqual(self.a_mono.num_channels, 1)
        # Sampling rate
        self.assertEqual(self.a_mono.fs, 48000)
        # Duration
        self.assertEqual(self.a_mono.dur, 1)

    def test_import_valid_stereo_array(self):
        # Create audio object
        self.a_stereo = audiomodel.Audio(self.stereo_array, sampling_rate=48000)
        # Number of channels
        self.assertEqual(self.a_stereo.num_channels, 2)

    def test_import_valid_eightchan_array(self):
        # Create audio object
        self.a_eightchan = audiomodel.Audio(self.eightchan_array, sampling_rate=48000)
        # Number of channels
        self.assertEqual(self.a_eightchan.num_channels, 8)

    def test_missing_sampling_rate(self):
        with self.assertRaises(audio_exceptions.MissingSamplingRate):
            self.a_mono = audiomodel.Audio(self.mono_array)


    # Import .wav files #
    def test_import_valid_mono_wav(self):
        # Create audio object
        self.a_mono_wav = audiomodel.Audio(Path(r'.\test\sample_stim.wav'))
        # Number of channels
        self.assertEqual(self.a_mono_wav.num_channels, 1)
        # Duration
        self.assertEqual(self.a_mono_wav.dur, 2.3371201814058957)

    def test_invalid_audio_type(self):
        with self.assertRaises(audio_exceptions.InvalidAudioType):
            self.a_mono_wav = audiomodel.Audio(r'.\test\sample_stim.wav')

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.a_mono_wav = audiomodel.Audio(Path(r'./invalid_path.wav'))


    # Play functions #
    def test_play_invalid_audio_device(self):
        self.audio = audiomodel.Audio(self.mono_array, sampling_rate=48000)
        with self.assertRaises(audio_exceptions.InvalidAudioDevice):
            self.audio.play(level=-30, device_id=999, routing=[1])

    def test_play_invalid_routing(self):
        self.audio = audiomodel.Audio(self.stereo_array, sampling_rate=48000)
        with self.assertRaises(audio_exceptions.InvalidRouting):
            self.audio.play(level=-30, device_id=2, routing=[1])

    # _set_level test?

    def test_clipping(self):
        self.audio = audiomodel.Audio(self.mono_array, sampling_rate=48000)
        with self.assertRaises(audio_exceptions.Clipping):
            self.audio.play(level=3000, device_id=2, routing=[1])

    def test_play_truncate_channels_to_match_device_outputs(self):
        with mock.patch('models.audiomodel.sd.play') as fake_play:
            self.audio = audiomodel.Audio(self.eightchan_array, sampling_rate=48000)
            self.audio.play(level=-30, device_id=2, routing=[1,2,3,4,5,6,7,8])
            self.assertEqual(self.audio.temp.shape, (48000,2))

    def test_play_num_channels_match_device_outputs(self):
        with mock.patch('models.audiomodel.sd.play') as fake_play:
            self.audio = audiomodel.Audio(self.stereo_array, sampling_rate=48000)
            self.audio.play(level=-30, device_id=2, routing=[1,2])
            self.assertEqual(self.audio.temp.shape, (48000,2))


if __name__ == '__main__':
    unittest.main()
