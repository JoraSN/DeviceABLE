import tkinter as tk
import pyautogui


class OnScreenKeyboard(tk.Tk):
    def __init__(self):
        super().__init__()
        # Configure the root window
        self.title("On-Screen Keyboard")
        self.geometry("1035x350")
        # Make the window always appear on top
        self.attributes("-topmost", True)
        self.bind("<Motion>", self.check_hover)  # Track mouse movements
        # Define the keyboard layout
        self.lowercase_keys = [
            ['`', '1', '2', '3', '4', '5', '6', '7',
                '8', '9', '0', '-', '=', 'Back\nSpace'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'Enter'],
            ['Tab', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'Shift'],
            ['Ctrl', 'Alt', 'Win', 'Space', '↑', '←', '↓', '→']
        ]
        self.uppercase_keys = [
            ['~', '!', '@', '#', '$', '%', '^', '&',
                '*', '(', ')', '_', '+', 'Back\nSpace'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '|'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"', 'Enter'],
            ['Tab', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?', 'Shift'],
            ['Ctrl', 'Alt', 'Win', 'Space', '↑', '←', '↓', '→']
        ]
        self.current_keys = self.lowercase_keys
        # Create and place the buttons
        self.buttons = []
        for row, key_row in enumerate(self.current_keys):
            button_row = []
            for col, key in enumerate(key_row):
                button = tk.Button(self, text=key, width=5,
                                   height=2, font=('Arial', 10, 'bold'))
                button.grid(row=row, column=col, padx=2, pady=2)
                button.bind("<Button-1>", lambda event,
                            k=key: self.send_key(k))
                button.bind("<ButtonRelease-1>", lambda event,
                            k=key: self.release_key(k))
                button_row.append(button)
            self.buttons.append(button_row)
        # Initialize the hover timer
        self.hover_timer = None
        self.hover_key = None
        # Initialize toggle key states
        self.shift_pressed = False
        self.ctrl_pressed = False
        self.alt_pressed = False
        self.win_pressed = False

    def check_hover(self, event):
        # Check if the mouse is hovering over a key
        for row, key_row in enumerate(self.current_keys):
            for col, key in enumerate(key_row):
                button = self.buttons[row][col]
                if button.winfo_containing(event.x_root, event.y_root) == button:
                    if self.hover_key != key:
                        self.hover_key = key
                        if self.hover_timer is not None:
                            self.after_cancel(self.hover_timer)
                        self.hover_timer = self.after(
                            2000, self.send_hover_key)
                else:
                    if self.hover_timer is not None and self.hover_key == key:
                        self.hover_key = None
                        self.after_cancel(self.hover_timer)
                        self.hover_timer = None

    def send_hover_key(self):
        # Send the key when it's hovered for 2 seconds and continue sending if key is held longer
        if self.hover_key:
            if self.hover_key == 'Shift':
                self.toggle_shift()
            elif self.hover_key == 'Ctrl':
                self.toggle_ctrl()
            elif self.hover_key == 'Alt':
                self.toggle_alt()
            elif self.hover_key == 'Win':
                self.toggle_win()
            elif self.hover_key == 'Back\nSpace':
                pyautogui.press("backspace")
                # Continue sending Backspace if held longer
                self.hover_timer = self.after(2000, self.send_hover_key)
            elif self.hover_key == 'Space':
                pyautogui.press("space")
                # Continue sending Space if held longer
                self.hover_timer = self.after(2000, self.send_hover_key)
            elif self.hover_key == 'Enter':
                pyautogui.press("enter")
                # Continue sending Enter if held longer
                self.hover_timer = self.after(2000, self.send_hover_key)
            elif self.hover_key == 'Tab':
                pyautogui.press("tab")
                # Continue sending Tab if held longer
                self.hover_timer = self.after(2000, self.send_hover_key)
            elif self.hover_key == '↑':
                pyautogui.press("up")
                self.hover_timer = self.after(2000, self.send_hover_key)
            elif self.hover_key == '←':
                pyautogui.press("left")
                self.hover_timer = self.after(2000, self.send_hover_key)
            elif self.hover_key == '↓':
                pyautogui.press("down")
                self.hover_timer = self.after(2000, self.send_hover_key)
            elif self.hover_key == '→':
                pyautogui.press("right")
                self.hover_timer = self.after(2000, self.send_hover_key)
            else:
                pyautogui.typewrite(self.hover_key)
                self.hover_timer = self.after(2000, self.send_hover_key)

    def send_key(self, key):
        # Send the key immediately when it's clicked
        if key == "Back\nSpace":
            pyautogui.press("backspace")
        elif key == "Shift":
            self.toggle_shift()
        elif key == "Ctrl":
            self.toggle_ctrl()
        elif key == "Alt":
            self.toggle_alt()
        elif key == "Win":
            self.toggle_win()
        elif key == "Enter":
            pyautogui.press("enter")
        elif key == 'Tab':
            pyautogui.press("tab")
        elif key == '↑':
            pyautogui.press("up")
        elif key == '←':
            pyautogui.press("left")
        elif key == '↓':
            pyautogui.press("down")
        elif key == '→':
            pyautogui.press("right")
        elif key == 'Space':
            pyautogui.press("space")
        else:
            pyautogui.typewrite(key)

    def release_key(self, key):
        # Release the Shift key when it's released
        if key == "Shift":
            self.toggle_shift()
        elif key == "Ctrl":
            self.toggle_ctrl()
        elif key == "Alt":
            self.toggle_alt()
        elif key == "Win":
            self.toggle_win()

    def toggle_shift(self):
        # Toggle between lowercase and uppercase keyboard layout
        if self.current_keys == self.lowercase_keys:
            self.current_keys = self.uppercase_keys
        else:
            self.current_keys = self.lowercase_keys
        # Update the button labels
        for row, key_row in enumerate(self.current_keys):
            for col, key in enumerate(key_row):
                self.buttons[row][col].configure(text=key)

    def toggle_ctrl(self):
        # Toggle the Ctrl key
        self.ctrl_pressed = not self.ctrl_pressed
        # Update the button color
        for row, key_row in enumerate(self.current_keys):
            for col, key in enumerate(key_row):
                button = self.buttons[row][col]
                if key == 'Ctrl':
                    button.configure(
                        bg='red' if self.ctrl_pressed else 'SystemButtonFace', activebackground='red')
        # Press or release the Ctrl key
        if self.ctrl_pressed:
            pyautogui.keyDown('ctrl')
        else:
            pyautogui.keyUp('ctrl')

    def toggle_alt(self):
        # Toggle the Alt key
        self.alt_pressed = not self.alt_pressed
        # Update the button color
        for row, key_row in enumerate(self.current_keys):
            for col, key in enumerate(key_row):
                button = self.buttons[row][col]
                if key == 'Alt':
                    button.configure(
                        bg='red' if self.alt_pressed else 'SystemButtonFace', activebackground='red')
        # Press or release the Alt key
        if self.alt_pressed:
            pyautogui.keyDown('alt')
        else:
            pyautogui.keyUp('alt')

    def toggle_win(self):
        # Toggle the Win key
        self.win_pressed = not self.win_pressed
        # Update the button color
        for row, key_row in enumerate(self.current_keys):
            for col, key in enumerate(key_row):
                button = self.buttons[row][col]
                if key == 'Win':
                    button.configure(
                        bg='red' if self.win_pressed else 'SystemButtonFace', activebackground='red')
        # Press or release the Win key
        if self.win_pressed:
            pyautogui.keyDown('winleft')
        else:
            pyautogui.keyUp('winleft')


if __name__ == "__main__":
    keyboard = OnScreenKeyboard()
    keyboard.mainloop()
