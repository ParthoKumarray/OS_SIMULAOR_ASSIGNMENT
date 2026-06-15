import math
import random
import tkinter as tk
from tkinter import ttk, messagebox
from ui_components import *

# Core logic loop to handle page hits, faults, and replacements
def simulate_page_replacement(refs, frames_count, algorithm):
    frames = []
    history = []      
    faults = []       
    actions = []      

    for i, page in enumerate(refs):
        hit = page in frames
        faults.append(not hit)
        updated_index = -1

        if not hit:
            if len(frames) < frames_count:
                frames.append(page)
                updated_index = len(frames) - 1
            else:
                if algorithm == "FIFO":
                    victim = frames[0]
                    frames.pop(0)
                    frames.append(page)
                    updated_index = frames_count - 1 
                    
                elif algorithm == "LRU":
                    # Find and replace the least recently used page
                    past_refs = refs[:i]
                    last_used = {f: (len(past_refs) - past_refs[::-1].index(f) - 1) for f in frames}
                    victim = min(frames, key=lambda f: last_used[f])
                    updated_index = frames.index(victim)
                    frames[updated_index] = page
                    
                elif algorithm == "Optimal":
                    future_refs = refs[i + 1:]
                    distances = {}
                    for f in frames:
                        distances[f] = future_refs.index(f) if f in future_refs else math.inf
                    victim = max(frames, key=lambda f: distances[f])
                    updated_index = frames.index(victim)
                    frames[updated_index] = page

        if algorithm == "FIFO":
            history.append(list(frames))
            if updated_index != -1:
                actions.append(len(frames) - 1)
            else:
                actions.append(frames.index(page))
        else:
            history.append(list(frames))
            actions.append(updated_index if not hit else frames.index(page))

    return history, faults, actions

