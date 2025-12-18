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

APP_TITLE="Pomodoro Timer"
APP_GEOMETRY="400x370+50+50"

APP_BG_COLOR = "#2c3e50"

WORK_TEXT = "WORK"
SHORT_BREAK_TEXT = "SHORT BREAK"
LONG_BREAK_TEXT = "LONG BREAK"

WORK_TIME = 25 * 60  # 25 minutes
BREAK_TIME = 5 * 60  # 5 minutes
LONG_BREAK_TIME = 15 * 60  # 15 minutes

# Color constants
COLOR_WORK = '#27ae60'
COLOR_SHORT_BREAK = '#3498db'
COLOR_LONG_BREAK = '#9b59b6'
COLOR_START_BUTTON = '#27ae60'
COLOR_START_BUTTON_ACTIVE = '#229954'
COLOR_PAUSE_BUTTON = '#e67e22'
COLOR_RESET_BUTTON = '#f39c12'
COLOR_RESET_BUTTON_ACTIVE = '#e67e22'
COLOR_SKIP_BUTTON = '#9b59b6'
COLOR_SKIP_BUTTON_ACTIVE = '#8e44ad'
COLOR_CLOSE_BUTTON = '#e74c3c'
COLOR_CLOSE_BUTTON_ACTIVE = '#c0392b'
COLOR_TEXT_PRIMARY = '#ecf0f1'
COLOR_TEXT_SECONDARY = '#95a5a6'
COLOR_DIVIDER = '#34495e'

# Font constants
FONT_FAMILY = 'Arial'
FONT_SIZE_TIME = 14
FONT_SIZE_STATUS = 14
FONT_SIZE_TIMER = 40
FONT_SIZE_COUNTER = 10
FONT_SIZE_BUTTON = 12

# Timing constants (milliseconds)
CLOCK_UPDATE_INTERVAL = 250
TIMER_UPDATE_INTERVAL = 1000

# Layout constants
PADDING_TOP = 10
PADDING_BOTTOM = 20
PADDING_BUTTON_FRAME = 20
PADDING_BUTTON = 5
PADDING_STATUS = 5
PADDING_TIMER = 5
PADDING_DIVIDER = 10
DIVIDER_HEIGHT = 1
BUTTON_WIDTH = 5
BUTTON_PADX = 20
BUTTON_PADY = 5

