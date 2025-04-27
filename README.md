# 🍅 Simple Pomodoro Timer

A command-line Pomodoro Timer to help you stay productive by managing work and break cycles.

## ✨ Features

- ⏱️ Customizable work and break durations
- 🔄 Multiple work cycles with short and long breaks
- ⏸️ Pause and resume functionality
- 📊 Track and display productivity statistics
- 🔔 Notifications when sessions end
- 📈 View daily and all-time statistics

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/pomodoro-timer.git
cd pomodoro-timer
```

2. Make the script executable (Unix/Linux/macOS):
```bash
chmod +x main.py
```

## 🔍 Usage

```bash
python main.py [options]
```

## ⚙️ Options

- `-w, --work`: Work session duration in minutes (default: 25)
- `-s, --short-break`: Short break duration in minutes (default: 5)
- `-l, --long-break`: Long break duration in minutes (default: 15)
- `-c, --cycles`: Number of work cycles (default: 4)
- `--stats`: Show pomodoro statistics

## 📝 Examples

### Start with default settings (25-5-15-4):
```bash
python main.py
```

### Customize work and break durations:
```bash
python main.py -w 30 -s 10 -l 20
```

### Set number of cycles:
```bash
python main.py -c 2
```

### View your productivity statistics:
```bash
python main.py --stats
```

## 🔄 How It Works

The Pomodoro Technique is a time management method that uses a timer to break work into intervals, traditionally 25 minutes in length, separated by short breaks. After four pomodoro sessions, you take a longer break.

1. **Work Session**: Focus on a task for 25 minutes
2. **Short Break**: Take a 5-minute break
3. **Repeat**: Continue this cycle
4. **Long Break**: After completing 4 work sessions, take a longer 15-minute break

This tool follows this pattern and lets you customize the durations to fit your workflow.

## 🎮 Controls

- **Ctrl+C**: Pause the timer / Exit when paused
- **Enter**: Resume when paused

## 📊 Statistics

The timer keeps track of your productivity:
- Today's work time and breaks
- Yesterday's work time
- Total work time across all days
- Number of completed cycles
- Total number of days you've used the timer

Statistics are stored in `~/.pomodoro_stats.json` on your system.

