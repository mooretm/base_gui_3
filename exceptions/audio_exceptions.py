""" Custom exceptions for the audiomodel class.

    Written by: Travis M. Moore
    Last edited: July 18, 2023
"""


class Clipping(Exception):
    """ Audio clipping has occurred """


class InvalidAudioDevice(Exception):
    """ Invalid audio device """

    def __init__(self, device, *args):
        super().__init__(args)
        self.device = device


    def __str__(self):
        return f'Audio Exception: {self.device} is not a valid audio device ID!'


class InvalidRouting(Exception):
    """ Invalid channel routing """

    def __init__(self, channels, routing, *args):
        super().__init__(args)
        self.channels = channels
        self.routing = routing


    def __str__(self):
        return f'Audio Exception: Audio has {self.channels} channel(s), but routing of {self.routing}.'


class InvalidAudioType(Exception):
    """ Invalid audio type """

    def __init__(self, audio_type, *args):
        super().__init__(args)
        self.audio_type = audio_type


    def __str__(self):
        return f'Audio Exception: Audio of type {self.audio_type} is not a valid audio type.'


class MissingSamplingRate(Exception):
    """ Missing sampling rate """

    def __init__(self, *args):
        super().__init__(args)


    def __str__(self):
        return f'Audio Exception: A sampling rate must be provided with numpy array signals.'
