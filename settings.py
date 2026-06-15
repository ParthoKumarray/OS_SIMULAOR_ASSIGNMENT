import customtkinter as ctk
from tkinter import messagebox

# UI Color configuration handles. 
# TIP: For elements to change color dynamically between Light/Dark modes,
# CustomTkinter expects a tuple format: ("Light_Mode_Hex", "Dark_Mode_Hex")
try:
    from ui_components import PANEL, ACCENT, GREEN
except ImportError:
    PANEL = ("#dbdbdb", "#2b2b2b")  # Dynamic tuple: Light gray for light mode, Dark gray for dark mode
    ACCENT = "#36a3ff"
    GREEN = "#37c65a"

class AppSettings(ctk.CTkFrame):
    """Settings page for managing OS Simulator configurations."""
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.step_delay_ms = 500
        self.extended_logging = ctk.BooleanVar(value=True)
        self.auto_resolve_deadlocks = ctk.BooleanVar(value=False)
        
        self.build_ui()

    def build_ui(self):
        
        header_frame = ctk.CTkFrame(self, fg_color=PANEL, corner_radius=10)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            header_frame, 
            text="System Settings", 
            font=("Segoe UI", 24, "bold"), 
            text_color=ACCENT
        ).pack(side="left", padx=20, pady=15)

        body_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        body_scroll.pack(fill="both", expand=True, padx=10, pady=5)

        # Personalization & Themes
        ui_card = ctk.CTkFrame(body_scroll, fg_color=PANEL, corner_radius=10)
        ui_card.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(ui_card, text="Appearance & Interface", font=("Segoe UI", 16, "bold"), text_color=ACCENT).pack(anchor="w", padx=20, pady=(15, 5))
        
        theme_row = ctk.CTkFrame(ui_card, fg_color="transparent")
        theme_row.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(theme_row, text="Color Theme Mode:", font=("Segoe UI", 14)).pack(side="left")
        
        # Dropdown options selector
        self.theme_menu = ctk.CTkOptionMenu(
            theme_row, 
            values=["Light", "Dark", "System"],
            command=self.change_theme,
            width=140
        )
        # Sets UI selector to match current system appearance state accurately
        self.theme_menu.set(ctk.get_appearance_mode())
        self.theme_menu.pack(side="right")

        #Simulator Core Configurations
        sim_card = ctk.CTkFrame(body_scroll, fg_color=PANEL, corner_radius=10)
        sim_card.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(sim_card, text="Simulator Core Engine", font=("Segoe UI", 16, "bold"), text_color=ACCENT).pack(anchor="w", padx=20, pady=(15, 5))
        
        speed_row = ctk.CTkFrame(sim_card, fg_color="transparent")
        speed_row.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(speed_row, text="Algorithm Execution Step Delay:", font=("Segoe UI", 14)).pack(side="left")
        
        self.delay_label = ctk.CTkLabel(speed_row, text=f"{self.step_delay_ms} ms", font=("Segoe UI", 13, "italic"))
        self.delay_label.pack(side="right", padx=(10, 0))
        
        self.speed_slider = ctk.CTkSlider(
            speed_row, 
            from_=100, 
            to=2000, 
            number_of_steps=19,
            command=self.update_slider_label
        )
        self.speed_slider.set(self.step_delay_ms)
        self.speed_slider.pack(side="right", fill="x", expand=True, padx=20)

        switch_row = ctk.CTkFrame(sim_card, fg_color="transparent")
        switch_row.pack(fill="x", padx=20, pady=(10, 20))
        
        self.log_switch = ctk.CTkSwitch(
            switch_row, 
            text="Enable verbose engine trace logs", 
            variable=self.extended_logging,
            font=("Segoe UI", 13)
        )
        self.log_switch.pack(side="left", padx=(0, 30))

        self.resolve_switch = ctk.CTkSwitch(
            switch_row, 
            text="Auto-abort processes during Deadlock detection", 
            variable=self.auto_resolve_deadlocks,
            font=("Segoe UI", 13)
        )
        self.resolve_switch.pack(side="left")

        #Action Footer
        footer_frame = ctk.CTkFrame(self, fg_color=PANEL, corner_radius=10)
        footer_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        ctk.CTkButton(
            footer_frame, 
            text="Save Settings", 
            command=self.save_settings, 
            fg_color=GREEN, 
            hover_color="#2da04a",
            width=150,
            font=("Segoe UI", 14, "bold")
        ).pack(side="right", padx=20, pady=15)
        
        ctk.CTkButton(
            footer_frame, 
            text="Reset Defaults", 
            command=self.reset_defaults, 
            fg_color="#5a6268", 
            hover_color="#4e555b",
            width=120
        ).pack(side="left", padx=20, pady=15)

    def change_theme(self, choice):
        """Changes app appearance instantly runtime."""
        ctk.set_appearance_mode(choice)

    def update_slider_label(self, value):
        self.step_delay_ms = int(value)
        self.delay_label.configure(text=f"{self.step_delay_ms} ms")

    def save_settings(self):
        config_summary = (
            f"Theme: {self.theme_menu.get()}\n"
            f"Step Delay: {self.step_delay_ms}ms\n"
            f"Verbose Logs: {self.extended_logging.get()}\n"
            f"Auto-Resolve Deadlocks: {self.auto_resolve_deadlocks.get()}"
        )
        messagebox.showinfo("Settings Saved", f"Configurations successfully updated:\n\n{config_summary}")

    def reset_defaults(self):
        """Resets all interface values to defaults."""
        self.theme_menu.set("Light")
        ctk.set_appearance_mode("Light")
        
        self.step_delay_ms = 500
        self.speed_slider.set(500)
        self.delay_label.configure(text="500 ms")
        
        self.extended_logging.set(True)
        self.auto_resolve_deadlocks.set(False)