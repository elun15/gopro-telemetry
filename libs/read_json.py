import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import cv2
import json

def read_json(video_json):


    f = open(video_json)

    # returns JSON object as a dictionary
    data = json.load(f)

    fps = data['frames/second']
    ms_between_frames = 1/fps*1000
    # # Iterating through the json
    # # for GPS5
    # cts_5 = []
    # values_5 = []
    # for i,j in enumerate(data['1']['streams']['GPS5']['samples']):
    #     # print(i['cts'])
    #     print(j)
    #     cts_5.append(round(j['cts']))
    #     values_5.append(j['value'])
    #
    # values_5 = np.asarray(values_5)
    # diff_ms_5 = np.diff(np.asarray(cts_5))

    df_gps = pd.DataFrame(data['1']['streams']['GPS5']['samples'])

    df_gps[['Latitude', 'Longitude', 'Altitude', '2D-Speed', '3D-speed']] = pd.DataFrame(df_gps.value.to_list())
    df_gps.drop(columns=['value', 'sticky'], inplace=True)
    df_gps['cts'] = round(df_gps['cts']).astype(int)



    f.close()
    return df_gps