#!/usr/bin/python3
#Unrar files under /home//shows/downloads/ and move them to the /home//shows/new folder

#Todo:
#Use move instead of copy after unraring files in downloads folder.
#Create a seperate function for individual files or folders being passed as args.

import logging
import os, shutil, pwd, grp, time, datetime
from unrar import rarfile
import configparser

src = '/home/mrmxyzptlyk/shows/downloads/'
dst = '/home/mrmxyzptlyk/shows/new/'
srt = '/home/mrmxyzptlyk/shows/sorting/'

uid = 1000
gid = 1000

#Create config reader object
config = configparser.ConfigParser()
config.read("/home/mrmxyzptlyk/python/sorter/conf/sorter.ini")
 
#Create a logger.
#Load initial values from config..
logging.basicConfig(filename=config['log']['filename'],format='%(asctime)s::%(levelname)s::%(funcName)s::%(message)s')
logger = logging.getLogger('sorter')
logger.setLevel(config['log']['level'])


def unrarer(folder):
    folder = os.path.abspath(folder)
    for foldername,subfolders,filenames in os.walk(folder):
        for filename in filenames:
            if filename.endswith('.rar'):
                full_filename = foldername +'/'+filename
                rar = rarfile.RarFile(full_filename)
                compressed_filename = rar.infolist()[0]
                if compressed_filename.filename not in os.listdir(foldername):
                    logger.info('Extracting %s...' % (compressed_filename.filename))
                    try:
                        rar.extractall(foldername)
                    except:
                        logger.warn('Extracting %s failed...' % (foldername))
                    dst_file=foldername + '/' + compressed_filename.filename
                    try:
                        os.chown(dst_file,uid,gid)
                    except:
                        logger.warn('Chown %s failed...' % (foldername))
                else:
                    logger.debug('Already Extracted: %s' % (compressed_filename.filename))
                #End if
            #End if
        #End for
    #End for
#End function

def mover(folder):
    folder = os.path.abspath(src)
    for foldername,subfolders,filenames in os.walk(folder):
        for filename in filenames:
            if filename.endswith('.mkv') or filename.endswith('.flv') or filename.endswith('.mov') or filename.endswith('.mp4'):
                if filename not in os.listdir(dst) and filename not in os.listdir(srt):
                    logger.info('Moving %s...' % (filename))
                    src_file = foldername + '/' + filename
                    dst_file=dst + '/' + filename
                    shutil.copyfile(src_file,dst_file)
                    os.chown(dst_file,uid,gid)
                else:
                    logger.debug('Already Moved: %s' % (filename))
                #End if
            #End if
        #End for
    #End for
#End function

#Deleter function logic: Check if folder or file. Check if folder is a root folder.
#If so, ignore.
#Other wise, execute appropriate command.
#def deleter():
#    os.path.isdir(path)
#       check if path = /home/mrmxyzptlyk/shows/downloads/
#       else delete folder.
def move_old():
    now = time.time()
    onlyfiles = os.listdir(dst)
    for x in onlyfiles:
        if os.stat(dst+x).st_ctime < now - 14*86400:
            #print("Time: %s Epoch: %s Now: %s Ep: %s" % (time.strftime('%Y-%m-%d', time.localtime(os.stat(x).st_ctime)),int(os.stat(x).st_ctime),int(now),x))
            logger.info("Old file moving for sorting: %s" % (x))
            shutil.move(dst+x, srt+x)

def main():
    #if len(sys.argv) == 1:
        #do all functions, unless a specific file or foldername is give in which case target one.
        #Although.. dont need to do that on cron.

    unrarer(src)
    mover(dst)
    move_old()

if __name__ == "__main__":
    main()
