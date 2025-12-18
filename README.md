# Pomodoro Timer

A simple and elegant Pomodoro Timer application built with Python and Tkinter.

![Pomodoro timer](/docs/img/image.png)

## Features

- **Current Time Display**: Shows the current system time at the top of the window
- **Pomodoro Timer**: Classic 25-minute work sessions
- **Break Management**: 
  - 5-minute short breaks after each work session
  - 15-minute long breaks after every 4 pomodoros
- **Session Tracking**: Counts completed pomodoro sessions
- **Always On Top**: Window stays visible above all other applications
- **Visual Feedback**: Color-coded status indicators for work and break sessions
- **Notifications**: Pop-up alerts when sessions complete
- **Control Buttons**: 
  - Start/Pause timer
  - Reset current session
  - Close application

## Requirements

- Python 3.x
- Tkinter (included with standard Python installation)

## Installation

No additional packages are required! Tkinter comes pre-installed with Python.

```bash
# Clone the repository
git clone <repository-url>
cd pomodoro-timer-python

# Run the application
python clock_app.py
```

## Usage

1. **Start a Work Session**: Click the "Start" button to begin a 25-minute work session
2. **Pause/Resume**: Click "Pause" to pause the timer, then "Resume" to continue
3. **Reset**: Click "Reset" to restart the current session
4. **Automatic Transitions**: The app automatically switches between work and break sessions
5. **Track Progress**: See your completed pomodoro count at the top of the timer

## The Pomodoro Technique

The Pomodoro Technique is a time management method that uses a timer to break work into intervals:

1. Work for 25 minutes (1 pomodoro)
2. Take a 5-minute short break
3. After 4 pomodoros, take a 15-minute long break
4. Repeat!

## Screenshots

The app features a modern dark theme with:
- Green for work sessions
- Blue for short breaks
- Purple for long breaks

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues and enhancement requests!
