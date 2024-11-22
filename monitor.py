import time
import psutil
from win32gui import GetWindowText, GetForegroundWindow
from app_scraper import scrape_data

def get_active_window():
    """Get the title of the currently active window."""
    try:
        return GetWindowText(GetForegroundWindow())
    except Exception as e:
        return f"Error: {e}"

def monitor_applications():
    """Monitors active applications and triggers scraping."""
    print("Starting monitoring service. Press Ctrl+C to stop.")
    last_active_app = None

    try:
        while True:
            active_window = get_active_window()
            if active_window != last_active_app:
                last_active_app = active_window
                print(f"Switched to: {active_window}")
                
                # Find active process name
                active_process = None
                for proc in psutil.process_iter(['pid', 'name']):
                    if proc.info['pid'] == GetForegroundWindow():
                        active_process = proc.info['name']
                        break
                
                # Call scraper logic for the active application
                scrape_data(active_window, active_process)
            
            time.sleep(2)
    except KeyboardInterrupt:
        print("Stopping monitoring service.")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    monitor_applications()
