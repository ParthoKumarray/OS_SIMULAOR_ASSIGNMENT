import sys
import platform
import tkinter as tk         # Added to safely check backend TkVersion
import customtkinter as ctk

# Safely import the global application styles from your UI components
try:
    from ui_components import ACCENT, BG
except ImportError:
    # Fallback responsive color tuples if imports fail
    ACCENT = "#36a3ff"
    BG = ("#f8fafc", "#1e1e1e")

# Define a professional card panel theme color
# Light mode: Clean white card | Dark mode: Modern dark charcoal card
PANEL = ("#ffffff", "#2b2b2b")

class AboutSection(ctk.CTkFrame):
    """Highly professional, modern system diagnostic and software about module."""
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.build_ui()

    def build_ui(self):
        # 1. Main Container with smooth scrolling capability
        scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll_container.pack(fill="both", expand=True, padx=25, pady=25)

        # 2. Hero Section / Application Branding
        hero_card = ctk.CTkFrame(scroll_container, fg_color=PANEL, corner_radius=12)
        hero_card.pack(fill="x", pady=(0, 15))
        
        brand_frame = ctk.CTkFrame(hero_card, fg_color="transparent")
        brand_frame.pack(anchor="w", padx=30, pady=25)
        
        logo_label = ctk.CTkLabel(brand_frame, text="▣", font=("Segoe UI", 42), text_color=ACCENT)
        logo_label.pack(side="left", padx=(0, 15))
        
        title_text_frame = ctk.CTkFrame(brand_frame, fg_color="transparent")
        title_text_frame.pack(side="left")
        
        ctk.CTkLabel(
            title_text_frame, 
            text="Operating System Simulator Suite", 
            font=("Segoe UI", 24, "bold")
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_text_frame, 
            text="Advanced Multi-Threading, CPU Scheduling & Resource Allocation Architecture Lab", 
            font=("Segoe UI", 13, "italic"),
            text_color=("#475569", "#94a3b8")
        ).pack(anchor="w", pady=(2, 0))

        # 3. Two-Column Dashboard Grid Layout
        grid_frame = ctk.CTkFrame(scroll_container, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True)
        grid_frame.grid_columnconfigure(0, weight=1, uniform="col")
        grid_frame.grid_columnconfigure(1, weight=1, uniform="col")

        # --- LEFT PANEL: Application Build Specifications ---
        app_card = ctk.CTkFrame(grid_frame, fg_color=PANEL, corner_radius=12)
        app_card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        
        ctk.CTkLabel(app_card, text="Build Specifications", font=("Segoe UI", 16, "bold"), text_color=ACCENT).pack(anchor="w", padx=20, pady=(15, 10))
        
        app_info = [
            ("Core Version", "v1.2.4-stable"),
            ("UI Engine", f"CustomTkinter (v{ctk.__version__})"),
            ("Build Date", "June 14, 2026"),
            ("Software License", "MIT Open Source Reference"),
            ("Release Stage", "Deployment Verified Production Stable")
        ]
        self.render_properties(app_card, app_info)

        # --- RIGHT PANEL: Live Host System Environment Diagnostics ---
        sys_card = ctk.CTkFrame(grid_frame, fg_color=PANEL, corner_radius=12)
        sys_card.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        
        ctk.CTkLabel(sys_card, text="Live Host Diagnostics", font=("Segoe UI", 16, "bold"), text_color=ACCENT).pack(anchor="w", padx=20, pady=(15, 10))
        
        # FIXED: Replaced ctk.TkVersion with tk.TkVersion to prevent core crashes
        sys_info = [
            ("Host OS Platform", platform.system()),
            ("Kernel Distribution", platform.release()),
            ("Processor Family", platform.machine()),
            ("Python Runtime", f"v{platform.python_version()} ({sys.byteorder}-endian)"),
            ("GUI Framework", f"Tkinter Engine (v{tk.TkVersion})")
        ]
        self.render_properties(sys_card, sys_info)

        # 4. Action / Repository Link Footer
        footer_card = ctk.CTkFrame(scroll_container, fg_color=PANEL, corner_radius=12)
        footer_card.pack(fill="x", pady=15)
        
        ctk.CTkLabel(
            footer_card, 
            text="© 2026 Advanced Operating Systems Lab Project Engine. All rights reserved.", 
            font=("Segoe UI", 11),
            text_color=("#64748b", "#94a3b8")
        ).pack(side="left", padx=20, pady=15)
        
        action_btn = ctk.CTkButton(
            footer_card, 
            text="View Documentation", 
            width=160,
            height=32,
            fg_color=ACCENT,
            hover_color=("#2563eb", "#1d4ed8"),
            font=("Segoe UI", 12, "bold")
        )
        action_btn.pack(side="right", padx=20, pady=12)

    def render_properties(self, parent_card, item_list):
        """Helper method to format data values cleanly like an enterprise settings panel."""
        for label, val in item_list:
            row_frame = ctk.CTkFrame(parent_card, fg_color="transparent")
            row_frame.pack(fill="x", padx=20, pady=6)
            
            # Left Property Title
            ctk.CTkLabel(
                row_frame, 
                text=label, 
                font=("Segoe UI Semibold", 13), 
                text_color=("#475569", "#cbd5e1")
            ).pack(side="left")
            
            # Right Property Calculated Value
            is_monospaced = "Version" in label or "Python" in label or "Framework" in label
            ctk.CTkLabel(
                row_frame, 
                text=val, 
                font=("Consolas" if is_monospaced else "Segoe UI", 13),
                text_color=("#1e293b", "#f8fafc")
            ).pack(side="right")
            
            # Thin elegant layout dividers
            separator = ctk.CTkFrame(parent_card, height=1, fg_color=("#e2e8f0", "#384252"))
            separator.pack(fill="x", padx=20, pady=(2, 4))