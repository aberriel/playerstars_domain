import os
from time import time, sleep
import sys

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
from multiprocessing import Process


def do_tests():
    os.system('clear')
    cmd = 'make tests' if len(sys.argv) == 1 else sys.argv[1]
    os.system(cmd)


class Watchdog:
    def __init__(self):
        self.last_event_time = time()

    def handle_change(self, event):
        elapsed = time() - self.last_event_time
        self.last_event_time = time()

        if elapsed < 5:
            return

        Process(target=do_tests).start()

    def run(self):
        patterns = ['*.py']
        ignore_patterns = ""
        ignore_directories = False
        case_sensitive = True
        my_event_handler = PatternMatchingEventHandler(patterns,
                                                       ignore_patterns,
                                                       ignore_directories,
                                                       case_sensitive)

        my_event_handler.on_created = self.handle_change
        my_event_handler.on_deleted = self.handle_change
        my_event_handler.on_modified = self.handle_change
        my_event_handler.on_moved = self.handle_change

        path = "."
        go_recursively = True
        my_observer = Observer()
        my_observer.schedule(my_event_handler, path, recursive=go_recursively)

        os.system('clear')
        my_observer.start()
        try:
            while True:
                sleep(1)
        except KeyboardInterrupt:
            my_observer.stop()
            my_observer.join()


if __name__ == "__main__":
    wd = Watchdog()
    wd.run()
