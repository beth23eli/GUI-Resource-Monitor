import os

import customtkinter as ctk
import time
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from GUIResourceMonitor.classes.Functionalities import Functionalities

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")


class App:
    def __init__(self):
        """Initiates the App class"""

        self.root = ctk.CTk()
        self.root.title("GUI Resource Monitor")
        self.root.geometry("800x700")
        self.filename = "resources_history.json"
        self.functions = Functionalities()

        self.resource_stats_frame = None
        self.graph_frame = None
        self.statistics_history_frame = None
        self.data_type = "cpu_usage" # default resource when first opening the app
        self.resource_label = None
        self.graph_info = []

        self._show_data()
        self._set_graph()
        self._set_statistics_history_area()
        self.update_statistics()

    def _show_data(self):
        """Displays monitor resources statistics"""

        self.resource_stats_frame = ctk.CTkFrame(self.root, fg_color="#c0d2fa")
        self.resource_stats_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.resource_label = ctk.CTkLabel(self.resource_stats_frame, text="CPU Usage: 0%", font=("Arial", 16, "bold"))
        self.resource_label.pack(pady=5)

        buttons = ctk.CTkFrame(self.root)
        buttons.pack(pady=10)

        cpu_button = ctk.CTkButton(buttons, text="CPU Usage", fg_color="#184ecc", command=lambda: self._change_data("cpu_usage"))
        cpu_button.pack(side="left", padx=5)

        memory_button = ctk.CTkButton(buttons, text="Memory Usage", fg_color="#184ecc",
                                      command=lambda: self._change_data("memory_usage"))
        memory_button.pack(side="left", padx=5)

        disk_button = ctk.CTkButton(buttons, text="Disk Usage", fg_color="#184ecc", command=lambda: self._change_data("disk_usage"))
        disk_button.pack(side="left", padx=5)

        network_button = ctk.CTkButton(buttons, text="Network Usage", fg_color="#184ecc",
                                       command=lambda: self._change_data("network_usage"))
        network_button.pack(side="left", padx=5)

    def _change_data(self, data_type):
        """Changes the data type for the graph and label accordingly the selected resource"""
        self.data_type = data_type
        self.graph_info.clear()
        self.resource_label.configure(text=f"{data_type.replace('_', ' ').title()}: 0%")
        self.ax.set_title(data_type.replace('_', ' ').title())
        self.ax.set_ylabel("% Utilization" if data_type != "network_usage" else "Bytes")

    def _set_graph(self):
        """Sets the graph frame for a resource statistics"""
        self.graph_frame = ctk.CTkFrame(self.root)
        self.graph_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        self.download_plot_ways = ctk.CTkOptionMenu(
            self.graph_frame,
            values=["jpeg", "pdf"],
            command=self._download_graph,
            height=10
        )
        self.download_plot_ways.set("Download plot")
        self.download_plot_ways.pack(side="right", pady=20)

        style.use('seaborn-v0_8-pastel')
        self.fig, self.ax = plt.subplots()
        self.ax.set_title("CPU")
        self.ax.set_ylabel("% Utilization")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.ani = FuncAnimation(self.fig, func=self._animate, interval=1000, cache_frame_data=False)

    def _download_graph(self, option):
        """
        Downloads the graph with the chosen extension
        :param option: the chosen extension
        """
        d_path = os.path.join(os.path.expanduser("~"), "Downloads")

        if option == "jpeg":
            plt.savefig(os.path.join(d_path, "resources.jpeg"))
        else:
            plt.savefig(os.path.join(d_path, "resources.jpeg"))


    def _animate(self, i):
        """Animates the graph by updating it live"""
        record = self.functions.get_most_recent_resources_statistics(self.filename)
        if record:
            value = record[self.data_type] if self.data_type != "network_usage" else record["network_usage"][
                "bytes_sent"]
            self.graph_info.append(value)

            self.ax.clear()
            self.ax.plot(self.graph_info, label=f"{self.data_type.replace('_', ' ').title()}")
            self.ax.legend()
            self.ax.set_title(self.data_type.replace('_', ' ').title())
            self.ax.set_ylabel("% Utilization" if self.data_type != "network_usage" else "Bytes")
            self.fig.tight_layout()

            return self.fig, self.ax

    def _set_statistics_history_area(self):
        """Sets the scrollable area for resources statistics history."""
        history_area = ctk.CTkFrame(self.root)
        history_area.pack(side="bottom", fill="x", padx=10, pady=(10, 5))

        title = ctk.CTkLabel(history_area, text="Resources Statistics History", font=("Arial", 16))
        title.pack(pady=5)

        self.statistics_history_frame = ctk.CTkScrollableFrame(history_area, width=600, height=600)
        self.statistics_history_frame.pack(side="left", fill="x", padx=10, pady=(10, 5))

        update_button = ctk.CTkButton(history_area, text="Update history", hover_color="#7440c2", command=self._update_statistics_history_area)
        update_button.pack(side="right", padx=10, pady=20)

        self._update_statistics_history_area()

    def _update_statistics_history_area(self):
        for old_content in self.statistics_history_frame.winfo_children():
            old_content.destroy()

        statistics_history = self.functions.get_all_resources_statistics(self.filename)
        for stats_record in statistics_history:
            record_time = stats_record.get("timestamp", "-")
            cpu = stats_record.get("cpu_usage", "-")
            memory = stats_record.get("memory_usage", "-")
            disk = stats_record.get("disk_usage", "-")
            bytes_sent = stats_record.get("network_usage", {}).get("bytes_sent", "-")
            bytes_received = stats_record.get("network_usage", {}).get("bytes_received", "-")

            label_text = (
                f"Time: {record_time}\n"
                f"CPU Usage: {cpu}% , Memory Usage: {memory}% , Disk Usage: {disk}%\n"
                f"Network Usage -> Sent: {bytes_sent} Bytes , Received: {bytes_received} Bytes\n"
                "**********************************************************************************"
            )
            label = ctk.CTkLabel(self.statistics_history_frame, text=label_text, anchor="w", justify="left", font=("Arial", 12))
            label.pack(fill="x", padx=5, pady=2)

    def update_statistics(self):
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
        self.functions.save_data(data, self.filename)

        if self.data_type == "cpu_usage":
            self.resource_label.configure(text=f"CPU Usage: {cpu_usage}%")
        elif self.data_type == "memory_usage":
            self.resource_label.configure(text=f"Memory Usage: {memory_usage}%")
        elif self.data_type == "disk_usage":
            self.resource_label.configure(text=f"Disk Usage: {disk_usage}%")
        elif self.data_type == "network_usage":
            self.resource_label.configure(
                text=f"Network Usage -> Sent: {network_usage['bytes_sent']} Bytes, "
                     f"Received: {network_usage['bytes_received']} Bytes"
            )
        self.root.after(1000, self.update_statistics)

    def run(self):
        """
        Runs the app
        """

        self.root.mainloop()
