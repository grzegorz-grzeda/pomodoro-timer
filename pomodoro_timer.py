# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2025 Grzegorz Grzęda
"""
Pomodoro Timer Application

A simple and elegant Pomodoro Timer with current time display,
built using Python and Tkinter.
"""

import tkinter as tk
from datetime import datetime
from tkinter import messagebox


class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("500x450+50+50")
        self.root.resizable(False, False)

        self.root.attributes('-topmost', True)

        self.root.overrideredirect(True)

        self.root.configure(bg='#2c3e50')

        self.offset_x = 0
        self.offset_y = 0

        self.root.bind('<Button-1>', self.start_drag)
        self.root.bind('<B1-Motion>', self.on_drag)

        self.WORK_TIME = 25 * 60
        self.BREAK_TIME = 5 * 60
        self.LONG_BREAK_TIME = 15 * 60

        self.time_remaining = self.WORK_TIME
        self.is_running = False
        self.is_work_session = True
        self.pomodoro_count = 0
        self.timer_id = None

        self.current_time_label = tk.Label(
            root,
            font=('Arial', 14),
            bg='#2c3e50',
            fg='#95a5a6',
            text="Current Time"
        )
        self.current_time_label.pack(pady=(10, 0))

        self.time_label = tk.Label(
            root,
            font=('Arial', 18, 'bold'),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        self.time_label.pack(pady=(0, 20))

        tk.Frame(root, height=2, bg='#34495e').pack(fill=tk.X, padx=20)

        self.status_label = tk.Label(
            root,
            text="WORK SESSION",
            font=('Arial', 16, 'bold'),
            bg='#2c3e50',
            fg='#27ae60'
        )
        self.status_label.pack(pady=15)

        self.counter_label = tk.Label(
            root,
            text="Pomodoros: 0",
            font=('Arial', 12),
            bg='#2c3e50',
            fg='#95a5a6'
        )
        self.counter_label.pack()

        self.timer_label = tk.Label(
            root,
            font=('Arial', 48, 'bold'),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        self.timer_label.pack(pady=20)

        button_frame = tk.Frame(root, bg='#2c3e50')
        button_frame.pack(pady=20)

        self.start_pause_button = tk.Button(
            button_frame,
            text="Start",
            command=self.toggle_timer,
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            activebackground='#229954',
            activeforeground='white',
            cursor='hand2',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            width=10
        )
        self.start_pause_button.grid(row=0, column=0, padx=5)

        self.reset_button = tk.Button(
            button_frame,
            text="Reset",
            command=self.reset_timer,
            font=('Arial', 12, 'bold'),
            bg='#f39c12',
            fg='white',
            activebackground='#e67e22',
            activeforeground='white',
            cursor='hand2',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            width=10
        )
        self.reset_button.grid(row=0, column=1, padx=5)

        self.skip_button = tk.Button(
            button_frame,
            text="Skip",
            command=self.skip_session,
            font=('Arial', 12, 'bold'),
            bg='#9b59b6',
            fg='white',
            activebackground='#8e44ad',
            activeforeground='white',
            cursor='hand2',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            width=10
        )
        self.skip_button.grid(row=0, column=2, padx=5)

        self.close_button = tk.Button(
            root,
            text="Close",
            command=self.close_app,
            font=('Arial', 12),
            bg='#e74c3c',
            fg='white',
            activebackground='#c0392b',
            activeforeground='white',
            cursor='hand2',
            relief=tk.FLAT,
            padx=20,
            pady=5
        )
        self.close_button.pack(pady=10)

        self.update_timer_display()
        self.update_time()

    def start_drag(self, event):
        """Record the starting position for window dragging"""
        self.offset_x = event.x
        self.offset_y = event.y

    def on_drag(self, event):
        """Move the window while dragging"""
        x = self.root.winfo_x() + event.x - self.offset_x
        y = self.root.winfo_y() + event.y - self.offset_y
        self.root.geometry(f'+{x}+{y}')

    def update_time(self):
        """Update the current time label every second"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

    def update_timer_display(self):
        """Update the pomodoro timer display"""
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")

    def toggle_timer(self):
        """Start or pause the timer"""
        self.is_running = not self.is_running
        if self.is_running:
            self.start_pause_button.config(text="Pause", bg='#e67e22')
            self.run_timer()
        else:
            self.start_pause_button.config(text="Resume", bg='#27ae60')
            if self.timer_id:
                self.root.after_cancel(self.timer_id)

    def run_timer(self):
        """Run the pomodoro timer countdown"""
        if self.is_running and self.time_remaining > 0:
            self.time_remaining -= 1
            self.update_timer_display()
            self.timer_id = self.root.after(1000, self.run_timer)
        elif self.is_running and self.time_remaining == 0:
            self.timer_complete()

    def timer_complete(self):
        """Handle timer completion"""
        self.is_running = False
        self.start_pause_button.config(text="Start", bg='#27ae60')

        if self.is_work_session:
            self.pomodoro_count += 1
            self.counter_label.config(text=f"Pomodoros: {self.pomodoro_count}")
            messagebox.showinfo("Pomodoro Complete!",
                                "Great work! Time for a break.")

            self.is_work_session = False
            if self.pomodoro_count % 4 == 0:
                self.time_remaining = self.LONG_BREAK_TIME
                self.status_label.config(text="LONG BREAK", fg='#9b59b6')
            else:
                self.time_remaining = self.BREAK_TIME
                self.status_label.config(text="SHORT BREAK", fg='#3498db')
        else:
            messagebox.showinfo("Break Complete!",
                                "Break's over! Ready to focus again?")
            self.is_work_session = True
            self.time_remaining = self.WORK_TIME
            self.status_label.config(text="WORK SESSION", fg='#27ae60')

        self.update_timer_display()

    def reset_timer(self):
        """Reset the timer to initial state"""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        self.is_running = False
        self.is_work_session = True
        self.time_remaining = self.WORK_TIME

        self.start_pause_button.config(text="Start", bg='#27ae60')
        self.status_label.config(text="WORK SESSION", fg='#27ae60')
        self.update_timer_display()

    def skip_session(self):
        """Skip the current session and move to the next state"""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        self.is_running = False
        self.start_pause_button.config(text="Start", bg='#27ae60')

        if self.is_work_session:
            self.pomodoro_count += 1
            self.counter_label.config(text=f"Pomodoros: {self.pomodoro_count}")

            self.is_work_session = False
            if self.pomodoro_count % 4 == 0:
                self.time_remaining = self.LONG_BREAK_TIME
                self.status_label.config(text="LONG BREAK", fg='#9b59b6')
            else:
                self.time_remaining = self.BREAK_TIME
                self.status_label.config(text="SHORT BREAK", fg='#3498db')
        else:
            self.is_work_session = True
            self.time_remaining = self.WORK_TIME
            self.status_label.config(text="WORK SESSION", fg='#27ae60')

        self.update_timer_display()

    def close_app(self):
        """Close the application"""
        self.root.destroy()


def main():
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
