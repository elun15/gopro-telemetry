import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import cv2
import json

def read_avi(video_avi):
    # Create a VideoCapture object and read from input file
    # If the input is the camera, pass 0 instead of the video file name
    video = cv2.VideoCapture(video_avi)
    # Check if camera opened successfully
    if (video.isOpened() == False):
        print("Error opening video stream or file")

    num_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.CAP_PROP_FPS)
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    video.release()


    return num_frames, fps