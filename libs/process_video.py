import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import cv2
import json
from read_json import read_json
from read_avi import read_avi
from geographiclib.geodesic import Geodesic


geod = Geodesic.WGS84  # define the WGS84 ellipsoid

# video_name = "video5"
# video_path = os.path.join("../src", video_name)
# video_json = os.path.join(video_path, video_name + '-full-telemetry.json')
# video_avi = os.path.join(video_path, video_name + '.MP4')

# df_gps = read_json(video_json)
# num_frames, fps = read_avi(video_avi)
# fps = round(fps)
# diff_ms = 1/fps*1000
# duration_ms = round(num_frames * diff_ms)
# frame_ms = np.round(np.arange(0,duration_ms,diff_ms)).astype(int)

# lat = df_gps['Latitude'].values
# long = df_gps['Longitude'].values
#
#
# x = frame_ms
# xp = df_gps['cts'].values
# fp = lat
# lat_interp= np.interp(x, xp, fp)
# fp = long
# long_interp= np.interp(x, xp, fp)



save_figures_flag = 1
if save_figures_flag == 1:
    plt.figure()
    plt.plot(long, lat,linewidth=3,color='lightblue')
    plt.ylabel('Latitude')
    plt.xlabel('Longitude')
    plt.plot(long, lat,'.',markersize=0.25,color='navy')
    plt.title('GPS trajectory')
    plt.savefig(os.path.join(video_path, video_name + '-gps.pdf'))
    plt.close()
    #now plot the interpolated values other color

    plt.figure()
    plt.plot(long_interp,lat_interp, linewidth=3,color='lightblue')
    plt.ylabel('Latitude')
    plt.xlabel('Longitude')
    plt.plot(long_interp,lat_interp,'.',markersize=0.25,color='navy')
    plt.title('GPS trajectory interpolated')
    plt.savefig(os.path.join(video_path, video_name + '-gps_interp.pdf'))
    plt.close()

    #plot both in the same plot with different colors
    plt.figure()
    plt.ylabel('Latitude')
    plt.xlabel('Longitude')
    plt.plot(long_interp, lat_interp ,'.',markersize=0.25,color='red')
    plt.plot(long,lat, '.', markersize=0.1, color='navy')
    plt.title('GPS trajectory')
    plt.savefig(os.path.join(video_path, video_name + '-gps_interp_both.pdf'))
    plt.close()


save_csv_flag = 1
if save_csv_flag == 1:

    # # a loop over the size of lat to compute the azi1 every 10 frames
    # azi1 = []
    # for i in range(0, len(lat_interp)-1):
    #     # use geod.inv to calculate the distance between two consecutive points
    #     g = geod.Inverse(lat_interp[i], long_interp[i], lat_interp[i+1], long_interp[i+1])
    #
    #
    #     # save the azi1  in a list if it is positive, else save 360+azi1
    #     if g['azi1'] > 0:
    #         azi1.append(g['azi1'])
    #     else:
    #         azi1.append(360+g['azi1'])
    #
    #
    #
    # #add a new valye at the begging of azi1 set to NaN
    # azi1.insert(0, np.nan)


    #plot all azi1 values. considering that azi1 is computed at every 10 frames, change the xticks to show the frame number
    #change the xticks to show the real frame number at 30fps
    # plt.figure()
    # plt.plot(azi1,'.',markersize=0.25,color='navy')
    # plt.xlabel('Sample')
    # plt.ylabel('Azimuth')
    # plt.title('Azimuth')
    # #change the xticks to show the real frame number at 30fps
    # plt.savefig(os.path.join(video_path, video_name + '-azi1.pdf'))
    #
    #
    # #histogram of azi1
    # plt.figure()
    # plt.hist(azi1, bins=100)
    # plt.xlabel('Azimuth')
    # plt.ylabel('Frequency')
    # plt.title('Azimuth')
    # plt.savefig(os.path.join(video_path, video_name + '-azi1_hist.pdf'))
    # plt.close()

    #list of number of frames in the video
    n_frame = np.arange(0,num_frames).astype(int)
    #save a csv file with three columns: number of frame, interpolated latitude, and interpolated longitude
    df = pd.DataFrame({'frame': n_frame, 'lat': lat_interp, 'long': long_interp, 'azi': azi1})
    df.to_csv(os.path.join(video_path, video_name + '-frame_gps_interp.csv'), index=False)



frame_img_path = os.path.join(video_path, 'img')
#if directory does not exist, end the program
if not os.path.exists(frame_img_path):
    print("Directory does not exist")
    exit()

#ignore plotting warnings
import warnings
warnings.filterwarnings("ignore")

#a loop plotting in a subplot, in the left the image, in the right the gps trajectory
#for 1 out of 10 frames
for i in range(0, int(num_frames), 10):

    # print the progress in the same line to avoid cluttering the terminal

    print("\rPlotting frame " + str(i) + " of " + str(int(num_frames)), end="")
    #read image
    img = cv2.imread(os.path.join(frame_img_path, str(i).zfill(6) + '.jpg'))
    #convert to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


    #plot image with bigger resolution
    plt.figure(figsize=(20,10))
    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.title('Frame ' + str(i))
    #plot gps trajectory
    plt.subplot(1, 2, 2)
    plt.plot(long_interp,lat_interp,  '.', markersize=2, color='lightskyblue')
    plt.plot(long_interp[i], lat_interp[i], '.', markersize=3, color='red')
    #considering azi1[i] is the angle. plot an arrow from the current point to the point at azi1[i] angle
    #and distance 0.0001
    # plt.arrow(long_interp[i], lat_interp[i], 0.0001*np.cos(np.deg2rad(azi1[i])),0.0001*np.sin(np.deg2rad(azi1[i])), head_width=0.0001, head_length=0.0001, fc='k', ec='k')

    plt.title('GPS trajectory. Azi: ' + str(round(azi1[i], 2)) + '°. \n North (0º)')
    plt.xlabel('South (180º)')
    plt.ylabel('West (270º)')
    plt.text(1.02, 0.5, 'East (90º)', ha='center', va='center', rotation='vertical', transform=plt.gca().transAxes)
    plt.text(1.02, 1, '(45º)', ha='center', va='center', rotation='vertical', transform=plt.gca().transAxes)
    plt.text(1.02, 0.05, '(135º)', ha='center', va='center', rotation='vertical', transform=plt.gca().transAxes)
    plt.text(-0.05, 0.05, '(225º)', ha='center', va='center', rotation='vertical', transform=plt.gca().transAxes)
    plt.text(-0.05,1, '(315º)', ha='center', va='center', rotation='vertical', transform=plt.gca().transAxes)


    plt.tight_layout()

    # #check if exists the directory, if not, create it
    if not os.path.exists(os.path.join(video_path ,'img_gps')):
        os.makedirs(os.path.join(video_path ,'img_gps'))
    plt.savefig(os.path.join(video_path ,'img_gps', str(i).zfill(6) + '.png'))
    plt.close()

