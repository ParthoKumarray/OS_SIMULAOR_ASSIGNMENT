import tkinter as tk
from tkinter import ttk


BG = "#1e1e1e" 

BG = ("#f4f6f9", "#1e1e1e") # (Light Mode Background, Dark Mode Background)
SIDEBAR = ("#e2e8f0", "#2b2b2b")
COLORS = {
    "BG": "#F8FAFC", "PANEL": "#FFFFFF", "TEXT": "#1E293B",
    "ACCENT": "#2563EB", "HOVER": "#1D4ED8", "MUTED": "#64748B"
}

def style_button(btn, cmd):
    btn.config(relief="flat", bg=COLORS["ACCENT"], fg="white", 
               font=("Segoe UI Semibold", 10), cursor="hand2")
    btn.bind("<Enter>", lambda e: btn.config(bg=COLORS["HOVER"]))
    btn.bind("<Leave>", lambda e: btn.config(bg=COLORS["ACCENT"]))
    btn.config(command=cmd)
BG = "#0b0f19"          # Deep dark background
PANEL = "#111827"       # Slightly lighter panel background
SIDEBAR = "#030712"     # Pitch dark sidebar
SIDEBAR_HOVER = "#1f2937"
ACCENT = "#3b82f6"      # Bright Modern Blue
GREEN = "#10b981"       # Emerald Green
ORANGE = "#f59e0b"      # Amber
RED = "#ef4444"         # Rose Red
PURPLE = "#8b5cf6"      # Violet
TEXT = "#f9fafb"        # Crisp White
MUTED = "#9ca3af"       # Slate Gray (for subtitles)
BORDER = "#1f2937"      # Subtle borders

FONT = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)
FONT_TITLE = ("Segoe UI", 22, "bold")
FONT_SUBTITLE = ("Segoe UI Semibold", 13)
FONT_CARD = ("Segoe UI", 36, "bold")

import tkinter as tk

# Define a professional color palette
BG = "#F8FAFC"
PANEL = "#FFFFFF"
ACCENT = "#2563EB"
HOVER = "#1D4ED8"
TEXT = "#1E293B"
MUTED = "#64748B"
GREEN = "#16A34A"
RED = "#DC2626"
BORDER = "#E2E8F0"

FONT = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI Semibold", 9)

def panel(parent):
    return tk.Frame(parent, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)

def button(parent, text, command, bg=ACCENT, width=12):
    btn = tk.Button(parent, text=text, command=command, bg=bg, fg="white", 
                    font=FONT_SMALL, relief="flat", activebackground=HOVER, 
                    padx=10, pady=5, width=width)
    
    # Hover Animation
    btn.bind("<Enter>", lambda e: btn.config(bg=HOVER))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn

def title_label(parent, text):
    return tk.Label(parent, text=text, font=("Segoe UI Bold", 18), bg=BG, fg=TEXT)

def section_label(parent, text):
    return tk.Label(parent, text=text, font=("Segoe UI Semibold", 11), bg=PANEL, fg=MUTED)

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def configure_styles(root):
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
        
    # Premium Treeview (Table) Styling for Dark Mode
    style.configure("Treeview", 
                    font=FONT_SMALL, 
                    rowheight=35, 
                    background=PANEL,
                    fieldbackground=PANEL, 
                    foreground=TEXT, 
                    bordercolor=PANEL,
                    borderwidth=0)
                    
    style.configure("Treeview.Heading", 
                    font=("Segoe UI Semibold", 10),
                    background="#1f2937", 
                    foreground=TEXT, 
                    relief="flat",
                    padding=8)
                    
    style.map("Treeview", 
              background=[("selected", "#1e3a8a")], 
              foreground=[("selected", "#ffffff")])
              
    style.map("Treeview.Heading", background=[("active", "#374151")])

def clear_frame(frame):
    for child in frame.winfo_children():
        child.destroy()

def panel(parent, **kwargs):
    # Removing thick borders for a cleaner look
    return tk.Frame(parent, bg=PANEL, highlightthickness=0, **kwargs)

def title_label(parent, text):
    return tk.Label(parent, text=text, bg=BG, fg=TEXT, font=FONT_TITLE, anchor="w")

def section_label(parent, text, bg=PANEL):
    return tk.Label(parent, text=text, bg=bg, fg=TEXT, font=FONT_SUBTITLE, anchor="w")