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
        :return: the disk usage
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
