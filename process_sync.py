import customtkinter as ctk
import tkinter as tk
import threading
import time
import random
import queue
import math
from ui_components import BG, FONT_SMALL  

COLOR_THINKING = "#2ECC71"   
COLOR_HUNGRY = "#F39C12"     
COLOR_EATING = "#E74C3C"     
COLOR_FORK_FREE = "#A0AEC0"  

class SmartPhilosopher(threading.Thread):
    def __init__(self, index, left_fork, right_fork, left_id, right_id, msg_queue, app_state):
        super().__init__(daemon=True)
        self.index = index
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.left_id = left_id
        self.right_id = right_id
        self.queue = msg_queue
        self.state = app_state  

    def run(self):
        while not self.state["stop_event"].is_set():
            self.report_state("Thinking")
            self.interruptible_sleep(random.uniform(1.5, 3.5))
            if self.state["stop_event"].is_set(): break

            self.report_state("Hungry")
            
            # sort locks by index to prevent circular wait deadlock
            first_fork, second_fork = sorted(
                [(self.left_fork, self.left_id), (self.right_fork, self.right_id)], 
                key=lambda x: x[1]
            )

            # try acquiring the lower-index fork first
            first_acquired = False
            while not first_acquired and not self.state["stop_event"].is_set():
                self.check_pause()
                if first_fork[0].acquire(timeout=0.1):
                    first_acquired = True
                    self.report_fork(first_fork[1], taken_by=self.index)
                else:
                    time.sleep(0.02)

            if self.state["stop_event"].is_set():
                if first_acquired: first_fork[0].release()
                break

            second_acquired = False
            while not second_acquired and not self.state["stop_event"].is_set():
                self.check_pause()
                if second_fork[0].acquire(timeout=0.1):
                    second_acquired = True
                    self.report_fork(second_fork[1], taken_by=self.index)
                else:
                    time.sleep(0.02)
            
            if self.state["stop_event"].is_set() or not second_acquired:
                if first_acquired: 
                    first_fork[0].release()
                    self.report_fork(first_fork[1], taken_by=None)
                if second_acquired: 
                    second_fork[0].release()
                    self.report_fork(second_fork[1], taken_by=None)
                break

            self.report_state("Eating")
            self.interruptible_sleep(random.uniform(2.0, 4.0))

            # release both resource locks after finishing
            second_fork[0].release()
            self.report_fork(second_fork[1], taken_by=None)
            first_fork[0].release()
            self.report_fork(first_fork[1], taken_by=None)

    def check_pause(self):
        while self.state["pause_event"].is_set() and not self.state["stop_event"].is_set():
            time.sleep(0.05)

    def interruptible_sleep(self, duration):
        elapsed = 0.0
        while elapsed < duration and not self.state["stop_event"].is_set():
            self.check_pause()
            speed_factor = max(0.1, self.state["speed_modifier"].get())
            time.sleep(0.02)
            elapsed += 0.02 * speed_factor

    def report_state(self, current_status):
        self.queue.put(("STATE", self.index, current_status))

    def report_fork(self, fork_index, taken_by):
        self.queue.put(("FORK", fork_index, taken_by))


