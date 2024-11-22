from pywinauto import Application
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pyautogui
import pytesseract
from docx import Document
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def scrape_data(window_title, process_name):
    """
    Scrape data based on the active application.
    """
    if not process_name:
        print(f"Unknown process for window: {window_title}")
        return

    print(f"Scraping data for process: {process_name} (Window: {window_title})")

    if "chrome" in process_name.lower():
        scrape_chrome(window_title)
    elif "notepad" in process_name.lower():
        scrape_notepad(window_title)
    else:
        print(f"No scraper defined for process: {process_name}")

def scrape_chrome(window_title):
    """Scrape data from Chrome."""
    print(f"Scraping Chrome data for tab: {window_title}")
    # Example: Use Chrome Debugging Protocol or browser extensions to fetch data.

    # Set up ChromeDriver
    service = Service("path/to/chromedriver")
    driver = webdriver.Chrome(service=service)

    # Attach to an existing Chrome session (requires debugging enabled)
    driver.get("http://localhost:9222/json")  # Ensure Chrome is launched with --remote-debugging-port=9222
    tabs = driver.find_elements(By.CSS_SELECTOR, "body *")
    
    for tab in tabs:
        print(tab.text)

    driver.quit()

def scrape_notepad(window_title):
    """Scrape data from Notepad."""
    print(f"Scraping Notepad content for: {window_title}")
    # Example: Check for file changes or capture content.
    capture_notepad_content()



def capture_notepad_content():
    """Capture content from Notepad."""
    try:
        app = Application(backend="uia").connect(title_re=".*Notepad")
        edit = app.window(title_re=".*Notepad").child_window(control_type="Edit")
        content = edit.get_value()
        print(f"Captured Content:\n{content}")
        return content
    except Exception as e:
        print(f"Error capturing Notepad content: {e}")
        return None




def capture_window_text():
    """Capture text from the active window using OCR."""
    screenshot = pyautogui.screenshot()
    text = pytesseract.image_to_string(screenshot)
    print(f"Captured Text:\n{text}")
    return text


def read_word_document(file_path):
    """Read content from a Word document."""
    doc = Document(file_path)
    for paragraph in doc.paragraphs:
        print(paragraph.text)






class FileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f"File modified: {event.src_path}")

# observer = Observer()
# observer.schedule(FileHandler(), path="path/to/watch", recursive=True)
# observer.start()

# try:
#     while True:
#         pass
# except KeyboardInterrupt:
#     observer.stop()
# observer.join()
