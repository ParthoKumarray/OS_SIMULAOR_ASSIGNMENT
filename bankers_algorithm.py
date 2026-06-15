import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import numpy as np
import random

try:
    from ui_components import BG, PANEL, ACCENT, GREEN, RED
except ImportError:
    BG = "#1e1e1e"
    PANEL = "#2b2b2b"
    ACCENT = "#36a3ff"
    GREEN = "#37c65a"
    RED = "#ff4d4d"

class BankerEngine:
    def __init__(self, available, max_matrix, alloc_matrix):
        self.available = np.array(available)
        self.max = np.array(max_matrix)
        self.alloc = np.array(alloc_matrix)
        self.need = self.max - self.alloc
        self.num_processes = len(max_matrix)
        self.num_resources = len(available)

    # Core loop to find a safe execution sequence for processes
    def find_safe_sequence(self):
        work = self.available.copy()
        finish = [False] * self.num_processes
        safe_sequence = []
        log_messages = []

        log_messages.append(f"Initial Work (Available Resources): {work.tolist()}")
        
        while len(safe_sequence) < self.num_processes:
            found = False
            for i in range(self.num_processes):
                if not finish[i]:
                    if all(self.need[i] <= work):
                        log_messages.append(f"✓ P{i} can run: Need {self.need[i].tolist()} <= Work {work.tolist()}")
                        work += self.alloc[i]
                        finish[i] = True
                        safe_sequence.append(i)
                        found = True
                        log_messages.append(f"  P{i} allocated resources released. New Work: {work.tolist()}")
            
            if not found:
                log_messages.append("\n⚠ DEADLOCK DETECTED! No safe sequence can be formed from remaining processes.")
                return None, log_messages
                
        log_messages.append("\n✓ System status evaluated: SAFE STATE.")
        return safe_sequence, log_messages

