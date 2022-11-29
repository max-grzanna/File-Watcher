import sys
import time
import logging
from watchdog.observers import Observer  
from watchdog.events import LoggingEventHandler
from watchdog.events import PatternMatchingEventHandler

def on_created(event):
    print(f"hey, {event.src_path} has been created!")
 
def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!")
 
def on_modified(event):
    print(f"hey buddy, {event.src_path} has been modified")

def on_moved(event):
    print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")



if __name__ == "__main__":


    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved


    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(my_event_handler, path, recursive=True)  #Scheduling monitoring of a path with the observer instance and event handler. There is 'recursive=True' because only with it enabled, watchdog.observers.Observer can monitor sub-directories
    observer.start()  #for starting the observer thread
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
