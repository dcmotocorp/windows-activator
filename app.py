import time
import psutil
from win32gui import GetWindowText, GetForegroundWindow
import logging

# Configure logging
logging.basicConfig(
    filename="active_applications.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def get_active_window():
    """Get the title of the currently active window."""
    try:
        return GetWindowText(GetForegroundWindow())
    except Exception as e:
        return f"Error: {e}"

def log_active_application():
    """Logs the active application name and its associated process."""
    print("Tracking active applications. Press Ctrl+C to stop.")
    try:
        while True:
            active_window = get_active_window()
            active_process = None
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['pid'] == GetForegroundWindow():
                    active_process = proc.info['name']
                    break

            log_message = f"Active Window: {active_window} | Active Process: {active_process}"
            logging.info(log_message)  # Save to log file
            print(log_message)  # Display on console

            time.sleep(2)
    except KeyboardInterrupt:
        print("Stopped tracking.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    log_active_application()