class DeadlockHandling(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.alloc_entries = []
        self.max_entries = []
        self.avail_entries = []
        
        self.build_ui()
        self.trigger_direct_simulation()

    def build_ui(self):
        header_frame = ctk.CTkFrame(self, fg_color=PANEL, corner_radius=10)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(header_frame, text="Banker's Algorithm Simulator", font=("Segoe UI", 24, "bold"), text_color=ACCENT).pack(side="left", padx=20, pady=15)
        
        config_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        config_frame.pack(side="right", padx=20, pady=10)
        
        ctk.CTkLabel(config_frame, text="Processes:", font=("Segoe UI", 14)).grid(row=0, column=0, padx=5)
        self.spin_proc = ctk.CTkEntry(config_frame, width=50)
        self.spin_proc.insert(0, "5")
        self.spin_proc.grid(row=0, column=1, padx=5)
        
        ctk.CTkLabel(config_frame, text="Resources:", font=("Segoe UI", 14)).grid(row=0, column=2, padx=5)
        self.spin_res = ctk.CTkEntry(config_frame, width=50)
        self.spin_res.insert(0, "3")
        self.spin_res.grid(row=0, column=3, padx=5)
        
        ctk.CTkButton(config_frame, text="Apply Grid", command=self.generate_grids, width=100).grid(row=0, column=4, padx=(15, 5))
        ctk.CTkButton(config_frame, text="Random Auto-Run", command=self.run_random_workload, width=130, fg_color="#6f42c1", hover_color="#5933a8").grid(row=0, column=5, padx=5)

        self.scroll_area = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_area.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.matrix_container = ctk.CTkFrame(self.scroll_area, fg_color="transparent")
        self.matrix_container.pack(fill="x", expand=True)
        
        footer_frame = ctk.CTkFrame(self, fg_color=PANEL, corner_radius=10, height=220)
        footer_frame.pack(fill="x", padx=20, pady=10)
        
        btn_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(btn_frame, text="Run Safety Analysis", command=self.run_simulation, fg_color=GREEN, hover_color="#2da04a", height=40, font=("Segoe UI", 14, "bold")).pack(side="left")
        ctk.CTkButton(btn_frame, text="Reset Defaults", command=self.trigger_direct_simulation, fg_color="#5a6268", hover_color="#4e555b", height=40).pack(side="left", padx=10)
        
        self.result_title = ctk.CTkLabel(btn_frame, text="", font=("Segoe UI", 16, "bold"))
        self.result_title.pack(side="left", padx=20)
        
        self.log_textbox = ctk.CTkTextbox(footer_frame, height=130, font=("Consolas", 13), fg_color=BG)
        self.log_textbox.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.log_textbox.configure(state="disabled")

    # Clear previous widgets and generate input fields for the matrices
    def generate_grids(self):
        try:
            p_count = int(self.spin_proc.get())
            r_count = int(self.spin_res.get())
        except ValueError:
            messagebox.showerror("Input Error", "Process and Resource counts must be valid integers.")
            return

        for widget in self.matrix_container.winfo_children():
            widget.destroy()

        self.alloc_entries.clear()
        self.max_entries.clear()
        self.avail_entries.clear()

        alloc_frame = ctk.CTkFrame(self.matrix_container, fg_color=PANEL)
        alloc_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.build_matrix_ui("Allocation Matrix", p_count, r_count, alloc_frame, self.alloc_entries)

        max_frame = ctk.CTkFrame(self.matrix_container, fg_color=PANEL)
        max_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.build_matrix_ui("Max Matrix", p_count, r_count, max_frame, self.max_entries)
        
        avail_frame = ctk.CTkFrame(self.matrix_container, fg_color=PANEL)
        avail_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(avail_frame, text="Available Resources", font=("Segoe UI", 16, "bold")).pack(pady=10)
        avail_grid = ctk.CTkFrame(avail_frame, fg_color="transparent")
        avail_grid.pack(pady=10)
        
        for j in range(r_count):
             ctk.CTkLabel(avail_grid, text=chr(65 + j)).grid(row=0, column=j, padx=5, pady=2)
             
        for j in range(r_count):
            entry = ctk.CTkEntry(avail_grid, width=45, justify="center")
            entry.grid(row=1, column=j, padx=5, pady=5)
            self.avail_entries.append(entry)

    def build_matrix_ui(self, title, p_count, r_count, parent, storage):
        ctk.CTkLabel(parent, text=title, font=("Segoe UI", 16, "bold")).pack(pady=10)
        grid_frame = ctk.CTkFrame(parent, fg_color="transparent")
        grid_frame.pack(pady=10)

        ctk.CTkLabel(grid_frame, text="P\\R").grid(row=0, column=0, padx=5, pady=2)
        for j in range(r_count):
             ctk.CTkLabel(grid_frame, text=chr(65 + j)).grid(row=0, column=j+1, padx=5, pady=2)

        for i in range(p_count):
            ctk.CTkLabel(grid_frame, text=f"P{i}").grid(row=i+1, column=0, padx=5, pady=2)
            row_items = []
            for j in range(r_count):
                entry = ctk.CTkEntry(grid_frame, width=40, justify="center")
                entry.grid(row=i+1, column=j+1, padx=5, pady=5)
                row_items.append(entry)
            storage.append(row_items)

    # Load default safe sample data right into the grid fields
    def trigger_direct_simulation(self):
        self.spin_proc.delete(0, "end")
        self.spin_proc.insert(0, "5")
        self.spin_res.delete(0, "end")
        self.spin_res.insert(0, "3")
        self.generate_grids()
        
        alloc_preset = [[0,1,0], [2,0,0], [3,0,2], [2,1,1], [0,0,2]]
        max_preset = [[7,5,3], [3,2,2], [9,0,2], [2,2,2], [4,3,3]]
        avail_preset = [3,3,2]
        
        for i in range(5):
            for j in range(3):
                self.alloc_entries[i][j].insert(0, str(alloc_preset[i][j]))
                self.max_entries[i][j].insert(0, str(max_preset[i][j]))
        for j in range(3):
            self.avail_entries[j].insert(0, str(avail_preset[j]))
            
        self.run_simulation()

    def run_random_workload(self):
        try:
            p_count = int(self.spin_proc.get())
            r_count = int(self.spin_res.get())
        except ValueError:
            return
            
        self.generate_grids()
        
        for i in range(p_count):
            for j in range(r_count):
                alloc_val = random.randint(0, 3)
                max_val = alloc_val + random.randint(0, 5)
                
                self.alloc_entries[i][j].insert(0, str(alloc_val))
                self.max_entries[i][j].insert(0, str(max_val))
                
        for j in range(r_count):
            self.avail_entries[j].insert(0, str(random.randint(1, 5)))
            
        self.run_simulation()

    def parse_matrix(self, entry_list, is_vector=False):
        try:
            if is_vector:
                return [int(e.get() or 0) for e in entry_list]
            return [[int(e.get() or 0) for e in row] for row in entry_list]
        except ValueError:
            return None

    # Parse inputs, validate safety criteria, and display logs
    def run_simulation(self):
        alloc = self.parse_matrix(self.alloc_entries)
        max_mat = self.parse_matrix(self.max_entries)
        avail = self.parse_matrix(self.avail_entries, is_vector=True)

        if alloc is None or max_mat is None or avail is None:
            messagebox.showerror("Matrix Error", "All vector slots must contain valid non-empty values.")
            return

        np_alloc, np_max = np.array(alloc), np.array(max_mat)
        if not np.all(np_max >= np_alloc):
            messagebox.showerror("Logical Violations", "Resource Allocation cannot exceed the declared Maximum limits (Max >= Alloc).")
            return

        engine = BankerEngine(avail, max_mat, alloc)
        sequence, log_messages = engine.find_safe_sequence()
        
        self.log_textbox.configure(state="normal")
        self.log_textbox.delete("1.0", "end")
        self.log_textbox.insert("end", "\n".join(log_messages))
        self.log_textbox.configure(state="disabled")
        
        if sequence:
            seq_text = " → ".join([f"P{i}" for i in sequence])
            self.result_title.configure(text=f"SAFE ORDER: {seq_text}", text_color=GREEN)
        else:
            self.result_title.configure(text="SYSTEM STATE UNSAFE: Potential Deadlock!", text_color=RED)