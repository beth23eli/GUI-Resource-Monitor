import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("GUI Resource Monitor")
        self.root.geometry("800x600")
        self.root.attributes("-alpha", 0.6)

    def run(self):
        self.root.mainloop()