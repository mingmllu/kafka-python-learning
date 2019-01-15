
import cv2
import numpy as np
import json
import multiprocessing
import os.path
import os
from datetime import datetime
import time

port_num = 9107

def video_recorder():
    # Create a VideoCapture object
    url = 'http://root:fitecam@135.222.247.179:%d/mjpg/video.mjpg'%(port_num)
    cap = cv2.VideoCapture(url)
    # Check if camera opened successfully
    if (cap.isOpened() == False): 
        print("Unable to read camera feed")
        cap_failure_file = open('video_cap_notok_%d.txt'%(port_num), 'w')
        cap_failure_file.close()
        return

    cap_success_file = open('video_cap_ok_%d.txt'%(port_num), 'w')
    cap_success_file.close()

    # Default resolutions of the frame are obtained.The default resolutions are system dependent.
    # We convert the resolutions from float to integer.
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Define the codec and create VideoWriter object.The output is stored in the file.
    now = datetime.utcnow().strftime("%Y%m%d%H%M%S")

    out_file_name = "video_fite_lab_{}_{}.avi".format(port_num, now)
    out = cv2.VideoWriter(out_file_name, cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
    # A counter for frames that have been written to the output file so far
    n_frames = 0
    while(True):
        ret, frame = cap.read()
        if ret == True: 
            # Write the frame into the file 'output.avi'
            out.write(frame)
            n_frames += 1
            print("Frame %d saved " % (n_frames))
        # Break the loop
        else:
            break 
    # When everything done, release the video capture and video write objects
    cap.release()
    out.release()





from kafka import KafkaConsumer

# If the broker installed on a separate host machine,
# use the machine's IP address
brokers = ['10.4.17.190:9092']

# connect to Kafka server and pass the topic we want to consume
topic = 'fitelab_cam_%d'%(port_num)
consumer = KafkaConsumer(topic, bootstrap_servers=brokers)
print("Start to listen on Kafka broker")
print("It may take some time to receive the first message")
print("")



average_person_count = 0.0
consecutive_count_above_thresh = 0
iir_filter_coef = 0.95
threshold_start_recording = 1.0
# the initial state of recorder
recorder_alive = False
# if "count_person" is above the threshold_start_recording 
above_start_thresh_in_a_row = 5
threshold_stop_recording = 0.1


start_recording_time = time.time()

for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    s = message.value.decode("utf-8") 
    data_double_quotes = s.replace("\'", "\"") #JSON strings must use double quotes
    data_dict = json.loads(data_double_quotes)
    count_person = data_dict['count_person']


    # Test code when no persons present  
    #if time.time() - start_recording_time < 100.0:
    #    count_person = 2

    if count_person < threshold_start_recording:
        consecutive_count_above_thresh = 0
    else:
        consecutive_count_above_thresh += 1
    average_person_count = iir_filter_coef * average_person_count + (1.0 - iir_filter_coef) * count_person

    if not recorder_alive and consecutive_count_above_thresh >= above_start_thresh_in_a_row:
        if os.path.isfile('video_cap_notok_%d.txt'%(port_num)): 
            os.remove('video_cap_notok_%d.txt'%(port_num))
        p = multiprocessing.Process(target = video_recorder)
        p.start()
        recorder_alive = True
        start_recording_time = time.time()

    if recorder_alive and time.time() - start_recording_time > 15.0:
        # check if VideoCapture is successful: will use a better way to do this
        # the file must there if we are able to read the camera
        if os.path.isfile('video_cap_notok_%d.txt'%(port_num)):
            p.terminate()
            p.join()
            recorder_alive = False # will try again upon arrival of the next message

    if recorder_alive and count_person == 0 and average_person_count <= threshold_stop_recording:
        p.terminate()
        p.join()
        # check if VideoCapture is successful: will use a better way to do this
        if os.path.isfile('video_cap_ok_%d.txt'%(port_num)): 
            os.remove('video_cap_ok_%d.txt'%(port_num))
        recorder_alive = False

    if not recorder_alive:
        print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))
