
import os
import matplotlib.pyplot as plt
import cv2

def extract_frames(video_name):

    # video_name = "video5"
    video_path = os.path.join("./src", video_name)

    # Create a VideoCapture object and read from input file
    # If the input is the camera, pass 0 instead of the video file name
    video = cv2.VideoCapture(os.path.join(video_path, video_name + '.MP4'))
    num_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.CAP_PROP_FPS)
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))


    # Check if camera opened successfully
    if (video.isOpened() == False):
        print("Error opening video stream or file")

    output_dir = os.path.join(video_path, 'img')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    frame_counter = 0

    # Read until video is completed
    while (video.isOpened()):
        # Capture frame-by-frame
        ret, frame = video.read()
        if ret == True:

            # Display the resulting frame
            # cv2.imshow('Frame', frame)
            frame_name = os.path.join(output_dir, str(frame_counter).zfill(6) + ".jpg")
            frame_counter += 1
            #print the progress in the same line to avoid cluttering the terminal
            print("\rSaving frame: " + str(frame_counter) + "/" + str(num_frames), end="")

            cv2.imwrite(frame_name, frame)

        # Break the loop
        else:
            break

    # When everything done, release the video capture object
    video.release()