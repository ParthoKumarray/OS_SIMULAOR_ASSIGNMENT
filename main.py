import argparse
import os
import time
import tkinter as tk
from PIL import ImageGrab

from ui_components import configure_styles, clear_frame, BG, SIDEBAR, SIDEBAR_HOVER, ACCENT, FONT_SMALL
from Dashboard1 import MyDashboard
from cpu_scheduler import CPUScheduler
from page_replacement import MemoryManagement
from process_sync import ProcessSyncApp
from bankers_algorithm import DeadlockHandling
from settings import AppSettings
from about import AboutSection

import customtkinter as ctk  

class MiniOSApp:
    def __init__(self, root, initial_page="Dashboard"):
        self.root = root
        self.root.title("Mini Operating System Simulator")
        self.root.geometry("1280x720")
        self.root.minsize(1100, 650)
        self.root.configure(fg_color=BG) 
        configure_styles(root)

        # Setup sidebar and main content areas
        self.sidebar = ctk.CTkFrame(root, fg_color=SIDEBAR, width=195, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        self.content = ctk.CTkFrame(root, fg_color=BG, corner_radius=0)
        self.content.pack(side="right", fill="both", expand=True)

        self.nav_buttons = {}
        self.pages = {
            "Dashboard": MyDashboard,
            "CPU Scheduling": CPUScheduler,
            "Memory Management": MemoryManagement,
            "Process Synchronization": ProcessSyncApp,
            "Deadlock Handling": DeadlockHandling,
            "Settings": AppSettings,
            "About": AboutSection,
        }
        self.current_page = initial_page
        self.build_sidebar()
        self.navigate(initial_page)
        root.app = self  

        self.build_global_theme_switch()

    def build_global_theme_switch(self):
        # Create dark mode toggle switch
        self.theme_switch = ctk.CTkSwitch(
            self.root, 
            text="Dark Mode", 
            command=self.execute_theme_toggle,
            font=("Segoe UI", 11, "bold"),
            progress_color="#36a3ff" 
        )
        
        # Position switch in the top-right corner
        self.theme_switch.place(relx=1.0, rely=0.0, anchor="ne", x=-25, y=20)
        
        # Sync switch with current theme
        if ctk.get_appearance_mode() == "Dark":
            self.theme_switch.select()
        else:
            self.theme_switch.deselect()

    def execute_theme_toggle(self):
        # Handle live theme switching
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

    def build_sidebar(self):
        # Sidebar title
        header = tk.Frame(self.sidebar, bg=SIDEBAR, height=56)
        header.pack(fill="x")
        tk.Label(header, text="▣", bg=SIDEBAR, fg="#36a3ff", font=("Segoe UI", 18)).pack(side="left", padx=(14, 8), pady=12)
        tk.Label(header, text="Mini OS Simulator", bg=SIDEBAR, fg="white",
                 font=("Segoe UI Semibold", 11)).pack(side="left", pady=15)

        # Generate navigation buttons
        icons = ["⌂", "▧", "▤", "⌘", "⚠", "▱", "⚙", "ⓘ"]
        for (name, _), icon in zip(self.pages.items(), icons):
            b = tk.Button(self.sidebar, text=f"  {icon}   {name}", anchor="w",
                          bg=SIDEBAR, fg="#d7e0eb", activebackground=SIDEBAR_HOVER,
                          activeforeground="white", relief="flat", bd=0,
                          font=("Segoe UI", 9), padx=10, pady=10,
                          command=lambda n=name: self.navigate(n), cursor="hand2")
            b.pack(fill="x", padx=6, pady=1)
            self.nav_buttons[name] = b

        # Bottom status indicator
        spacer = tk.Frame(self.sidebar, bg=SIDEBAR)
        spacer.pack(fill="both", expand=True)
        status = tk.Frame(self.sidebar, bg=SIDEBAR)
        status.pack(fill="x", padx=15, pady=14)
        tk.Label(status, text="●", bg=SIDEBAR, fg="#37c65a", font=("Segoe UI", 12)).pack(side="left")
        tk.Label(status, text="System Ready", bg=SIDEBAR, fg="#e7edf4", font=FONT_SMALL).pack(side="left", padx=8)

    def navigate(self, name):
        # Update button highlights and swap active page
        self.current_page = name
        for key, b in self.nav_buttons.items():
            b.configure(bg=ACCENT if key == name else SIDEBAR,
                        fg="white" if key == name else "#d7e0eb")
        clear_frame(self.content)
        
        page_class = self.pages[name]
        page_instance = page_class(self.content)
        page_instance.pack(fill="both", expand=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--page", default="Dashboard")
    parser.add_argument("--screenshot", default="")
    args = parser.parse_args()
    
    ctk.set_appearance_mode("Light") 
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk() 
    app = MiniOSApp(root, initial_page=args.page)

    # Handle automated screenshot flag if provided
    if args.screenshot:
        def capture():
            root.update_idletasks()
            root.update()
            time.sleep(0.5)
            x = root.winfo_rootx()
            y = root.winfo_rooty()
            w = root.winfo_width()
            h = root.winfo_height()
            img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
            os.makedirs(os.path.dirname(args.screenshot) or ".", exist_ok=True)
            img.save(args.screenshot)
            root.destroy()
        root.after(1200, capture)
    root.mainloop()

if __name__ == "__main__":
    main()