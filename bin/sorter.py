#!/usr/bin/python3
#Trigger event when new file is added to downloads folder.

import time
import logging
import configparser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
from time import sleep
import sys

config = configparser.ConfigParser()
config.read("/home/mrmxyzptlyk/python/sorter/conf/sorter.ini")

#Create a logger.
#Load initial values from config..
logging.basicConfig(filename=config['log']['filename'],format='%(asctime)s::%(levelname)s::%(funcName)s::%(message)s')
logger = logging.getLogger('sorter')
logger.setLevel(config['log']['level'])

src = "/home/mrmxyzptlyk/shows/downloads/"
showList = []

class Watcher:
    src = "/home/mrmxyzptlyk/shows/downloads/"
    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.src, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
                showList = []
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            logging.info("Directory created: ")
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            new_asset = event.src_path.split("/")[5]
            if new_asset not in showList:
                showList.append(new_asset)
                
                logger.info("Received created event: %s" % new_asset)
    
                #call script to untar. 
                #cmd = 'python3 /home/mrmxyzptlyk/python/sorter/bin/un.py ' + new_asset
                cmd = 'python3 ~/python/sorter/bin/folder.py'
                
                p = subprocess.Popen(cmd,  shell=True)
                #Wait for proc to return. Then run next. 
                p.communicate()
    
        #elif event.event_type == 'modified':
        #    # Taken any action here when a file is modified.
        #    print("Received modified event - %s." % event.src_path)


def main():
    w = Watcher()
    w.run()

if __name__ == '__main__':
    main()