class ProcessSyncApp(ctk.CTkFrame): 
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=BG, corner_radius=0, **kwargs)
        
        self.app_state = {
            "stop_event": threading.Event(),
            "pause_event": threading.Event(),
            "speed_modifier": tk.DoubleVar(value=1.0)
        }
        self.msg_queue = queue.Queue()
        self.philosopher_threads = []
        self.fork_locks = []
        
        self.current_philo_count = 5
        self.philo_current_states = {}
        self.fork_owners = {}

        self.build_layout_architecture()
        
        self.canvas.bind("<Configure>", lambda e: self.render_canvas_environment())
        self.after(50, self.consume_thread_queue)

    def build_layout_architecture(self):
        title_lbl = ctk.CTkLabel(self, text="Process Synchronization - Dining Philosophers", 
                                 font=("Segoe UI", 18, "bold"), text_color=("#1A2332", "#E2E8F0"))
        title_lbl.pack(anchor="w", padx=24, pady=(15, 10))

        ctrl_card = ctk.CTkFrame(self, height=70, fg_color="white", border_color="#E2E8F0", border_width=1, corner_radius=6)
        ctrl_card.pack(fill="x", side="bottom", padx=24, pady=(10, 20))
        ctrl_card.pack_propagate(False)

        lbl_count = ctk.CTkLabel(ctrl_card, text="Number of Philosophers", font=("Segoe UI", 13), text_color="#1A2332")
        lbl_count.pack(side="left", padx=(20, 10))
        
        self.combo_count = ctk.CTkComboBox(ctrl_card, values=["3", "4", "5", "6", "7", "8"], width=70, state="readonly", command=self.on_config_changed)
        self.combo_count.set("5")
        self.combo_count.pack(side="left", padx=5)
        
        lbl_speed = ctk.CTkLabel(ctrl_card, text="Simulation Speed", font=("Segoe UI", 13), text_color="#1A2332")
        lbl_speed.pack(side="left", padx=(30, 10))
        
        self.slider_speed = ctk.CTkSlider(ctrl_card, from_=0.2, to=3.0, variable=self.app_state["speed_modifier"], width=150)
        self.slider_speed.pack(side="left", padx=5)
        
        self.btn_start = ctk.CTkButton(ctrl_card, text="Start", font=("Segoe UI", 12, "bold"), fg_color="#2ECC71", hover_color="#27AE60", text_color="white", width=80, height=36, command=self.start_simulation)
        self.btn_start.pack(side="right", padx=(5, 20), pady=15)
        
        self.btn_pause = ctk.CTkButton(ctrl_card, text="Pause", font=("Segoe UI", 12, "bold"), fg_color="#F39C12", hover_color="#D35400", text_color="white", width=80, height=36, command=self.pause_simulation, state="disabled")
        self.btn_pause.pack(side="right", padx=5, pady=15)
        
        self.btn_reset = ctk.CTkButton(ctrl_card, text="Reset", font=("Segoe UI", 12, "bold"), fg_color="#7A869A", hover_color="#5A6578", text_color="white", width=80, height=36, command=self.reset_simulation)
        self.btn_reset.pack(side="right", padx=5, pady=15)

        center_workspace = ctk.CTkFrame(self, fg_color="transparent")
        center_workspace.pack(fill="both", expand=True, padx=24, pady=5)

        left_card = ctk.CTkFrame(center_workspace, fg_color="white", border_color="#E2E8F0", border_width=1, corner_radius=6)
        left_card.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.canvas = tk.Canvas(left_card, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=15, pady=15)
        
        right_card = ctk.CTkFrame(center_workspace, width=350, fg_color="white", border_color="#E2E8F0", border_width=1, corner_radius=6)
        right_card.pack(side="right", fill="both", expand=False, padx=(10, 0))
        right_card.pack_propagate(False)

        log_title = ctk.CTkLabel(right_card, text="Log", font=("Segoe UI", 16, "bold"), text_color="#1A2332")
        log_title.pack(anchor="w", padx=16, pady=(15, 5))

        self.log_box = tk.Text(right_card, font=("Consolas", 10), bg="white", fg="#2D3748", relief="flat", highlightthickness=0, wrap="word")
        self.log_box.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        
        self.log_box.tag_config("INFO", foreground="#718096")
        self.log_box.tag_config("Thinking", foreground=COLOR_THINKING, font=("Consolas", 10, "bold"))
        self.log_box.tag_config("Hungry", foreground=COLOR_HUNGRY, font=("Consolas", 10, "bold"))
        self.log_box.tag_config("Eating", foreground=COLOR_EATING, font=("Consolas", 10, "bold"))

    def render_canvas_environment(self):
        # recalculate coordinates and draw nodes in a circular formation
        self.canvas.delete("all")
        self.canvas_nodes = {}
        self.canvas_forks = {}

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 1 or h <= 1: 
            return  

        cx, cy = w / 2, h / 2
        table_r = min(w, h) * 0.28
        philo_node_r = 24

        self.canvas.create_oval(w - 105, 15, w - 95, 25, fill=COLOR_THINKING, outline="")
        self.canvas.create_text(w - 85, 20, text="Thinking", font=("Segoe UI", 10), anchor="w", fill="#718096")
        self.canvas.create_oval(w - 105, 35, w - 95, 45, fill=COLOR_HUNGRY, outline="")
        self.canvas.create_text(w - 85, 40, text="Hungry", font=("Segoe UI", 10), anchor="w", fill="#718096")
        self.canvas.create_oval(w - 105, 55, w - 95, 65, fill=COLOR_EATING, outline="")
        self.canvas.create_text(w - 85, 60, text="Eating", font=("Segoe UI", 10), anchor="w", fill="#718096")

        self.canvas.create_oval(cx - table_r, cy - table_r, cx + table_r, cy + table_r, fill="#F8FAFC", outline="#E2E8F0", width=2)

        n = self.current_philo_count
        step = 2 * math.pi / n

        for i in range(n):
            angle = i * step - (math.pi / 2)
            px = cx + math.cos(angle) * (table_r + 45)
            py = cy + math.sin(angle) * (table_r + 45)

            state = self.philo_current_states.get(i, "Thinking")
            color = COLOR_THINKING if state == "Thinking" else (COLOR_HUNGRY if state == "Hungry" else COLOR_EATING)

            oval = self.canvas.create_oval(px - philo_node_r, py - philo_node_r, px + philo_node_r, py + philo_node_r, fill=color, outline="#CBD5E1", width=1)
            text = self.canvas.create_text(px, py, text=f"P{i+1}", fill="white", font=("Segoe UI", 11, "bold"))
            lbl = self.canvas.create_text(px, py + philo_node_r + 12, text=state, fill=color, font=("Segoe UI", 10))
            
            self.canvas_nodes[i] = {"oval": oval, "text": text, "label": lbl}

            f_angle = angle + (step / 2)
            fx1 = cx + math.cos(f_angle) * (table_r - 20)
            fy1 = cy + math.sin(f_angle) * (table_r - 20)
            fx2 = cx + math.cos(f_angle) * (table_r + 5)
            fy2 = cy + math.sin(f_angle) * (table_r + 5)

            owner = self.fork_owners.get(i, None)
            f_color = COLOR_FORK_FREE if owner is None else COLOR_EATING

            f_line = self.canvas.create_line(fx1, fy1, fx2, fy2, fill=f_color, width=4, capstyle="round")
            self.canvas_forks[i] = {"line": f_line}

        if int(self.log_box.index('end-1c').split('.')[0]) <= 1:
            self.write_log(f"[INFO] Semaphore initialized with {n} forks", "INFO")
            self.write_log("[INFO] Mutex protects each shared fork", "INFO")

    def start_simulation(self):
        self.btn_start.configure(state="disabled", fg_color="#A0AEC0")
        self.btn_pause.configure(state="normal", text="Pause", fg_color="#F39C12", hover_color="#D35400")
        self.combo_count.configure(state="disabled")

        self.app_state["stop_event"].clear()
        self.app_state["pause_event"].clear()

        n = self.current_philo_count
        self.fork_locks = [threading.Lock() for _ in range(n)]
        self.philosopher_threads = []

        for i in range(n):
            p = SmartPhilosopher(i, self.fork_locks[i], self.fork_locks[(i + 1) % n], i, (i + 1) % n, self.msg_queue, self.app_state)
            self.philosopher_threads.append(p)
            p.start()

    def pause_simulation(self):
        if self.app_state["pause_event"].is_set():
            self.app_state["pause_event"].clear()
            self.btn_pause.configure(text="Pause", fg_color="#F39C12", hover_color="#D35400")
        else:
            self.app_state["pause_event"].set()
            self.btn_pause.configure(text="Resume", fg_color="#2ECC71", hover_color="#27AE60")

    def reset_simulation(self):
        self.app_state["stop_event"].set()
        self.app_state["pause_event"].clear()
        
        self.philo_current_states.clear()
        self.fork_owners.clear()
        self.log_box.delete("1.0", tk.END)

        self.btn_start.configure(state="normal", fg_color="#2ECC71", hover_color="#27AE60")
        self.btn_pause.configure(state="disabled", text="Pause", fg_color="#F39C12")
        self.combo_count.configure(state="readonly")
        self.render_canvas_environment()

    def on_config_changed(self, value):
        self.current_philo_count = int(value)
        self.philo_current_states.clear()
        self.fork_owners.clear()
        self.render_canvas_environment()

    def consume_thread_queue(self):
        # parse asynchronous thread queue events to safely update GUI items
        try:
            for _ in range(25):
                msg_data = self.msg_queue.get_nowait()
                msg_type = msg_data[0]

                if msg_type == "STATE":
                    _, idx, state = msg_data
                    self.philo_current_states[idx] = state
                    self.write_log(f"Philosopher {idx + 1} is {state}", state)
                    
                    if idx in self.canvas_nodes:
                        color = COLOR_THINKING if state == "Thinking" else (COLOR_HUNGRY if state == "Hungry" else COLOR_EATING)
                        self.canvas.itemconfig(self.canvas_nodes[idx]["oval"], fill=color)
                        self.canvas.itemconfig(self.canvas_nodes[idx]["label"], text=state, fill=color)

                elif msg_type == "FORK":
                    _, f_idx, owner = msg_data
                    self.fork_owners[f_idx] = owner
                    if f_idx in self.canvas_forks:
                        f_color = COLOR_FORK_FREE if owner is None else COLOR_EATING
                        self.canvas.itemconfig(self.canvas_forks[f_idx]["line"], fill=f_color)
        except queue.Empty:
            pass
        finally:
            if self.winfo_exists():
                self.after(40, self.consume_thread_queue)

    def write_log(self, text, tag):
        self.log_box.insert(tk.END, text + "\n", tag)
        self.log_box.see(tk.END)

    def destroy(self):
        self.app_state["stop_event"].set()
        self.app_state["pause_event"].clear()
        for t in self.philosopher_threads:
            if t.is_alive():
                t.join(timeout=0.01)
        super().destroy()