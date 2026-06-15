import tkinter as tk
from tkinter import ttk, messagebox
from ui_components import *

import ui_components as ui

class CPUSchedulerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CPU Scheduler Pro")
        self.geometry("1000x600")
        self.configure(bg=ui.COLORS["BG"])
        
        self.step_index = 0
        self.simulation_data = [] 
        
        self.setup_ui()

    def setup_ui(self):
        header = tk.Label(self, text="CPU Scheduler Simulator", font=("Segoe UI Bold", 20), bg=ui.COLORS["BG"], fg=ui.COLORS["TEXT"])
        header.pack(pady=20)
        
        main_frame = tk.Frame(self, bg=ui.COLORS["BG"])
        main_frame.pack(fill="both", expand=True, padx=40)
        
        ctrl = tk.Frame(main_frame, bg=ui.COLORS["BG"])
        ctrl.pack(fill="x", pady=10)
        
        self.btn_run = tk.Button(ctrl, text="▶ Run Animation")
        ui.style_button(self.btn_run, self.start_animation)
        self.btn_run.pack(side="left")
        
        self.canvas = tk.Canvas(main_frame, bg="white", highlightthickness=1, highlightbackground="#E2E8F0")
        self.canvas.pack(fill="both", expand=True, pady=20)
        self.canvas.bind("<Configure>", self.redraw_canvas)

    def get_scheduling_data(self):
        return [("P1", 0, 5), ("P2", 5, 8), ("P3", 8, 16), ("P4", 16, 22)]

    def start_animation(self):
        self.simulation_data = self.get_scheduling_data()
        self.step_index = 0
        self.canvas.delete("all") 
        self.animate_step()

    def animate_step(self):
        if self.step_index < len(self.simulation_data):
            pid, start, end = self.simulation_data[self.step_index]
            
            self.draw_block(pid, start, end)
            
            self.step_index += 1
            self.after(1000, self.animate_step)
        else:
            messagebox.showinfo("Done", "Simulation Complete!")

    def draw_block(self, pid, start, end):
        width = self.canvas.winfo_width()
        scale = (width - 40) / self.simulation_data[-1][2]
        
        x1 = 20 + (start * scale)
        x2 = 20 + (end * scale)
        
        self.canvas.create_rectangle(x1, 50, x2, 150, fill="#60A5FA", outline="white", width=2)
        self.canvas.create_text((x1+x2)/2, 100, text=pid, fill="white", font=("Arial", 12, "bold"))
        self.canvas.create_text((x1+x2)/2, 170, text=str(end), fill=ui.COLORS["TEXT"])

    def redraw_canvas(self, event):
        if self.simulation_data:
            self.canvas.delete("all")
            for i in range(self.step_index):
                self.draw_block(*self.simulation_data[i])

if __name__ == "__main__":
    app = CPUSchedulerApp()
    app.mainloop()

def start_step_simulation(self):
        segments = self.calculate_all_steps() 
        self.step_index = 0
        self.animate_step(segments)

def animate_step(self, segments):
    if self.step_index < len(segments):
        self.draw_highlight(segments[self.step_index])
            
        self.step_index += 1
        self.after(1000, lambda: self.animate_step(segments))
    else:
        messagebox.showinfo("Simulation", "Simulation Complete!")

def button(parent, text, command, bg=ACCENT, width=None):
    # Dynamic wrapper to support both CTk and native Tkinter button styling
    if hasattr(parent, "winfo_class") and "CTk" in parent.winfo_class():
        import customtkinter as ctk
        px_width = (width * 10) if (width is not None and width < 30) else (width if width else 120)
        txt_color = "#11111b" if bg in [ACCENT, GREEN, ORANGE] else "white"
        
        return ctk.CTkButton(parent, text=text, command=command, fg_color=bg, text_color=txt_color,
                             font=("Segoe UI", 12, "bold"), corner_radius=8, width=px_width, height=36,
                             cursor="hand2")
    else:
        import tkinter as tk
        txt_color = "black" if bg in [ACCENT, GREEN, ORANGE] else "white"
        w = width if width else 12
        
        btn = tk.Button(parent, text=text, command=command, bg=bg, fg=txt_color,
                        font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2", 
                        width=w, pady=4)
        return btn

