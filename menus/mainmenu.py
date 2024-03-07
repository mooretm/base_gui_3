""" Main menu class
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import messagebox

# Import custom modules
from app_assets import images


#########
# Begin #
#########
class MainMenu(tk.Menu):
    """ Main Menu
    """
    # Find parent window and tell it to 
    # generate a callback sequence
    def _event(self, sequence):
        def callback(*_):
            root = self.master.winfo_toplevel()
            root.event_generate(sequence)
        return callback


    def _bind_accelerators(self):
        """ Bind shortcut keys to event triggers.
        """
        #self.bind_all('<space>', self._event('<<PlaybackStart>>'))
        #self.bind_all('<Control-c>', self._event('<<PlaybackStop>>'))
        self.bind_all('<Control-q>', self._event('<<FileQuit>>'))


    def _create_icons(self):
        """ Create a dictionary of icons. Necessary because
            PhotoImage objects cannot be created until an 
            instance of Tk has been created.
        """
        self.icons = {
            # File menu
            'file_settings': tk.PhotoImage(file=images.SETTINGS_ICON),
            'file_start': tk.PhotoImage(file=images.PLAY_ICON),

            # Tools menu
            'tools_audio': tk.PhotoImage(file=images.AUDIO_ICON),
            'tools_calibration': tk.PhotoImage(file=images.CALIBRATION_ICON),

            # Help menu
            'help_about': tk.PhotoImage(file=images.ABOUT_ICON),
            'help_help': tk.PhotoImage(file=images.HELP_ICON),
            'help_changelog': tk.PhotoImage(file=images.CHANGELOG_ICON)
        }


    def __init__(self, parent, _app_info, **kwargs):
        super().__init__(parent, **kwargs)

        # Assign variables
        self._app_info = _app_info

        # Create icons
        self._create_icons()

        #############
        # File Menu #
        #############
        self.file_menu = tk.Menu(self, tearoff=False)
        self.file_menu.add_command(
            label="Session Info...",
            command=self._event('<<FileSession>>'),
            image=self.icons['file_settings'],
            compound=tk.LEFT
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label="Start Task",
            command=self._event('<<FileStart>>'),
            image=self.icons['file_start'],
            compound=tk.LEFT
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label="Quit",
            command=self._event('<<FileQuit>>'),
            accelerator='Ctrl+Q',
        )
        self.add_cascade(label='File', menu=self.file_menu)


        ############## 
        # Tools menu #
        ##############
        tools_menu = tk.Menu(self, tearoff=False)
        tools_menu.add_command(
            label='Audio Settings...',
            command=self._event('<<ToolsAudioSettings>>'),
            image=self.icons['tools_audio'],
            compound=tk.LEFT,
        )
        tools_menu.add_separator()
        tools_menu.add_command(
            label='Calibration...',
            command=self._event('<<ToolsCalibration>>'),
            image=self.icons['tools_calibration'],
            compound=tk.LEFT,
        )
        # Add Tools menu to the menubar
        self.add_cascade(label="Tools", menu=tools_menu)


        #################
        # Playback Menu #
        #################
        # playback_menu = tk.Menu(self, tearoff=False)
        # playback_menu.add_command(
        #     label="Start Audio",
        #     command=self._event('<<PlaybackStart>>'),
        #     accelerator='Spacebar'
        # )
        # playback_menu.add_separator()
        # playback_menu.add_command(
        #     label="Stop Audio",
        #     command=self._event('<<PlaybackStop>>'),
        #     accelerator='Ctrl+C'
        # )
        # self.add_cascade(label='Playback', menu=playback_menu)


        #############
        # Help Menu #
        #############
        help_menu = tk.Menu(self, tearoff=False)
        help_menu.add_command(
            label='About...',
            command=self.show_about,
            image=self.icons['help_about'],
            compound=tk.LEFT,
        )
        help_menu.add_command(
            label='README...',
            command=self._event('<<HelpREADME>>'),
            image=self.icons['help_help'],
            compound=tk.LEFT,
        )
        help_menu.add_command(
            label="Change Log...",
            command=self._event('<<HelpChangelog>>'),
            image=self.icons['help_changelog'],
            compound=tk.LEFT,
        )
        # Add help menu to the menubar
        self.add_cascade(label="Help", menu=help_menu)


        #####################
        # Bind accelerators #
        #####################
        self._bind_accelerators()


    ##################
    # Menu Functions #
    ##################
    # HELP menu
    def show_about(self):
        """ Show the about dialog """
        about_message = self._app_info['name']
        about_detail = (
            'Written by: Travis M. Moore\n' +
            'Version {}\n'.format(self._app_info['version']) +
            'Created: July 14, 2023\n'
            'Last edited: {}'.format(self._app_info['last_edited'])
        )
        messagebox.showinfo(
            title='About',
            message=about_message,
            detail=about_detail
        )
