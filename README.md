# Gopro-telemetry 

**1**. Create the Anaconda environment from SEGACV.yml

**2**. Donwload the .zip or clone this repository

**3**. Create the *gopro-telemetry/src/* folder. This folder will contain the videos to process. The structure should be the following:

```
src
│
└───video_name1
│   └── video_name1.MP4
└───video_name2
    └── video_name2.MP4
    
```

**4**. Extract the JSON containing the telemetry information from the video file. To do so:

 - Edit the file *full-telemetry.js* . Line 5 must contain the path to the video file, and line 10 must contain the path to the output JSON file.  
 - Run `node full-telemetry.js`. The output JSON 

**5.** Extract telemetry data from the JSON file:

 - Edit the variable *video_name*  in the *main.py* file to contain the name of the video file without the .MP4 extension.
 - Select the desired flags
 - Run python main.py


**REFERENCES**

https://www.trekview.org/blog/2022/gopro-telemetry-exporter-getting-started/

https://github.com/JuanIrache/gopro-telemetry

https://github.com/gopro/gpmf-parser
