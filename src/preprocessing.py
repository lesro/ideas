
import json
import pandas as pd
import numpy as np
from pytube import YouTube
import cv2
import os
from moviepy.editor import *


def dfmakeColumns(df):

    """
    create column for unique file names to save videos

    Parameters:
    df (DataFrame): pandas dataframe 
    label (string): name of column to pass in as unique file name

    Returns:
    New dataframe with new filename column
    """
    for i in range(len(df.index)):
        df['filename'][i] = str(df.index[i])+'-'+str(df.label[i])
        df['path'][i] = str(df.text)+'/'+str(df.index[i])+'-'+str(df.label[i])+'.mp4'
    return df


def pullURL(main_dir, df):
    """
    save all videos locally into relative directory and assign unique filename

    Parameters:
        main_dir(string): main directory path for root folder where subfolders are all the classes
        df(pandas Dataframe): dataframe that holds all features of each video
    Returns:
        None
    """

    for url, fname, class_ in zip(df.url, df.filename, df.text):
        os.chdir(str(main_dir))
        try:
            vid = YouTube(str(url)).streams.first()
            if os.path.isdir(str(class_)) is False:
                 os.makedirs(str(class_))
                 os.chdir(str(main_dir)+str(class_))
                 vid.download(filename=fname)
            else:    
                os.chdir(str(main_dir)+str(class_))
                vid.download(filename=fname)
        except:
            continue

def get_vidDirectory(main_dir, end_char):
    """ 
    create list of all the end file directory for every class

    Parameters:
        main_path(string): main directory path for root folder
        end_char(string): desired file extension the file name ends

    Returns:
        list of all file directory
    """
    lst = []
    for class_ in os.listdir(str(main_dir)):
        try:
            if class_.endswith('Store'):
                continue
            else:
                for f in os.listdir(f'{main_dir}{class_}/'):
                    if f.endswith(str(end_char)):
                        lst.append(os.path.join(f'{main_dir}{class_}',f))
        except:
            continue
    return lst


def subClip(main_dir, df):
    """ 
    Identifies which vidoes require subclipping and cross-references with dataframe.
    Also deletes original video that has additional ASL. 

    Parameters:
        main_dir(string): main directory path for root folder where subfolders are all the classes
        df(pandas Dataframe): dataframe that holds all features of each video

    Returns:
        None
    """
    for class_ in os.listdir(str(main_dir)):
        try:
            if not class_.endswith('Store'):
                os.chdir(str(main_dir)+str(class_))
                for fname in os.listdir(str(main_dir)+str(class_)):
                    if not fname.endswith('Store'):
                        x = df[df.filename == str(fname)]
                        start = x.start_time.values[0]
                        end = x.end_time.values[0]
                        if not start == 0:
                            VideoFileClip(str(os.path.join(f'{main_dir}{class_}',fname)), audio=False).subclip(float(start),float(end)).write_videofile('C-'+str(fname))
                            os.remove(str(fname))
                            os.rename('C-'+str(fname), str(fname))
                        else:
                            continue
                    else:
                        continue
        else:
            continue

def extractFrames(main_dir, sec=0, fRate=.1):

    for class_ in os.listdir(str(main_dir)):
        try:
            if not class_.endswith('Store'):
                os.chdir(str(main_dir)+str(class_))
                for fname in os.listdir(str(main_dir)+str(class_)):
                    if not fname.endswith('Store'):
                        vidcap = cv2.VideoCapture(str(fname))
                        def getFrame(sec):
                            vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
                            hasFrames,image = vidcap.read()
                            if hasFrames:
                                cv2.imwrite(str(fname.split('.')[0])+ '-' + str(count)+".jpg", image)     # save frame as JPG file
                            return hasFrames
                        sec = 0
                        frameRate = fRate #//it will capture image in each 0.5 second
                        count=1
                        success = getFrame(sec)
                        while success:
                            count = count + 1
                            sec = sec + frameRate
                            sec = round(sec, 2)
                            success = getFrame(sec)
        except:
            continue

# OPENCV FUNCTIONS FOR FUTURE USE

"""
using openCV optical flow for 
=====
Optical flow is the pattern of apparent motion of image objects between two consecutive frames caused 
by the movemement of object or camera. It is 2D vector field where each vector is a displacement vector sh

link: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_video/py_lucas_kanade/py_lucas_kanade.html?highlight=videocapture%20show%20frames
=====
"""

"""
opencv FaceDetection
=====
Facial detection

link: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_objdetect/py_face_detection/py_face_detection.html#face-detection
=====
"""


"""
opencv Background subtraction
=====
Background subtraction is a major preprocessing steps in many vision based applications. 
For example, consider the cases like visitor counter where a static camera takes the number of 
visitors entering or leaving the room, or a traffic camera extracting information about the vehicles etc. 

link: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_video/py_bg_subtraction/py_bg_subtraction.html?highlight=videocapture%20show%20frames
=====
"""
if __name__ == __main__:
    pass