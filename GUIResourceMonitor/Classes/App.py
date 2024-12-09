import json
import customtkinter as ctk
import time
from GUIResourceMonitor.classes.Functionalities import Functionalities

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App:
    def __init__(self):
        """Initiates the App class"""

        self.root = ctk.CTk()
        self.root.title("GUI Resource Monitor")
        self.root.geometry("800x600")
        self.filename = "resources_history.json"
        self.functions = Functionalities()

        self._show_data()

    def _show_data(self):
        """Displays monitor resources statistics"""

        self.stats_frame = ctk.CTkFrame(self.root)
        self.stats_frame.pack(fill="both", expand=True, padx=10, pady=10)

        #etichete
        self.cpu_label = ctk.CTkLabel(self.stats_frame, text="CPU Usage: 0%", font=("Arial", 16))
        self.cpu_label.pack(pady=5)

        self.memory_label = ctk.CTkLabel(self.stats_frame, text="Memory Usage: 0%", font=("Arial", 16))
        self.memory_label.pack(pady=5)

        self.disk_label = ctk.CTkLabel(self.stats_frame, text="Disk Usage: 0%", font=("Arial", 16))
        self.disk_label.pack(pady=5)

        self.network_label = ctk.CTkLabel(self.stats_frame, text="Network Usage: Sent: 0 B, Received: 0 B",
                                          font=("Arial", 16))
        self.network_label.pack(pady=5)

        self.update_button = ctk.CTkButton(
            self.stats_frame, text="Update", command=self.update_stats
        )
        self.update_button.pack(pady=10)

    def update_stats(self):
        """Updates monitor resources statistics"""

        cpu_usage = self.functions.get_cpu_usage()
        memory_usage = self.functions.get_memory_usage()
        disk_usage = self.functions.get_disk_usage()
        network_usage = self.functions.get_network_usage()
        resources_time = time.ctime()

        data = {
            "timestamp": resources_time,
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "disk_usage": disk_usage,
            "network_usage": {
                "bytes_sent": network_usage["bytes_sent"],
                "bytes_received": network_usage["bytes_received"],
            },
        }
        self.save_data(data)

        self.cpu_label.configure(text=f"CPU Usage: {cpu_usage}%")
        self.memory_label.configure(text=f"Memory Usage: {memory_usage}%")
        self.disk_label.configure(text=f"Disk Usage: {disk_usage}%")
        self.network_label.configure(
            text=f"Network Usage: Sent: {network_usage['bytes_sent']} B, "
                 f"Received: {network_usage['bytes_received']} B"
        )

    def save_data(self, data):
        """Saves data to the json file

        Args:
            data (dict): data to save
        """

        try:
            with open(self.filename, "r") as f:
                history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            history = []

        history.insert(0, data)
        with open(self.filename, 'w') as f:
            json.dump(history, f, indent=4)

    def run(self):
        """
        Runs the app
        """

        self.root.mainloop()