def schedule_fcfs(processes):
    # First Come First Served scheduling calculation
    time_now = 0
    segments, completion = [], {}
    for pid, arr, burst, prio in sorted(processes, key=lambda x: (x[1], x[0])):
        if time_now < arr:
            segments.append(("Idle", time_now, arr))
            time_now = arr
        segments.append((pid, time_now, time_now + burst))
        time_now += burst
        completion[pid] = time_now
    return segments, completion

def schedule_sjf(processes):
    # Shortest Job First scheduling calculation
    remaining = {p[0]: p[2] for p in processes}
    done = set()
    segments, completion = [], {}
    time_now = min(p[1] for p in processes) if processes else 0
    while len(done) < len(processes):
        ready = [p for p in processes if p[1] <= time_now and p[0] not in done]
        if not ready:
            next_arr = min(p[1] for p in processes if p[0] not in done)
            segments.append(("Idle", time_now, next_arr))
            time_now = next_arr
            continue
        p = min(ready, key=lambda x: (x[2], x[1], x[0]))
        pid, arr, burst, prio = p
        segments.append((pid, time_now, time_now + burst))
        time_now += burst
        completion[pid] = time_now
        done.add(pid)
    return segments, completion

def schedule_priority(processes):
    # Priority scheduling logic execution loop
    done = set()
    segments, completion = [], {}
    time_now = min(p[1] for p in processes) if processes else 0
    while len(done) < len(processes):
        ready = [p for p in processes if p[1] <= time_now and p[0] not in done]
        if not ready:
            next_arr = min(p[1] for p in processes if p[0] not in done)
            segments.append(("Idle", time_now, next_arr))
            time_now = next_arr
            continue
        p = min(ready, key=lambda x: (x[3], x[1], x[0]))
        pid, arr, burst, prio = p
        segments.append((pid, time_now, time_now + burst))
        time_now += burst
        completion[pid] = time_now
        done.add(pid)
    return segments, completion

def schedule_rr(processes, quantum):
    # Preemptive Round Robin simulator processing queue blocks
    processes_sorted = sorted(processes, key=lambda x: (x[1], x[0]))
    remaining = {p[0]: p[2] for p in processes}
    completion = {}
    segments = []
    queue = []
    idx = 0
    time_now = processes_sorted[0][1] if processes_sorted else 0

    while len(completion) < len(processes):
        while idx < len(processes_sorted) and processes_sorted[idx][1] <= time_now:
            queue.append(processes_sorted[idx])
            idx += 1
            
        if not queue:
            if idx < len(processes_sorted):
                next_arr = processes_sorted[idx][1]
                if time_now < next_arr:
                    segments.append(("Idle", time_now, next_arr))
                time_now = next_arr
                continue
            break

        p = queue.pop(0)
        pid, arr, burst, prio = p
        run_time = min(quantum, remaining[pid])
        segments.append((pid, time_now, time_now + run_time))
        time_now += run_time
        remaining[pid] -= run_time

        while idx < len(processes_sorted) and processes_sorted[idx][1] <= time_now:
            queue.append(processes_sorted[idx])
            idx += 1

        if remaining[pid] > 0:
            queue.append(p)
        else:
            completion[pid] = time_now

    return segments, completion

def calculate_metrics(processes, completion, segments):
    # Processes computation data for metrics dashboard feedback
    waiting, turnaround = {}, {}
    for pid, arr, burst, prio in processes:
        tat = completion[pid] - arr
        wt = tat - burst
        waiting[pid] = wt
        turnaround[pid] = tat
        
    start_time = min((s[1] for s in segments), default=0)
    end_time = max((s[2] for s in segments), default=0)
    total_time = end_time - start_time
    
    busy_time = sum(s[2] - s[1] for s in segments if s[0] != "Idle")
    utilization = (busy_time / total_time * 100) if total_time > 0 else 0
    throughput = (len(processes) / total_time) if total_time > 0 else 0
    
    return waiting, turnaround, utilization, throughput

