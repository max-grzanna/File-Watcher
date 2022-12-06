import time
import logging
import os
import ocrmypdf
import tomllib
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import PatternMatchingEventHandler

with open("config.toml", "rb") as f:
    data = tomllib.load(f)

ORIGIN_DIR = data["general"]["origin_path"]
DEST_DIR = data["general"]["destination_path"]
DESKEW = data["ocr"]["deskew"]
CLEAN = data["ocr"]["clean"]
CLEAN_FINAL = data["ocr"]["clean_final"]


def sanitize_path(path: str):
    # Some apps tend to append their name to the scanned documents
    print("input string:", path)
    string_to_delete = "_QuickScan"
    file_name = path.split("/")[-1]
    print("filename: ", file_name)

    if string_to_delete in file_name:
        print("Changing filename...")
        altered_filename = file_name.replace(string_to_delete, "")
        os.rename(path, ORIGIN_DIR + altered_filename)
        print("altered: ")
        return altered_filename

    return file_name


def ocr_file(filename: str):
    time.sleep(2)
    # TODO: Check if file is ready after creating

    origin = ORIGIN_DIR + filename
    destination = DEST_DIR + filename
    ocrmypdf.ocr(origin, destination, deskew=DESKEW, clean=CLEAN, clean_final=CLEAN_FINAL)


def on_created(event):
    print(f"{event.src_path} has been created!")
    file_name = sanitize_path(event.src_path)

    try:
        ocr_file(file_name)
    except:
        print("Error occurred while ocr-ing file.")


if __name__ == "__main__":

    PATTERNS = ["*"]
    IGNORE_PATTERNS = None
    IGNORE_DIRECTORIES = False
    CASE_SENSITIVE = True
    my_event_handler = PatternMatchingEventHandler(
        PATTERNS, IGNORE_PATTERNS, IGNORE_DIRECTORIES, CASE_SENSITIVE
    )

    my_event_handler.on_created = on_created

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(my_event_handler, ORIGIN_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
