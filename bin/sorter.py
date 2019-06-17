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

#Filepaths
src = "/home/mrmxyzptlyk/shows/downloads/"
dst = "/home/mrmxyzptlyk/shows/new/"
showList = []

#Set mrmxyzptlyk permissions.
uid = 1000
gid = 1000

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
                #start_run()
                #extracter(src + new_asset)
    
        #elif event.event_type == 'modified':
        #    # Taken any action here when a file is modified.
        #    print("Received modified event - %s." % event.src_path)

def extracter(loc):
    #If file, move else look for .video extention, else look for rar.
    #Extract, write to file.

    if loc is os.path.isfile():
        logger.info('Moving %s...' % (loc))
        src_file = loc.split("/")[-1]
        dst_file=dst + '/' + src_file
        shutil.copyfile(loc,dst_file)
    else:
        folder = os.path.abspath(loc)
        for foldername,subfolders,filenames in os.walk(folder):
            for filename in filenames:
                if filename.endswith('.mkv') or filename.endswith('.flv') or filename.endswith('.mov') or filename.endswith('.mp4'):
                    logger.info('Moving %s...' % (filename))
        src_file = loc.split("/")[-1]
        dst_file=dst + '/' + src_file
        shutil.copyfile(loc,dst_file)

        

def start_run():
    #Call the unrarer script.
    cmd = 'python3 /home/mrmxyzptlyk/python/sorter/bin/folder.py'
    p = subprocess.Popen(cmd,  shell=True)
    #Wait for proc to return. Then run next.
    p.communicate()

def main():
    #start_run()

    w = Watcher()
    w.run()

if __name__ == '__main__':
    main()