# Pomodoro cycle
LONG_BREAK_CYCLE = 4

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(APP_GEOMETRY)
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        self.root.configure(bg=APP_BG_COLOR)

        self.offset_x = 0
        self.offset_y = 0

        self.root.bind('<Button-1>', self.start_drag)
        self.root.bind('<B1-Motion>', self.on_drag)

        self.WORK_TIME = WORK_TIME
        self.BREAK_TIME = BREAK_TIME
        self.LONG_BREAK_TIME = LONG_BREAK_TIME

        self.time_remaining = self.WORK_TIME
        self.is_running = False
        self.is_work_session = True
        self.pomodoro_count = 0
        self.timer_id = None

        self._create_ui()
        self.update_timer_display()
        self.update_time()

    def _create_ui(self):
        """Create all UI elements"""
        self._create_time_display()
        self._create_timer_display()
        self._create_buttons()

    def _create_time_display(self):
        """Create the current time display section"""
        self.current_time_label = tk.Label(
            self.root,
            font=(FONT_FAMILY, FONT_SIZE_TIME),
            bg=APP_BG_COLOR,
            fg=COLOR_TEXT_SECONDARY,
            text="Current Time"
        )
        self.current_time_label.pack(pady=(PADDING_TOP, 0))

        self.time_label = tk.Label(
            self.root,
            font=(FONT_FAMILY, FONT_SIZE_TIME, 'bold'),
            bg=APP_BG_COLOR,
            fg=COLOR_TEXT_PRIMARY
        )
        self.time_label.pack(pady=(0, PADDING_BOTTOM))

        tk.Frame(self.root, height=DIVIDER_HEIGHT, bg=COLOR_DIVIDER).pack(fill=tk.X, padx=PADDING_DIVIDER)

    def _create_timer_display(self):
        """Create the pomodoro timer display section"""
        self.status_label = tk.Label(
            self.root,
            text=WORK_TEXT,
            font=(FONT_FAMILY, FONT_SIZE_STATUS, 'bold'),
            bg=APP_BG_COLOR,
            fg=COLOR_WORK
        )
        self.status_label.pack(pady=PADDING_STATUS)

        self.timer_label = tk.Label(
            self.root,
            font=(FONT_FAMILY, FONT_SIZE_TIMER, 'bold'),
            bg=APP_BG_COLOR,
            fg=COLOR_TEXT_PRIMARY
        )
        self.timer_label.pack(pady=PADDING_TIMER)

        self.counter_label = tk.Label(
            self.root,
            text="Pomodoros: 0",
            font=(FONT_FAMILY, FONT_SIZE_COUNTER),
            bg=APP_BG_COLOR,
            fg=COLOR_TEXT_SECONDARY
        )
        self.counter_label.pack()

    def _create_buttons(self):
        """Create all control buttons"""
        button_frame = tk.Frame(self.root, bg=APP_BG_COLOR)
        button_frame.pack(pady=PADDING_BUTTON_FRAME)

        self.start_pause_button = self._create_button(
            button_frame, "Start", self.toggle_timer, COLOR_START_BUTTON, COLOR_START_BUTTON_ACTIVE
        )
        self.start_pause_button.grid(row=0, column=0, padx=PADDING_BUTTON)

        self.reset_button = self._create_button(
            button_frame, "Reset", self.reset_timer, COLOR_RESET_BUTTON, COLOR_RESET_BUTTON_ACTIVE
        )
        self.reset_button.grid(row=0, column=1, padx=PADDING_BUTTON)

        self.skip_button = self._create_button(
            button_frame, "Skip", self.skip_session, COLOR_SKIP_BUTTON, COLOR_SKIP_BUTTON_ACTIVE
        )
        self.skip_button.grid(row=0, column=2, padx=PADDING_BUTTON)

        self.close_button = self._create_button(
            self.root, "Close", self.close_app, COLOR_CLOSE_BUTTON, COLOR_CLOSE_BUTTON_ACTIVE
        )
        self.close_button.pack(pady=0)

    def _create_button(self, parent, text, command, bg_color, active_bg):
        """Create a styled button with common properties"""
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=(FONT_FAMILY, FONT_SIZE_BUTTON, 'bold'),
            bg=bg_color,
            fg='white',
            activebackground=active_bg,
            activeforeground='white',
            cursor='hand2',
            relief=tk.FLAT,
            padx=BUTTON_PADX,
            pady=BUTTON_PADY,
            width=BUTTON_WIDTH
        )

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
        self.root.after(CLOCK_UPDATE_INTERVAL, self.update_time)

    def update_timer_display(self):
        """Update the pomodoro timer display"""
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")

    def toggle_timer(self):
        """Start or pause the timer"""
        self.is_running = not self.is_running
        if self.is_running:
            self.start_pause_button.config(text="Pause", bg=COLOR_PAUSE_BUTTON)
            self.run_timer()
        else:
            self.start_pause_button.config(text="Resume", bg=COLOR_START_BUTTON)
            if self.timer_id:
                self.root.after_cancel(self.timer_id)

    def run_timer(self):
        """Run the pomodoro timer countdown"""
        if self.is_running and self.time_remaining > 0:
            self.time_remaining -= 1
            self.update_timer_display()
            self.timer_id = self.root.after(TIMER_UPDATE_INTERVAL, self.run_timer)
        elif self.is_running and self.time_remaining == 0:
            self.timer_complete()

    def timer_complete(self):
        """Handle timer completion"""
        self._stop_timer()

        if self.is_work_session:
            self._complete_work_session()
        else:
            self._complete_break_session()

        self.update_timer_display()

    def _stop_timer(self):
        """Stop the timer and reset the start button"""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.is_running = False
        self.start_pause_button.config(text="Start", bg=COLOR_START_BUTTON)

    def _complete_work_session(self):
        """Complete a work session and start a break"""
        self.pomodoro_count += 1
        self.counter_label.config(text=f"Pomodoros: {self.pomodoro_count}")
        messagebox.showinfo("Pomodoro Complete!", "Great work! Time for a break.")
        self._transition_to_break()

    def _complete_break_session(self):
        """Complete a break session and start work"""
        messagebox.showinfo("Break Complete!", "Break's over! Ready to focus again?")
        self._transition_to_work()

    def _transition_to_break(self):
        """Transition from work to break state"""
        self.is_work_session = False
        if self.pomodoro_count % LONG_BREAK_CYCLE == 0:
            self._set_timer_state(self.LONG_BREAK_TIME, LONG_BREAK_TEXT, COLOR_LONG_BREAK)
        else:
            self._set_timer_state(self.BREAK_TIME, SHORT_BREAK_TEXT, COLOR_SHORT_BREAK)

    def _transition_to_work(self):
        """Transition from break to work state"""
        self.is_work_session = True
        self._set_timer_state(self.WORK_TIME, WORK_TEXT, COLOR_WORK)

    def _set_timer_state(self, time, status_text, status_color):
        """Set the timer to a specific state"""
        self.time_remaining = time
        self.status_label.config(text=status_text, fg=status_color)

    def reset_timer(self):
        """Reset the timer to initial state"""
        self._stop_timer()
        self._transition_to_work()
        self.update_timer_display()

    def skip_session(self):
        """Skip the current session and move to the next state"""
        self._stop_timer()

        if self.is_work_session:
            self.pomodoro_count += 1
            self.counter_label.config(text=f"Pomodoros: {self.pomodoro_count}")
            self._transition_to_break()
        else:
            self._transition_to_work()

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