class CPUScheduler(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        self.current_segments = []  
        self.build_ui()

    def build_ui(self):
        wrap = tk.Frame(self, bg=BG)
        wrap.pack(fill="both", expand=True, padx=20, pady=16)
        title_label(wrap, "CPU Scheduling").pack(fill="x", pady=(0, 12))

        controls = panel(wrap)
        controls.pack(fill="x", pady=(0, 12))
        
        tk.Label(controls, text="Algorithm", bg=PANEL, fg=TEXT, font=FONT_SMALL).pack(side="left", padx=(16, 8), pady=12)
        self.algo_var = tk.StringVar(value="Round Robin")
        self.algo_cb = ttk.Combobox(controls, textvariable=self.algo_var, values=["FCFS", "SJF", "Round Robin", "Priority"], state="readonly", width=18)
        self.algo_cb.pack(side="left", padx=(0, 24))
        self.algo_cb.bind("<<ComboboxSelected>>", self.on_algo_change)

        self.lbl_quantum = tk.Label(controls, text="Time Quantum", bg=PANEL, fg=TEXT, font=FONT_SMALL)
        self.lbl_quantum.pack(side="left", padx=(0, 8))
        self.quantum_var = tk.StringVar(value="2")
        self.entry_quantum = ttk.Entry(controls, textvariable=self.quantum_var, width=8)
        self.entry_quantum.pack(side="left", padx=(0, 24))

        button(controls, "▶ Run Simulation", self.run_simulation, width=16, bg=ACCENT).pack(side="right", padx=16, pady=10)

        body = tk.Frame(wrap, bg=BG)
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(0, weight=4) 
        body.grid_columnconfigure(1, weight=5) 
        body.grid_rowconfigure(0, weight=1)

        left_panel = panel(body)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        section_label(left_panel, "Process Table").pack(anchor="w", padx=12, pady=(12, 6))

        table_frame = tk.Frame(left_panel, bg=PANEL)
        table_frame.pack(fill="both", expand=True, padx=12, pady=(0, 8))
        
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical")
        scroll_y.pack(side="right", fill="y")
        
        cols = ("PID", "Arrival Time", "Burst Time", "Priority")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.tree.yview)
        
        for c, w in zip(cols, [70, 100, 100, 80]):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w, anchor="center")
            
        self.tree.pack(fill="both", expand=True)
        
        btn_frame = tk.Frame(left_panel, bg=PANEL)
        btn_frame.pack(fill="x", padx=12, pady=(4, 12))
        button(btn_frame, "+ Add Process", self.add_process, bg=GREEN).pack(side="left")
        button(btn_frame, "− Remove", self.remove_process, bg=RED).pack(side="left", padx=8)
        button(btn_frame, "↻ Reset", self.reset_table, bg=MUTED).pack(side="right")

        right_panel = tk.Frame(body, bg=BG)
        right_panel.grid(row=0, column=1, sticky="nsew")

        gantt_panel = panel(right_panel)
        gantt_panel.pack(fill="both", expand=True, pady=(0, 12))
        section_label(gantt_panel, "Gantt Chart").pack(anchor="w", padx=12, pady=(12, 6))
        
        self.canvas = tk.Canvas(gantt_panel, bg=PANEL, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        self.canvas.bind("<Configure>", lambda e: self.draw_gantt(self.current_segments)) 

        metrics_panel = panel(right_panel)
        metrics_panel.pack(fill="x")
        section_label(metrics_panel, "Performance Metrics").pack(anchor="w", padx=12, pady=(12, 6))
        
        self.metrics_frame = tk.Frame(metrics_panel, bg=PANEL)
        self.metrics_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        self.reset_table()
        self.on_algo_change() 

    def on_algo_change(self, event=None):
        if self.algo_var.get() == "Round Robin":
            self.entry_quantum.config(state="normal")
            self.lbl_quantum.config(fg=TEXT)
        else:
            self.entry_quantum.config(state="disabled")
            self.lbl_quantum.config(fg=MUTED)

    def get_processes(self):
        processes = []
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            try:
                pid = str(values[0])
                arr = int(values[1])
                burst = int(values[2])
                prio = int(values[3])
                processes.append((pid, arr, burst, prio))
            except ValueError:
                raise ValueError(f"Invalid numeric data in process {values[0]}")
        if not processes:
            raise ValueError("Process table is empty.")
        return processes

    def run_simulation(self):
        try:
            processes = self.get_processes()
            algo = self.algo_var.get()

            if algo == "FCFS":
                segments, comp = schedule_fcfs(processes)
            elif algo == "SJF":
                segments, comp = schedule_sjf(processes)
            elif algo == "Priority":
                segments, comp = schedule_priority(processes)
            elif algo == "Round Robin":
                try:
                    q = int(self.quantum_var.get())
                    if q <= 0: raise ValueError
                except ValueError:
                    raise ValueError("Time Quantum must be a positive integer.")
                segments, comp = schedule_rr(processes, q)

            self.current_segments = segments
            
            wt, tat, util, throughput = calculate_metrics(processes, comp, segments)
            
            self.draw_gantt(segments)
            self.update_metrics_display(wt, tat, util, throughput)

        except ValueError as e:
            messagebox.showwarning("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

    def update_metrics_display(self, wt, tat, util, throughput):
        clear_frame(self.metrics_frame)
        
        avg_wt = sum(wt.values()) / len(wt)
        avg_tat = sum(tat.values()) / len(tat)

        data = [
            ("Average Waiting Time", f"{avg_wt:.2f} ms"),
            ("Average Turnaround Time", f"{avg_tat:.2f} ms"),
            ("CPU Utilization", f"{util:.2f}%"),
            ("System Throughput", f"{throughput:.3f} p/ms")
        ]

        for i, (label, val) in enumerate(data):
            tk.Label(self.metrics_frame, text=label, bg=PANEL, fg=MUTED, font=FONT_SMALL).grid(row=i//2, column=(i%2)*2, sticky="w", padx=(0, 16), pady=8)
            tk.Label(self.metrics_frame, text=val, bg=PANEL, fg=TEXT, font=("Segoe UI Semibold", 12)).grid(row=i//2, column=(i%2)*2+1, sticky="w", padx=(0, 32), pady=8)

    def draw_gantt(self, segments):
        # Clear, scale, and render scheduling timeline visually to the Tk canvas layout
        self.canvas.delete("all")
        if not segments: return
        self.canvas.update_idletasks()
        
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 50 or h < 50: return 

        total_time = max(s[2] for s in segments)
        if total_time == 0: return

        pad_x, pad_y = 20, 30
        draw_w = w - (pad_x * 2)
        box_top = pad_y
        box_bottom = h - pad_y - 20 

        colors = {"P1": "#5D9CEC", "P2": "#48CFAD", "P3": "#FC6E51", "P4": "#FFCE54", "P5": "#AC92EC", 
                  "P6": "#EC87C0", "P7": "#A0D468", "P8": "#4FC1E9", "Idle": "#E6E9ED"}
        
        color_idx = 0
        palette = list(colors.values())[:-1] 

        for pid, start, end in segments:
            if pid not in colors and pid != "Idle":
                colors[pid] = palette[color_idx % len(palette)]
                color_idx += 1

            x1 = pad_x + (start / total_time) * draw_w
            x2 = pad_x + (end / total_time) * draw_w
            
            self.canvas.create_rectangle(x1, box_top, x2, box_bottom, fill=colors.get(pid, "#CCD1D9"), outline="#AAB2BD", width=1)
            
            if x2 - x1 > 25:
                text_color = "#333333" if pid in ["P4", "Idle"] else "#FFFFFF"
                self.canvas.create_text((x1 + x2) / 2, (box_top + box_bottom) / 2, text=pid, font=("Segoe UI Semibold", 10), fill=text_color)
            
            self.canvas.create_line(x1, box_bottom, x1, box_bottom + 8, fill="#AAB2BD")
            self.canvas.create_text(x1, box_bottom + 16, text=str(start), font=("Segoe UI", 8), fill=MUTED)

        self.canvas.create_line(pad_x + draw_w, box_bottom, pad_x + draw_w, box_bottom + 8, fill="#AAB2BD")
        self.canvas.create_text(pad_x + draw_w, box_bottom + 16, text=str(total_time), font=("Segoe UI", 8), fill=MUTED)

    def add_process(self):
        n = len(self.tree.get_children()) + 1
        arr = max([0] + [int(self.tree.item(item, "values")[1]) for item in self.tree.get_children()]) + 1
        self.tree.insert("", "end", values=(f"P{n}", arr, 4, 2))

    def remove_process(self):
        selected = self.tree.selection()
        if selected:
            for item in selected:
                self.tree.delete(item)
        else:
            messagebox.showinfo("Select Process", "Please select a process from the table to remove.")

    def reset_table(self):
        self.tree.delete(*self.tree.get_children())
        defaults = [
            ("P1", 0, 5, 2),
            ("P2", 1, 3, 1),
            ("P3", 2, 8, 3),
            ("P4", 3, 6, 2),
            ("P5", 4, 4, 1)
        ]
        for row in defaults:
            self.tree.insert("", "end", values=row)
            
        self.algo_var.set("Round Robin")
        self.quantum_var.set("2")
        self.on_algo_change()
        self.current_segments = []
        self.canvas.delete("all")
        clear_frame(self.metrics_frame)
        self.run_simulation()