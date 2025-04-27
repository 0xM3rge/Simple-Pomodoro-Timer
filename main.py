#!/usr/bin/env python3

import argparse
import time
import os
import json
import signal
import sys
from datetime import datetime, timedelta

# Constants
DEFAULT_WORK_TIME = 25  # minutes
DEFAULT_SHORT_BREAK = 5  # minutes
DEFAULT_LONG_BREAK = 15  # minutes
DEFAULT_CYCLES = 4
CONFIG_FILE = os.path.expanduser("~/.pomodoro_stats.json")

# Global variables
running = True
paused = False

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def format_time(seconds):
    """Format seconds into minutes and seconds"""
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"

def save_stats(session_type, duration_minutes):
    """Save session statistics"""
    stats = load_stats()
    
    today = datetime.now().strftime("%Y-%m-%d")
    if today not in stats:
        stats[today] = {
            "work": 0,
            "short_break": 0,
            "long_break": 0,
            "completed_cycles": 0
        }
    
    stats[today][session_type] += duration_minutes
    if session_type == "work":
        stats[today]["completed_cycles"] += 1
    
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(stats, f)
    except:
        pass  # Ignore errors when saving stats

def load_stats():
    """Load session statistics"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

def show_stats():
    """Display pomodoro statistics"""
    stats = load_stats()
    if not stats:
        print("No pomodoro statistics available yet.")
        return
    
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    print("\n=== Pomodoro Statistics ===\n")
    
    if today in stats:
        today_stats = stats[today]
        print(f"Today ({today}):")
        print(f"  Work time: {today_stats['work']} minutes")
        print(f"  Short breaks: {today_stats['short_break']} minutes")
        print(f"  Long breaks: {today_stats['long_break']} minutes")
        print(f"  Completed cycles: {today_stats['completed_cycles']}")
    
    if yesterday in stats:
        yesterday_stats = stats[yesterday]
        print(f"\nYesterday ({yesterday}):")
        print(f"  Work time: {yesterday_stats['work']} minutes")
        print(f"  Completed cycles: {yesterday_stats['completed_cycles']}")
    
    # Calculate total stats
    total_work = sum(day["work"] for day in stats.values())
    total_cycles = sum(day["completed_cycles"] for day in stats.values())
    
    print(f"\nAll time:")
    print(f"  Total work time: {total_work} minutes")
    print(f"  Total completed cycles: {total_cycles}")
    print(f"  Total days: {len(stats)}")

def signal_handler(sig, frame):
    """Handle Ctrl+C"""
    global running, paused
    
    if paused:
        # If already paused, exit
        print("\nExiting Pomodoro Timer")
        running = False
    else:
        # Pause timer
        paused = True
        print("\nTimer paused. Press Enter to resume or Ctrl+C again to exit.")

def start_timer(duration, session_type, cycle=None, total_cycles=None):
    """Start a countdown timer"""
    global running, paused
    
    signal.signal(signal.SIGINT, signal_handler)
    
    end_time = time.time() + duration
    
    while running and time.time() < end_time:
        if paused:
            # When paused, wait for user input
            try:
                input()
                paused = False
                # Recalculate end time
                end_time = time.time() + (end_time - time.time())
            except KeyboardInterrupt:
                # Exit on second Ctrl+C
                print("\nExiting Pomodoro Timer")
                running = False
                break
        
        # Calculate remaining time
        remaining = int(end_time - time.time())
        if remaining < 0:
            break
        
        # Display timer
        clear_screen()
        
        if session_type == "work":
            print(f"🍅 WORK SESSION {cycle}/{total_cycles} 🍅")
        elif session_type == "short_break":
            print(f"☕ SHORT BREAK {cycle}/{total_cycles} ☕")
        else:
            print(f"🌴 LONG BREAK 🌴")
        
        print(f"\nTime remaining: {format_time(remaining)}")
        print("\nPress Ctrl+C to pause/exit")
        
        time.sleep(1)
    
    # Save statistics when session completes successfully
    if running and not paused:
        save_stats(session_type, duration // 60)
        
        # Play notification sound if available
        if os.name == 'posix':  # Unix/Linux/MacOS
            os.system('tput bel')  # Terminal bell
        elif os.name == 'nt':  # Windows
            os.system('echo \a')  # Terminal bell
        
        clear_screen()
        if session_type == "work":
            print(f"✅ Work session {cycle}/{total_cycles} completed!")
        elif session_type == "short_break":
            print(f"✅ Short break completed! Get ready to work!")
        else:
            print(f"✅ Long break completed! Ready for a new cycle?")
        
        for i in range(5, 0, -1):
            print(f"Next session starts in {i} seconds...", end='\r')
            time.sleep(1)
        
        clear_screen()

def run_pomodoro(work_time, short_break, long_break, cycles):
    """Run a full pomodoro session"""
    for cycle in range(1, cycles + 1):
        # Work session
        start_timer(work_time * 60, "work", cycle, cycles)
        if not running:
            break
        
        # Break (short or long)
        if cycle < cycles:
            start_timer(short_break * 60, "short_break", cycle, cycles)
        else:
            start_timer(long_break * 60, "long_break")
        
        if not running:
            break
    
    if running:
        clear_screen()
        print("🎉 Pomodoro session completed! 🎉")
        print("\nStatistics for this session:")
        print(f"  Work time: {work_time * cycles} minutes")
        print(f"  Break time: {short_break * (cycles - 1) + long_break} minutes")
        print(f"  Completed cycles: {cycles}")

def main():
    parser = argparse.ArgumentParser(description="Simple Pomodoro Timer")
    
    parser.add_argument("-w", "--work", type=int, default=DEFAULT_WORK_TIME,
                       help=f"Work session duration in minutes (default: {DEFAULT_WORK_TIME})")
    parser.add_argument("-s", "--short-break", type=int, default=DEFAULT_SHORT_BREAK,
                       help=f"Short break duration in minutes (default: {DEFAULT_SHORT_BREAK})")
    parser.add_argument("-l", "--long-break", type=int, default=DEFAULT_LONG_BREAK,
                       help=f"Long break duration in minutes (default: {DEFAULT_LONG_BREAK})")
    parser.add_argument("-c", "--cycles", type=int, default=DEFAULT_CYCLES,
                       help=f"Number of work cycles (default: {DEFAULT_CYCLES})")
    parser.add_argument("--stats", action="store_true", help="Show pomodoro statistics")
    
    args = parser.parse_args()
    
    if args.stats:
        show_stats()
        return
    
    try:
        run_pomodoro(args.work, args.short_break, args.long_break, args.cycles)
    except KeyboardInterrupt:
        print("\nPomodoro Timer stopped.")

if __name__ == "__main__":
    main()
