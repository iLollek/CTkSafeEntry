import customtkinter as ctk

class CTkSafeEditBox(ctk.CTkFrame):
    """
    A CustomTkinter Widget for Displaying a CTkEntry alongside a CTkButton that Enables or Disables User Input.
    Author: Loris Dante (iLollek)
    """

    def __init__(self, master=None,
                 edit_disabled_text="A",
                 edit_enabled_text="M",
                 edit_disabled_color="red",
                 edit_enabled_color="green",
                 max_characters=None,
                 on_disable_edit_command=None,
                 on_enable_edit_command=None,
                 **kwargs):
        """
        Initializes the CTkSafeEditBox Widget.
        
        :param master: Parent widget
        :param edit_disabled_text: The Text that the CTkButton should display while editing of the CTkEntry is disabled
        :param edit_enabled_text: The Text that the CTkButton should display while editing of the CTkEntry is enabled
        :param edit_disabled_color: The Color of the CTkButton while editing of the CTkEntry is disabled
        :param edit_enabled_color: The Color of the CTkButton while editing of the CTkEntry is enabled
        :param max_characters: The maximum amount of Characters that the CTkEntry is allowed to hold
        :param on_disable_edit_command: A Command (Callback) that will be executed when the Editing switches from Enabled to Disabled
        :param on_enable_edit_command: A Command (Callback) that will be executed when the Editing switches from Disabled to Enabled

        Additionally, any Arguments for CTkFrame can be passed as kwargs
        If you want to manually change properties of the CTkButton or CTkEntry, you can access them via `self.EditButton` & `self.Entry`
        """

        super().__init__(master, **kwargs)

        self.can_edit = False

        self.edit_disabled_text = edit_disabled_text
        self.edit_enabled_text = edit_enabled_text

        self.edit_disabled_color = edit_disabled_color
        self.edit_enabled_color = edit_enabled_color

        self.on_disable_edit_command = on_disable_edit_command
        self.on_enable_edit_command = on_enable_edit_command

        self.max_characters = max_characters

        self.entry_var = ctk.StringVar()
        if self.max_characters != None and type(self.max_characters) == int:
            self.entry_var.trace_add("write", self._limit_characters)

        # Define consistent height (can be changed dynamically if needed)
        self.widget_height = 28  # fixed height for both widgets

        self.grid_columnconfigure(0, weight=1)  # Entry expands
        self.grid_columnconfigure(1, weight=0)  # Button fixed

        self.Entry = ctk.CTkEntry(self, height=self.widget_height, state="disabled", textvariable=self.entry_var)
        self.Entry.grid(row=0, column=0, sticky="nsew")

        self.EditButton = ctk.CTkButton(self,
                                        width=self.widget_height,  # Square: width == height
                                        height=self.widget_height,
                                        fg_color=self.edit_disabled_color,
                                        hover_color=self._get_hover_color(self.edit_disabled_color),
                                        text=self.edit_disabled_text,
                                        command=self.toggle_edit_mode)
        self.EditButton.grid(row=0, column=1, pady=0)

    def toggle_edit_mode(self):
        """ Toggles between enabled/disabled entry """
        self.can_edit = not self.can_edit

        if self.can_edit:
            self.Entry.configure(state="normal")
            self.EditButton.configure(fg_color=self.edit_enabled_color,
                                    hover_color=self._get_hover_color(self.edit_enabled_color),
                                    text=self.edit_enabled_text)

            # Text markieren wie bei Strg+A
            self.Entry.focus_set()
            self.Entry.select_range(0, 'end')

            if self.on_enable_edit_command:
                self.on_enable_edit_command()
        else:
            self.Entry.configure(state="disabled")
            self.EditButton.configure(fg_color=self.edit_disabled_color,
                                    hover_color=self._get_hover_color(self.edit_disabled_color),
                                    text=self.edit_disabled_text)
            if self.on_disable_edit_command:
                self.on_disable_edit_command()

    def _limit_characters(self, *args):
        if len(self.entry_var.get()) >= self.max_characters:
            self.entry_var.set(self.entry_var.get()[:self.max_characters])

    def _get_hover_color(self, color_name_or_code: str) -> str:
        """
        Returns a slightly darker "hover color".

        :param color_name_or_code: Either a named color (e.g., "red") or an HTML color code like "#RRGGBB".
        :type color_name_or_code: str
        :return: A slightly darker tone of the color.
        :rtype: str
        :raises ValueError: If the color input is invalid.
        """

        # Try resolving via ThemeManager (for customtkinter theme colors)
        try:
            color_code = ctk.ThemeManager.theme["CTkButton"]["fg_color"][color_name_or_code]
            if isinstance(color_code, list):
                # Use default color from theme (light/dark fallback)
                color_code = color_code[0]
            if not isinstance(color_code, str) or not color_code.startswith("#"):
                raise ValueError
        except Exception:
            color_code = color_name_or_code

        # Resolve named tkinter colors to RGB
        if not color_code.startswith("#"):
            try:
                # Convert named tkinter color to RGB and normalize to 0–255
                r, g, b = [int(v / 256) for v in self.master.winfo_rgb(color_code)]
            except Exception:
                raise ValueError(f"Unknown or invalid color name: '{color_code}'")
        else:
            if len(color_code) != 7:
                raise ValueError("Color code must be in format '#RRGGBB'.")
            try:
                r = int(color_code[1:3], 16)
                g = int(color_code[3:5], 16)
                b = int(color_code[5:7], 16)
            except ValueError:
                raise ValueError("Invalid hex values in color code.")

        # Apply darkening factor (e.g. 15%)
        factor = 0.85
        r = max(0, int(r * factor))
        g = max(0, int(g * factor))
        b = max(0, int(b * factor))

        # Return as HTML hex code
        return "#{:02x}{:02x}{:02x}".format(r, g, b)


    


if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("400x400")

    for i in range(1, 10):
        my_button = CTkSafeEditBox(app, max_characters=8)
        my_button.pack()

    app.mainloop()