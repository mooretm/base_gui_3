""" Main view for BASE GUI 3
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk


#########
# BEGIN #
#########
class MainFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Assign variables
        self.parent = parent

        # Populate frame with widgets
        self.draw_widgets()


    def draw_widgets(self):
        """ Populate the main view with all widgets
        """
        ##########
        # Styles #
        ##########
        self.style = ttk.Style(self)
        self.style.configure('Heading.TLabel', font=('TkDefaultFont', 20))
        self.style.configure('Big.TLabel', font=('TkDefaultFont', 15))
        self.style.configure('Medium.TLabel', font=('TkDefaultFont', 12))
        self.style.configure('Big.TButton', font=('TKDefaultFont', 15))


        #################
        # Create frames #
        #################
        options = {'padx':20, 'pady':20}

        # Main container
        frm_main = ttk.Frame(self)
        frm_main.grid(column=5, row=5, **options)

        frm_heading = ttk.Frame(frm_main)
        frm_heading.grid(column=5, row=5)

        #frm_buttons = ttk.Frame(frm_main)
        #frm_buttons.grid(column=5, row=10, pady=(30,0))

        ttk.Separator(frm_main, orient='horizontal').grid(row=15, column=5, 
            columnspan=50, sticky='we', pady=20)

        frm_submit = ttk.Frame(frm_main)
        frm_submit.grid(row=20, column=5)

        ##################
        # Create Widgets #
        ##################
        ttk.Label(frm_heading, text="Did you hear a chirp?", 
            style='Heading.TLabel').grid(row=5, column=5)
        ttk.Label(frm_heading, text="1 = Yes", style="Medium.TLabel").grid(
            row=10, column=5)
        ttk.Label(frm_heading, text="2 = No", style="Medium.TLabel").grid(
            row=15, column=5)
        
        # ttk.Button(frm_buttons, text="Yes", command=self._on_yes, 
        #     style='Big.TButton', takefocus=0).grid(row=5, column=5, padx=10)
        #self.parent.bind('1', lambda event: self._on_yes())

        # ttk.Button(frm_buttons, text="No", command=self._on_no,
        #     style='Big.TButton', takefocus=0).grid(row=5, column=10, padx=10)
        #self.parent.bind('2', lambda event: self._on_no())

        # SEPARATOR #

        self.text_var = tk.StringVar(value="Your Response:")        
        self.label = ttk.Label(frm_submit, textvariable=self.text_var, 
            style="Big.TLabel", width=18)
        self.label.grid(row=5, column=5, pady=(0,20))

        self.btn_submit = ttk.Button(frm_submit, text="Submit", 
            style="Big.TButton", command=self._on_submit, takefocus=0, 
            state='disabled', 
            #image=self.submit_button_icon, compound=tk.LEFT
            )
        self.btn_submit.grid(row=10, column=5)


    #############
    # Functions #
    #############
    def _on_yes(self):
        self.text_var.set("Your Response: Yes")
        self.btn_submit.config(state='enabled')
        self.parent.bind('<Return>', lambda event: self._on_submit())
        self.event_generate('<<MainYes>>')


    def _on_no(self):
        self.text_var.set("Your Response: No")
        self.btn_submit.config(state='enabled')
        self.parent.bind('<Return>', lambda event: self._on_submit())
        self.event_generate('<<MainNo>>')


    def _on_submit(self):
        self.btn_submit.config(state='disabled')
        self.parent.unbind('<Return>')
        self.text_var.set("Your Response:")
        self.event_generate('<<MainSubmit>>')
