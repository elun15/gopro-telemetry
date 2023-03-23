from libs import read_json, read_avi
import numpy as np
import pandas as pd


def extract_telemetry(geod, path_video_json, path_video_avi):
    #Dataframe with GPS data
    df_gps = read_json.read_json(path_video_json)

    #Number of frames and FPS
    num_frames, fps = read_avi.read_avi(path_video_avi)
    fps = round(fps)

    #Compute the time difference in ms between frames
    diff_ms = 1 / fps * 1000
    #Compute the duration of the video in ms
    duration_ms = round(num_frames * diff_ms)
    #Compute the time in ms of each frame
    frame_ms = np.round(np.arange(0, duration_ms, diff_ms)).astype(int)

    #Extract the latitude and longitude values
    lat = df_gps['Latitude'].values
    long = df_gps['Longitude'].values

    #Interpolate the latitude and longitude values
    x = frame_ms
    xp = df_gps['cts'].values
    fp = lat
    lat_interp = np.interp(x, xp, fp)
    fp = long
    long_interp = np.interp(x, xp, fp)

    #Compute the azimuth between two consecutive points (orientation)
    azi1 = []
    for i in range(0, len(lat_interp) - 1):
        # use geod.inv to calculate the distance between two consecutive points
        g = geod.Inverse(lat_interp[i], long_interp[i], lat_interp[i + 1], long_interp[i + 1])

        # save the azi1  in a list if it is positive, else save 360+azi1
        if g['azi1'] > 0:
            azi1.append(g['azi1'])
        else:
            azi1.append(360 + g['azi1'])

    #Add a new value at the begining of azi1 to NaN
    azi1.insert(0, np.nan)

    #List of number of frames in the video
    n_frame = np.arange(0, num_frames).astype(int)

    #Compute the dataframe with the interpolated values
    df_telemetry_interp = pd.DataFrame({'frame': n_frame, 'lat': lat_interp, 'long': long_interp, 'azi': azi1})

    #Computea a dataframe with the original values
    df_telemetry = pd.DataFrame({'ms': df_gps['cts'].values , 'lat': df_gps['Latitude'].values, 'long': df_gps['Longitude'].values})

    return df_telemetry_interp, df_telemetry
