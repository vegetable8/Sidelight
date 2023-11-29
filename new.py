import tkinter as tk
from tkinter import ttk
import platform
import socket
import subprocess
import re
import requests
from requests import ConnectionError

def get_system_info():
    system_info = {}

    # Get basic system information
    system_info['System'] = platform.system()
    system_info['Node Name'] = platform.node()
    system_info['Version'] = platform.version()
    system_info['Machine'] = platform.machine()
    system_info['Processor'] = platform.processor()

    # Get RAM information
    try:
        installed_ram, used_ram = get_ram_info()
        system_info['Installed RAM'] = installed_ram
        system_info['Free RAM GB'] = used_ram
        system_info['Pct Free'] = round((int(used_ram) / int(installed_ram)) * 100, 2)
    except TypeError as e:
        print(f"Error getting RAM information: {e}")
        system_info['Installed RAM'] = 'N/A'
        system_info['Free RAM GB'] = 'N/A'

    # Get network information
    system_info['Hostname'] = platform.node()

    try:
        response = requests.get('https://icanhazip.com')
        if response.status_code == 200:
            system_info['Public IP Address'] = response.text
        else:
            print('Unable to get IP Address')
        #system_info['IP Address'] = socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        system_info['Public IP Address'] = 'N/A'

    return system_info

def get_ram_info():
    """
    This function retrieves the total and used RAM information on a Windows machine.

    It uses PowerShell commands to fetch the RAM details. The total RAM is obtained using the Win32_PhysicalMemory class,
    and the used RAM is obtained using the Memory\Available MBytes counter.

    The function returns the total and used RAM in GB as a tuple of strings. If there is an error in fetching the RAM information,
    it prints the error message and returns 'N/A', 'N/A'.

    Returns:
        tuple: A tuple containing total RAM and used RAM in GB as strings. For example, ('8.00 GB', '4 GB').
    """
    try:
        # Run PowerShell commands to get RAM information
        
        total_ram_command = 'Get-WmiObject Win32_PhysicalMemory | Measure-Object Capacity -Sum | Select-Object -ExpandProperty Sum'
        used_ram_command = 'Get-Counter "\Memory\Available MBytes" | Select-Object -ExpandProperty CounterSamples | Select-Object -ExpandProperty CookedValue'
        
        ram_stats_cmd = '$os = Get-WmiObject -Class Win32_OperatingSystem; "$([math]::Round($os.TotalVisibleMemorySize / 1MB)), $([math]::Round($os.FreePhysicalMemory / 1MB))"'

        
        ram_stats = subprocess.run(['powershell', '-Command', ram_stats_cmd], capture_output=True, text=True, check=True)

        total_ram_result = subprocess.run(['powershell', '-Command', total_ram_command], capture_output=True, text=True, check=True)
        used_ram_result = subprocess.run(['powershell', '-Command', used_ram_command], capture_output=True, text=True, check=True)

        print(ram_stats.stdout)
        total_ram_gb_str = ram_stats.stdout.split(',')
        
        return total_ram_gb_str
            
        # Extract only the numeric values
        total_ram_bytes_str = re.search(r'\d+', total_ram_result.stdout)
        used_ram_mb_str = re.search(r'\d+', used_ram_result.stdout)

        if total_ram_gb_str is not None:
            #total_ram_bytes = int(total_ram_bytes_str.group())
            #used_ram_mb = int(used_ram_mb_str.group())
            #total_ram_gb = total_ram_bytes / (1024 ** 3)
            
            # Convert used RAM to the nearest gigabyte
            used_ram_gb = round(used_ram_mb / 1024)

            return f"{total_ram_gb:.2f} GB", f"{used_ram_gb} GB"
        else:
            raise ValueError(f"Failed to extract numeric values from PowerShell output: {total_ram_result.stdout}, {used_ram_result.stdout}")
    except Exception as e:
        print(f"Error getting RAM information on Windows: {e}")
        return 'N/A', 'N/A'

class RemoteSpecsGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Remote System Specs")
        self.master.geometry("600x400")

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=1, fill="both")

        self.create_tab("System Info")
        self.create_tab("Execute Command")

    def create_tab(self, tab_name):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=tab_name)
        
        if tab_name == "System Info":
            self.create_system_info_tab(tab)
        elif tab_name == "Execute Command":
            self.create_execute_command_tab(tab)

    def create_system_info_tab(self, tab):
        system_info_text = tk.Text(tab, wrap="word", width=40, height=12)
        system_info_text.pack(padx=10, pady=10)

        def get_and_display_system_info():
            remote_system_info = get_system_info()
            info_str = "Remote System Information:\n"
            for key, value in remote_system_info.items():
                info_str += f"{key}: {value}\n"
            system_info_text.delete(1.0, tk.END)
            system_info_text.insert(tk.END, info_str)

        refresh_button = tk.Button(tab, text="Refresh", command=get_and_display_system_info)
        refresh_button.pack(pady=10)

    def create_execute_command_tab(self, tab):
        pass  # Placeholder for the Execute Command tab

if __name__ == "__main__":
    root = tk.Tk()
    app = RemoteSpecsGUI(root)
    root.mainloop()
