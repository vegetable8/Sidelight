import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess

class Tab1(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.set_policy_pressed = False
        self.revert_policy_pressed = False
        self.create_widgets()

    def create_widgets(self):
        # Create buttons to run Bash and PowerShell commands, each in its own row
        bash_button = tk.Button(self, text="Install Printer", command=self.run_bash_command)
        powershell_button = tk.Button(self, text="Run Windows Updates", command=self.run_powershell_command)

        # Place the Install Printer button in its own row, centered
        bash_button.grid(row=2, column=0, pady=10, padx=10, columnspan=2, sticky='nsew')

        # Place the PowerShell button in its own row, centered
        powershell_button.grid(row=1, column=0, pady=10, padx=10, columnspan=2, sticky='nsew')

        # Run DSU button in its own row, centered
        dsu_button = tk.Button(self, text="Run DSU (Dell Servers)", command=self.run_dsu_command)
        dsu_button.grid(row=3, column=0, pady=10, padx=10, columnspan=2, sticky='nsew')

        # Set Policy button in its own row at the top left
        set_policy_button = tk.Button(self, text="Set Policy Unrestricted", command=self.set_execution_policy_unrestricted)
        set_policy_button.grid(row=0, column=0, pady=10, padx=10, sticky='nw')

        # Revert Policy button on its own row at the bottom right
        revert_policy_button = tk.Button(self, text="Revert Policy", command=self.revert_execution_policy)
        revert_policy_button.grid(row=5, column=1, pady=10, padx=10, columnspan=2, sticky='se')

        # Set ShadowStorage button on its own row
        shadow_storage_button = tk.Button(self, text="Set ShadowStorage 10%", command=self.set_shadowstorage)
        shadow_storage_button.grid(row=4, column=0, pady=10, padx=10, columnspan=2, sticky='nsew')

        # Set row and column weights to make buttons expand and fill the available space
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def set_shadowstorage(self):
        powershell_command = "vssadmin resize shadowstorage /for=C: /on=C: /maxsize=10%"
        subprocess.run(["powershell", "-Command", powershell_command])
        
        # Display popup after setting ShadowStorage
        self.show_popup("Process Execution", "ShadowStorage has been set to 10%.")

    def run_bash_command(self):
        bash_command = "printui.exe /il"
        subprocess.run(["powershell", "-Command", bash_command])

    def run_powershell_command(self):
        powershell_command = "Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force;Install-Module PSWindowsUpdate -Force;Install-WindowsUpdate -AcceptAll"
        subprocess.run(["powershell", "-NoExit", "-Command", powershell_command])

    def set_execution_policy_unrestricted(self):
        self.set_policy_pressed = True  # Set the variable to True
        powershell_command = "Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser -Force"
        subprocess.run(["powershell", "-Command", powershell_command])
        
        # Display popup after setting execution policy
        self.show_popup("Process Execution", "Current execution policy has been set to Unrestricted.")

    def revert_execution_policy(self):
        self.revert_policy_pressed = True  # Set the variable to True
        self.set_policy_pressed = False  # Reset the "Set Policy" variable to False
        powershell_command = "Set-ExecutionPolicy -ExecutionPolicy Restricted -Scope CurrentUser -Force"
        subprocess.run(["powershell", "-Command", powershell_command])

        # Display popup after reverting execution policy
        self.show_popup("Process Execution", "Current execution policy has been set to Restricted.")

    def run_dsu_command(self):
        dsu_command = "dsu"
        try:
            subprocess.run(["wsl", "bash", "-c", dsu_command], check=True)
        except subprocess.CalledProcessError:
            # If the dsu command fails, show an error popup
            error_title = "Error: Install or Check Version"
            error_message = "Please double-check the Dell server version or install DSU from the toolbox if not already installed."
            messagebox.showerror(error_title, error_message)

    def show_popup(self, title, body):
        popup = tk.Toplevel(self)
        popup.title(title)

        label = tk.Label(popup, text=body)
        label.pack(padx=10, pady=10)

        ok_button = tk.Button(popup, text="Ok", command=popup.destroy)
        ok_button.pack(pady=10)      

class Tab2(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        # Add your layout and buttons for Tab 2 here
        default_button = tk.Button(self, text="Default Button", command=self.default_action)
        default_button.pack()

    def default_action(self):
        print("Default action for Tab 2")

class Tab3(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        button_texts = ["Button 1", "Button 2", "Button 3", "Button 4", "Button 5"]

        for text in button_texts:
            button = tk.Button(self, text=text, command=self.dummy_action, width=20, height=5)
            button.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def dummy_action(self):
        print("Button Clicked")

class HelpTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        help_text = (
            "Welcome to the Help tab!\n"
            "This is where you can provide helpful information or instructions."
        )
        label = tk.Label(self, text=help_text, font=("Arial", 14), justify="center")
        label.pack(pady=20)

# Function to confirm exit with a prompt
def show_custom_dialog():
    dialog = tk.Toplevel(app)
    dialog.title("Custom Dialog")

    label = tk.Label(dialog, text="Did you revert PowerShell Execution Policy?")
    label.pack(padx=10, pady=10)

    no_button = tk.Button(dialog, text="No", command=dialog.destroy)
    no_button.pack(pady=10)

def on_closing():
    if tab1.set_policy_pressed and not tab1.revert_policy_pressed:
        show_custom_dialog()
    else:
        app.destroy()

# Create the main application window
app = tk.Tk()
app.title("Tech Sidelight")

# Set the window icon for the taskbar
# app.iconbitmap("icon.ico")  # Replace with the actual path to your icon file

# Set the default size of the window
app.geometry("400x600")

# Create a notebook (tabs container)
tab_control = ttk.Notebook(app)

# Create instances of the Tab1, Tab2, Tab3, and HelpTab classes
tab1 = Tab1(master=tab_control)
tab2 = Tab2(master=tab_control)
tab3 = Tab3(master=tab_control)
help_tab = HelpTab(master=tab_control)

# Add Tabs to the notebook
tab_control.add(tab1, text="Quick Run")
tab_control.add(tab2, text="Drive Cleanup")
tab_control.add(tab3, text="Downloads")
tab_control.add(help_tab, text="Help")  # Add the Help tab

# Place the notebook in the main window
tab_control.pack(expand=1, fill="both")

# Bind the closing event to the on_closing function
app.protocol("WM_DELETE_WINDOW", on_closing)

# Start the application
app.mainloop()