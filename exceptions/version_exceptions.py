""" Custom exceptions for the updatermodel class.

    Written by: Travis M. Moore
    Last edited: July 18, 2023
"""

""" EXCEPTIONS ARE NOT CURRENTLY USED """

class RequiredUpdate(Exception):
    """ New mandatory software version available """

    def __init__(self, current_v, new_v, *args):
        super().__init__(args)
        self.current_v = current_v
        self.new_v = new_v


    def __str__(self):
        message = f"updater: You are using version {self.current_v}, but " \
            f"version {self.new_v} is available."
        return message


class OptionalUpdate(Exception):
    """ New optional software version available """

    def __init__(self, current_v, new_v, *args):
        super().__init__(args)
        self.current_v = current_v
        self.new_v = new_v


    def __str__(self):
        message = f"updater: You are using version {self.current_v}, but " \
            f"version {self.new_v} is available."
        return message
