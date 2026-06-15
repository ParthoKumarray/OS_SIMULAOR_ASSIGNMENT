import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import random
from ui_components import *

class MyDashboard(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.is_live = False  
        self.cpu_history = [random.randint(20, 45) for _ in range(24)] 
        self.running_procs = 2
        self.waiting_procs = 3
        
        self.build_ui()

    def build_ui(self):
        wrap = ctk.CTkFrame(self, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=30, pady=25)
        
        header = ctk.CTkFrame(wrap, fg_color="transparent")
        header.pack(fill="x", pady=(0, 25))
        
        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.pack(side="left")
        title_label(title_box, "System Monitor").pack(anchor="w")
        tk.Label(title_box, text="Click any card, chart, or table row to open its module", bg=BG, fg=MUTED, font=FONT_SMALL).pack(anchor="w", pady=(2,0))
        
        self.live_btn = ctk.CTkButton(header, text="▶ Initialize Live Simulation", 
                                      fg_color=ACCENT, hover_color="#2563eb", text_color="#ffffff", 
                                      font=("Segoe UI Semibold", 12), corner_radius=8, height=36, 
                                      cursor="hand2", command=self.toggle_live_simulation)
        self.live_btn.pack(side="right")

        cards_frame = ctk.CTkFrame(wrap, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 25))
        
        self.card_labels = [] 
        stats_config = [
            ("Active Tasks", ACCENT, "CPU Scheduling"),
            ("Running State", GREEN, "CPU Scheduling"),
            ("Waiting State", ORANGE, "Process Synchronization"),
            ("CPU Load", PURPLE, "CPU Scheduling"),
        ]
        
        for i, (label, color, target_page) in enumerate(stats_config):
            card = ctk.CTkFrame(cards_frame, fg_color=PANEL, corner_radius=12, border_width=1, border_color=BORDER, height=110)
            card.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 18, 0))
            cards_frame.grid_columnconfigure(i, weight=1)
            card.grid_propagate(False)
            card.configure(cursor="hand2")
            
            dot = ctk.CTkFrame(card, width=12, height=12, fg_color=color, corner_radius=6)
            dot.place(relx=0.08, rely=0.2)
            
            lbl = ctk.CTkLabel(card, text=label.upper(), font=("Segoe UI", 11, "bold"), text_color=MUTED)
            lbl.place(relx=0.18, rely=0.16)

            val_label = ctk.CTkLabel(card, text="0", font=("Segoe UI", 38, "bold"), text_color=TEXT)
            val_label.place(relx=0.08, rely=0.45)
            self.card_labels.append(val_label)
            
            self.make_interactive(card, target_page)

        middle = ctk.CTkFrame(wrap, fg_color="transparent")
        middle.pack(fill="both", expand=True, pady=(0, 25))
        middle.grid_columnconfigure(0, weight=5)
        middle.grid_columnconfigure(1, weight=3)
        middle.grid_rowconfigure(0, weight=1)

        util_panel = ctk.CTkFrame(middle, fg_color=PANEL, corner_radius=12, border_width=1, border_color=BORDER)
        util_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 18))
        section_label(util_panel, "CPU Utilization Graph ↗", bg=PANEL).pack(anchor="w", padx=20, pady=(15, 0))
        
        self.line_canvas = tk.Canvas(util_panel, bg=PANEL, highlightthickness=0, height=220, cursor="hand2")
        self.line_canvas.pack(fill="both", expand=True, padx=20, pady=(10, 15))
        self.make_interactive(util_panel, "CPU Scheduling", is_canvas_wrapper=True, canvas_widget=self.line_canvas)

        pie_panel = ctk.CTkFrame(middle, fg_color=PANEL, corner_radius=12, border_width=1, border_color=BORDER)
        pie_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 0))
        section_label(pie_panel, "Process Distribution ↗", bg=PANEL).pack(anchor="w", padx=20, pady=(15, 0))
        
        self.pie_canvas = tk.Canvas(pie_panel, bg=PANEL, highlightthickness=0, height=220, cursor="hand2")
        self.pie_canvas.pack(fill="both", expand=True, padx=20, pady=(10, 15))
        self.make_interactive(pie_panel, "Process Synchronization", is_canvas_wrapper=True, canvas_widget=self.pie_canvas)

        recent = ctk.CTkFrame(wrap, fg_color=PANEL, corner_radius=12, border_width=1, border_color=BORDER)
        recent.pack(fill="x", expand=False)
        
        header_frame = ctk.CTkFrame(recent, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(15, 5))
        section_label(header_frame, "Active Process Queue", bg=PANEL).pack(side="left")
        
        cols = ("PID", "Module Subsystem", "Execution State", "Memory Alloc", "Burst Time")
        self.tree = ttk.Treeview(recent, columns=cols, show="headings", height=4)
        
        widths = [80, 250, 150, 130, 120]
        for c, w in zip(cols, widths):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w, anchor="center")
            
        self.tree.pack(fill="x", padx=20, pady=(0, 20))
        
        self.tree.bind("<<TreeviewSelect>>", self.on_table_row_click)
        self.tree.bind("<Motion>", lambda e: self.tree.configure(cursor="hand2"))

        self.line_canvas.bind("<Configure>", lambda e: self.draw_line_chart())
        self.pie_canvas.bind("<Configure>", lambda e: self.draw_pie_chart())
        self.update_ui_values()

    def make_interactive(self, widget, target_page, is_canvas_wrapper=False, canvas_widget=None):
        # Configure hover bindings and dashboard routing for UI components
        hover_color = "#1f2937"  
        default_color = PANEL
        
        def on_enter(e):
            widget.configure(fg_color=hover_color)
            if is_canvas_wrapper and canvas_widget:
                canvas_widget.configure(bg=hover_color)
                if canvas_widget == self.line_canvas: self.draw_line_chart(hover_color)
                if canvas_widget == self.pie_canvas: self.draw_pie_chart(hover_color)

        def on_leave(e):
            widget.configure(fg_color=default_color)
            if is_canvas_wrapper and canvas_widget:
                canvas_widget.configure(bg=default_color)
                if canvas_widget == self.line_canvas: self.draw_line_chart(default_color)
                if canvas_widget == self.pie_canvas: self.draw_pie_chart(default_color)

        def on_click(e):
            self.go_to_page(target_page)

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
        widget.bind("<Button-1>", on_click)

        for child in widget.winfo_children():
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)
            child.bind("<Button-1>", on_click)
            
            if isinstance(child, tk.Canvas):
                child.bind("<Button-1>", on_click)

    def go_to_page(self, page_name):
        try:
            top_window = self.winfo_toplevel()
            if hasattr(top_window, 'app'):
                top_window.app.navigate(page_name)
        except Exception as e:
            print(f"Routing Error: {e}")

    def on_table_row_click(self, event):
        selected_item = self.tree.focus()
        if not selected_item: return
        row_values = self.tree.item(selected_item, "values")
        if not row_values: return
        
        module_name = row_values[1] 
        mapping = {
            "CPU Scheduler": "CPU Scheduling",
            "Memory Management": "Memory Management",
            "Disk I/O Manager": "File Management",
            "Banker's Algorithm": "Deadlock Handling"
        }
        target_page = mapping.get(module_name)
        if target_page: 
            self.go_to_page(target_page)
            self.tree.selection_remove(selected_item) 

    def toggle_live_simulation(self):
        self.is_live = not self.is_live
        if self.is_live:
            self.live_btn.configure(text="⏸ Pause Monitor", fg_color="#1f2937", text_color=RED, border_width=1, border_color=RED)
            self.run_live_loop()
        else:
            self.live_btn.configure(text="▶ Initialize Live Simulation", fg_color=ACCENT, text_color="#ffffff", border_width=0)

    def run_live_loop(self):
        # Update simulation counters and redraw visuals every 1.2 seconds
        if not self.winfo_exists() or not self.is_live: return

        next_val = max(5, min(98, self.cpu_history[-1] + random.randint(-15, 18)))
        self.cpu_history.pop(0)
        self.cpu_history.append(next_val)

        if random.random() > 0.5:
            self.running_procs = random.randint(2, 6)
            self.waiting_procs = random.randint(1, 4)

        self.update_ui_values()
        
        line_bg = self.line_canvas.cget("bg")
        pie_bg = self.pie_canvas.cget("bg")
        
        self.draw_line_chart(line_bg)
        self.draw_pie_chart(pie_bg)
        
        self.after(1200, self.run_live_loop)

    def update_ui_values(self):
        total = self.running_procs + self.waiting_procs + random.randint(1, 3)
        current_cpu = self.cpu_history[-1]

        self.card_labels[0].configure(text=str(total))
        self.card_labels[1].configure(text=str(self.running_procs))
        self.card_labels[2].configure(text=str(self.waiting_procs))
        self.card_labels[3].configure(f"{current_cpu}%")

        for item in self.tree.get_children():
            self.tree.delete(item)
            
        components = ["CPU Scheduler", "Memory Management", "Disk I/O Manager", "Banker's Algorithm"]
        for i in range(total):
            state = "Running" if i < self.running_procs else ("Waiting" if i < self.running_procs + self.waiting_procs else "Ready")
            mod = random.choice(components)
            ram = f"{random.randint(64, 1024)} MB"
            burst = f"{random.randint(1, 20)} ms"
            self.tree.insert("", "end", values=(f"P{i+301}", mod, state, ram, burst))

    def draw_line_chart(self, bg_color=PANEL):
        # Dynamically render the real-time line chart onto the tk.Canvas
        c = self.line_canvas
        c.delete("all")
        
        w, h = max(c.winfo_width(), 500), max(c.winfo_height(), 190)
        left, right, top, bottom = 40, w - 20, 10, h - 30
        
        for pct in range(0, 101, 25):
            y = bottom - (pct / 100) * (bottom - top)
            c.create_line(left, y, right, y, fill="#1f2937", dash=(2, 4))
            c.create_text(left - 10, y, text=f"{pct}%", anchor="e", fill=MUTED, font=("Segoe UI", 9))
            
        pts = []
        for i, v in enumerate(self.cpu_history):
            x = left + i * (right - left) / (len(self.cpu_history) - 1)
            y = bottom - v / 100 * (bottom - top)
            pts.extend([x, y])
            
        if pts:
            poly_pts = [left, bottom] + pts + [right, bottom]
            c.create_polygon(*poly_pts, fill="#172554", outline="") 
            c.create_line(*pts, fill=ACCENT, width=3, smooth=True, capstyle="round")
        
        c.create_text((left + right) / 2, h - 5, text="Time Ticks ➔", fill=MUTED, font=("Segoe UI Semibold", 9))

    def draw_pie_chart(self, bg_color=PANEL):
        c = self.pie_canvas
        c.delete("all")
        
        w, h = max(c.winfo_width(), 350), max(c.winfo_height(), 190)
        size = min(150, h - 30)
        x1, y1 = 40, (h - size) / 2 - 10
        x2, y2 = x1 + size, y1 + size
        
        total = max(1, self.running_procs + self.waiting_procs)
        run_ext = (self.running_procs / total) * 360
        wait_ext = 360 - run_ext
        
        c.create_arc(x1, y1, x2, y2, start=90, extent=run_ext, fill=GREEN, outline=bg_color, width=4)
        c.create_arc(x1, y1, x2, y2, start=90+run_ext, extent=wait_ext, fill=ORANGE, outline=bg_color, width=4)
        
        c.create_oval(x1+40, y1+40, x2-40, y2-40, fill=bg_color, outline="")
        
        legend_x = x2 + 35
        legend_y_start = (h - 60) / 2
        legend_items = [(GREEN, f"Running ({self.running_procs})"), (ORANGE, f"Waiting ({self.waiting_procs})")]
        
        for i, (color, text) in enumerate(legend_items):
            ly = legend_y_start + i * 35
            c.create_oval(legend_x, ly, legend_x + 12, ly + 12, fill=color, outline="")
            c.create_text(legend_x + 25, ly + 6, text=text, anchor="w", fill=TEXT, font=("Segoe UI Semibold", 11))