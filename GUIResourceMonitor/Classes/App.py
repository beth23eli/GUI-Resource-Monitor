import customtkinter as ctk
import psutil
import time
from GUIResourceMonitor.Classes.Functionalities import Functionalities

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("GUI Resource Monitor")
        self.root.geometry("800x600")
        self.root.attributes("-alpha", 0.6)
        self.functions = Functionalities()

        self.monitor_resources()

    def monitor_resources(self):
        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            print(f"CPU Usage: {cpu_usage}%")

            memory = psutil.virtual_memory()
            print(f"Memory Usage: {memory.percent}%")

            disk_usage = psutil.disk_usage('/')
            print(f"Disk Usage: {disk_usage.percent}%")

            network = psutil.net_io_counters()
            print(f"Bytes Sent: {network.bytes_sent}, Bytes Received: {network.bytes_recv}")

            print("-" * 40)
            time.sleep(5)

    def run(self):
        self.root.mainloop()