class MemoryManagement(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        self.build_ui()

    def build_ui(self):
        wrap = tk.Frame(self, bg=BG)
        wrap.pack(fill="both", expand=True, padx=20, pady=16)
        title_label(wrap, "Memory Management").pack(fill="x", pady=(0, 8))

        self.notebook = ttk.Notebook(wrap)
        self.notebook.pack(fill="both", expand=True)
        
        self.page_tab = tk.Frame(self.notebook, bg=BG)
        self.alloc_tab = tk.Frame(self.notebook, bg=BG) 
        
        self.notebook.add(self.page_tab, text="Page Replacement")
        self.notebook.add(self.alloc_tab, text="Block Allocation")
        
        self.build_page_replacement(self.page_tab)

    def build_page_replacement(self, parent):
        top = panel(parent)
        top.pack(fill="x", padx=4, pady=(12, 8))
        
        tk.Label(top, text="Total Frames", bg=PANEL, fg=TEXT, font=FONT_SMALL).pack(side="left", padx=(16, 8), pady=12)
        self.frame_var = tk.StringVar(value="4")
        self.frame_spin = ttk.Spinbox(top, from_=1, to=10, textvariable=self.frame_var, width=5, state="readonly")
        self.frame_spin.pack(side="left")

        tk.Label(top, text="Algorithm", bg=PANEL, fg=TEXT, font=FONT_SMALL).pack(side="left", padx=(24, 8))
        self.algo_var = tk.StringVar(value="LRU")
        self.algo_cb = ttk.Combobox(top, textvariable=self.algo_var, values=["FIFO", "LRU", "Optimal"], state="readonly", width=12)
        self.algo_cb.pack(side="left")

        tk.Label(top, text="Reference String", bg=PANEL, fg=TEXT, font=FONT_SMALL).pack(side="left", padx=(24, 8))
        self.ref_var = tk.StringVar(value="7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2")
        self.ref_entry = ttk.Entry(top, textvariable=self.ref_var, width=35)
        self.ref_entry.pack(side="left", expand=True, fill="x", padx=(0, 16))

        button(top, "⚄ Randomize", self.randomize_string, bg=MUTED, width=12).pack(side="right", padx=(0, 16), pady=10)
        button(top, "▶ Run", self.run_simulation, bg=ACCENT, width=10).pack(side="right", padx=(16, 8), pady=10)

        body = tk.Frame(parent, bg=BG)
        body.pack(fill="both", expand=True, padx=4)
        body.grid_columnconfigure(0, weight=7) 
        body.grid_columnconfigure(1, weight=2) 
        body.grid_rowconfigure(0, weight=1)

        vis_panel = panel(body)
        vis_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        
        header_frame = tk.Frame(vis_panel, bg=PANEL)
        header_frame.pack(fill="x", padx=12, pady=(12, 6))
        section_label(header_frame, "Page Frame Visualization").pack(side="left")
        
        legend = tk.Frame(header_frame, bg=PANEL)
        legend.pack(side="right")
        self.make_legend_item(legend, "#e5f4df", "Hit")
        self.make_legend_item(legend, "#fde2e2", "Fault")
        self.make_legend_item(legend, "#fca5a5", "Replaced Page")

        canvas_container = tk.Frame(vis_panel, bg=PANEL)
        canvas_container.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        
        self.scroll_x = ttk.Scrollbar(canvas_container, orient="horizontal")
        self.scroll_x.pack(side="bottom", fill="x")
        
        self.canvas = tk.Canvas(canvas_container, bg=PANEL, highlightthickness=0, xscrollcommand=self.scroll_x.set)
        self.canvas.pack(side="top", fill="both", expand=True)
        self.scroll_x.config(command=self.canvas.xview)

        stat_panel = panel(body)
        stat_panel.grid(row=0, column=1, sticky="nsew")
        section_label(stat_panel, "Statistics").pack(anchor="w", padx=16, pady=(12, 6))
        
        self.stats_frame = tk.Frame(stat_panel, bg=PANEL)
        self.stats_frame.pack(fill="both", expand=True, padx=16, pady=8)

        self.run_simulation()

    def make_legend_item(self, parent, color, text):
        f = tk.Frame(parent, bg=PANEL)
        f.pack(side="left", padx=8)
        c = tk.Canvas(f, width=16, height=16, bg=PANEL, highlightthickness=0)
        c.create_rectangle(0, 0, 16, 16, fill=color, outline=BORDER)
        c.pack(side="left", padx=(0, 4))
        tk.Label(f, text=text, bg=PANEL, fg=MUTED, font=("Segoe UI", 9)).pack(side="left")

    def randomize_string(self):
        length = random.randint(12, 20)
        pages = [str(random.randint(0, 7)) for _ in range(length)]
        self.ref_var.set(", ".join(pages))
        self.run_simulation()

    # Parse inputs safely and trigger the chosen replacement execution
    def run_simulation(self):
        try:
            raw_input = self.ref_var.get().replace(",", " ")
            refs = [int(x) for x in raw_input.split() if x.strip().isdigit()]
            
            if not refs:
                raise ValueError("Reference string is empty or invalid.")
                
            frames_count = int(self.frame_var.get())
            algo = self.algo_var.get()

            history, faults, actions = simulate_page_replacement(refs, frames_count, algo)
            
            self.draw_visualization(refs, history, faults, actions, frames_count)
            self.update_statistics(len(refs), faults)

        except ValueError as e:
            messagebox.showwarning("Input Error", f"Please check your inputs:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

    def update_statistics(self, total_refs, faults):
        clear_frame(self.stats_frame)
        
        fault_count = sum(faults)
        hit_count = total_refs - fault_count
        fault_rate = (fault_count / total_refs) * 100
        hit_rate = (hit_count / total_refs) * 100

        data = [
            ("Total References", str(total_refs)),
            ("Page Faults", str(fault_count)),
            ("Page Hits", str(hit_count)),
            ("Fault Rate", f"{fault_rate:.2f}%"),
            ("Hit Rate", f"{hit_rate:.2f}%")
        ]

        for i, (label, val) in enumerate(data):
            val_color = TEXT
            if "Hits" in label or "Hit Rate" in label: val_color = GREEN
            elif "Faults" in label or "Fault Rate" in label: val_color = RED
            
            tk.Label(self.stats_frame, text=label, bg=PANEL, fg=MUTED, font=FONT).grid(row=i, column=0, sticky="w", pady=12)
            tk.Label(self.stats_frame, text=val, bg=PANEL, fg=val_color, font=("Segoe UI Semibold", 12)).grid(row=i, column=1, sticky="w", padx=24, pady=12)

    # Render the structured grid, cell states, and results onto the Canvas layout
    def draw_visualization(self, refs, history, faults, actions, frames_count):
        self.canvas.delete("all")
        
        cell_w, cell_h = 44, 38
        pad_x, pad_y = 20, 20
        
        total_width = pad_x * 2 + (len(refs) + 1) * cell_w
        total_height = pad_y * 2 + (frames_count + 3) * cell_h
        self.canvas.config(scrollregion=(0, 0, total_width, total_height))

        self.canvas.create_text(pad_x + cell_w/2, pad_y + cell_h/2, text="Ref", font=("Segoe UI Semibold", 10), fill=MUTED)
        for col, page in enumerate(refs):
            x = pad_x + (col + 1) * cell_w
            self.canvas.create_rectangle(x, pad_y, x + cell_w, pad_y + cell_h, fill="#f8fafc", outline=BORDER)
            self.canvas.create_text(x + cell_w/2, pad_y + cell_h/2, text=str(page), font=("Segoe UI Semibold", 11), fill=TEXT)

        for r in range(frames_count):
            y = pad_y + (r + 1) * cell_h
            self.canvas.create_text(pad_x + cell_w/2, y + cell_h/2, text=f"F{r}", font=("Segoe UI Semibold", 9), fill=MUTED)
            
            for col in range(len(refs)):
                x = pad_x + (col + 1) * cell_w
                is_fault = faults[col]
                updated_idx = actions[col]
                
                if is_fault:
                    if r == updated_idx:
                        bg_color = "#fca5a5"  
                    else:
                        bg_color = "#fde2e2"  
                else:
                    bg_color = "#e5f4df"      
                
                self.canvas.create_rectangle(x, y, x + cell_w, y + cell_h, fill=bg_color, outline=BORDER)
                
                state = history[col]
                if r < len(state):
                    val = str(state[r])
                    font = ("Segoe UI Semibold", 10) if r == updated_idx else ("Segoe UI", 10)
                    self.canvas.create_text(x + cell_w/2, y + cell_h/2, text=val, font=font, fill=TEXT)
                else:
                    self.canvas.create_text(x + cell_w/2, y + cell_h/2, text="-", font=("Segoe UI", 10), fill="#94a3b8")

        y_footer = pad_y + (frames_count + 1) * cell_h + 8
        self.canvas.create_text(pad_x + cell_w/2, y_footer + cell_h/2, text="Status", font=("Segoe UI Semibold", 9), fill=MUTED)
        
        for col, is_fault in enumerate(faults):
            x = pad_x + (col + 1) * cell_w
            text = "F" if is_fault else "H"
            color = RED if is_fault else GREEN
            
            self.canvas.create_rectangle(x, y_footer, x + cell_w, y_footer + cell_h, fill=PANEL, outline=BORDER)
            self.canvas.create_text(x + cell_w/2, y_footer + cell_h/2, text=text, font=("Segoe UI Semibold", 11), fill=color)