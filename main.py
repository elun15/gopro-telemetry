import os
import sys

import  numpy as np
import pandas as pd
from libs import extract_telemetry, extract_frames, read_avi
import matplotlib.pyplot as plt
import cv2
from geographiclib.geodesic import Geodesic

geod = Geodesic.WGS84  # define the WGS84 ellipsoid

video_name = "video5"
video_path = os.path.join("./src", video_name)
path_video_json = os.path.join(video_path, video_name + '-full-telemetry.json')
path_video_avi = os.path.join(video_path, video_name + '.MP4')

flag_save_telemetry = 0
flag_extract_frames = 0
flag_save_interp_trajectory = 1
flag_save_frames_with_trajectory_azi = 1


#############################
# Extract both interpolated telemetry and original as pandas dataframes
telemetry_interp, telemetry = extract_telemetry.extract_telemetry(geod, path_video_json, path_video_avi)
if flag_save_telemetry  == 1:
    telemetry_interp.to_csv(os.path.join(video_path, video_name + '-frame_gps_interp.csv'), index=False)


#############################
if flag_extract_frames == 1:
    extract_frames.extract_frames(video_name)


#############################
# Plot interpolated trajectory
if flag_save_interp_trajectory == 1:

    long = telemetry['long'].values
    lat = telemetry['lat'].values
    long_interp = telemetry_interp['long'].values
    lat_interp = telemetry_interp['lat'].values

    plt.figure()
    plt.plot(long, lat, linewidth=3, color='lightblue')
    plt.ylabel('Latitude')
    plt.xlabel('Longitude')
    plt.plot(long, lat, '.', markersize=0.25, color='navy')
    plt.title('GPS trajectory')
    plt.savefig(os.path.join(video_path, video_name + '-gps.pdf'))
    plt.close()
    # now plot the interpolated values other color

    plt.figure()
    plt.plot(long_interp, lat_interp, linewidth=3, color='lightblue')
    plt.ylabel('Latitude')
    plt.xlabel('Longitude')
    plt.plot(long_interp, lat_interp, '.', markersize=0.25, color='navy')
    plt.title('GPS trajectory interpolated')
    plt.savefig(os.path.join(video_path, video_name + '-gps_interp.pdf'))
    plt.close()

    # plot both in the same plot with different colors
    plt.figure()
    plt.ylabel('Latitude')
    plt.xlabel('Longitude')
    plt.plot(long_interp, lat_interp, '.', markersize=0.25, color='red')
    plt.plot(long, lat, '.', markersize=0.1, color='navy')
    plt.title('GPS trajectory')
    plt.legend(['Interpolated', 'Original'])
    plt.savefig(os.path.join(video_path, video_name + '-gps_interp_both.pdf'))
    plt.close()


#############################
# Plot frame with trajectory and orientation
if flag_save_frames_with_trajectory_azi == 1:

    frame_img_path = os.path.join(video_path, 'img')

    if not os.path.exists(frame_img_path):
        print("Directory does not exist")
        exit()

    num_frames, fps = read_avi(path_video_avi)


    long_interp = telemetry_interp['long'].values
    lat_interp = telemetry_interp['lat'].values
    azi = telemetry_interp['azi'].values

    # A loop plotting in a subplot, at the left the image, at the right the gps trajectory and the orientation
    # for 1 out of 10 frames
    for i in range(0, int(num_frames), 10):

        # print the progress in the same line to avoid cluttering the terminal

        print("\rPlotting frame " + str(i) + " of " + str(int(num_frames)), end="")
        # read image
        img = cv2.imread(os.path.join(frame_img_path, str(i).zfill(6) + '.jpg'))
        # convert to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # plot image with bigger resolution
        plt.figure(figsize=(20, 10))
        plt.subplot(1, 2, 1)
        plt.imshow(img)
        plt.title('Frame ' + str(i))
        # plot gps trajectory
        plt.subplot(1, 2, 2)
        plt.plot(long_interp, lat_interp, '.', markersize=2, color='lightskyblue')
        plt.plot(long_interp[i], lat_interp[i], '.', markersize=3, color='red')

        plt.title('GPS trajectory. Azi: ' + str(round(azi[i], 2)) + '°. \n North (0º)')
        plt.xlabel('South (180º)')
        plt.ylabel('West (270º)')
        plt.text(1.02, 0.5, 'East (90º)', ha='center', va='center', rotation='vertical', transform=plt.gca().transAxes)
        plt.text(1.02, 1, '(45º)', ha='center', va='center', rotation='vertical', transform=plt.gca().transAxes)
        plt.text(1.02, 0.05, '(135º)', ha='center', va='center', rotation='vertical', transform=plt.gca().transAxes)
        plt.text(-0.05, 0.05, '(225º)', ha='center', va='center', rotation='vertical', transform=plt.gca().transAxes)
        plt.text(-0.05, 1, '(315º)', ha='center', va='center', rotation='vertical', transform=plt.gca().transAxes)

        plt.tight_layout()

        # #check if exists the directory, if not, create it
        if not os.path.exists(os.path.join(video_path, 'img_gps')):
            os.makedirs(os.path.join(video_path, 'img_gps'))
        plt.savefig(os.path.join(video_path, 'img_gps', str(i).zfill(6) + '.png'))
        plt.close()
