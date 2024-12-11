import json
import psutil


class Functionalities:

    def get_cpu_usage(self):
        """
        Gets CPU usage
        :return: the CPU usage
        """
        cpu_usage = psutil.cpu_percent(interval=1)

        return cpu_usage

    def get_memory_usage(self):
        """
        Gets the memory usage
        :return: the memory usage
        """
        memory = psutil.virtual_memory()

        return memory.percent

    def get_disk_usage(self):
        """
        Gets the disk usage
        :return: the disk usage in percentage
        """
        disk_usage = psutil.disk_usage('/')

        return disk_usage.percent

    def get_network_usage(self):
        """
        Gets the network usage
        :return: the network usage in json format
        """
        network = psutil.net_io_counters()

        return {
            "bytes_sent": network.bytes_sent,
            "bytes_received": network.bytes_recv,
        }

    def get_most_recent_resources_statistics(self, filename):
        """
        Gets the most recent resource statistics
        :param filename: the path of the statistics file
        :return: the first record of the statistics file
        """
        try:
            with open(filename, 'r') as f:
                history = json.load(f)
                return history[0] if history else None
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def save_data(self, data, filename):
        """Saves data to the json file

        Args:
            :param data: the new data to be saved in the json file
            :param filename: the path of the statistics file
        """

        try:
            with open(filename, "r") as f:
                history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            history = []

        history.insert(0, data)
        with open(filename, 'w') as f:
            json.dump(history, f, indent=4)

    def get_all_resources_statistics(self, filename):
        """
        Gets all the resources statistics from the json file
        :param filename: the path of the statistics file
        :return: the statistics data
        """
        try:
            with open(filename, 'r') as f:
                history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            history = []

        return history