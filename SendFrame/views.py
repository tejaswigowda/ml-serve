from wsgiref import headers
from django.shortcuts import render
from django.http import HttpResponse
from urllib.parse import unquote
from django.views.decorators.csrf import csrf_exempt
import json
import io
from PIL import Image
import base64
import mediapipe as mp
import math
import numpy as np
import cv2
import os
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
import gc

def download_model(model_type):
    server_prefix = 'https://omnomnom.vision.rwth-aachen.de/data/metrabs'
    model_zippath = tf.keras.utils.get_file(
        origin=f'{server_prefix}/{model_type}_20211019.zip',
        extract=True, cache_subdir='models')
    model_path = os.path.join(os.path.dirname(model_zippath), model_type)
    return model_path

# gc.collect()
# config = ConfigProto()
# config.gpu_options.per_process_gpu_memory_fraction = 0.2
# config.gpu_options.allow_growth = True
# session = InteractiveSession(config=config)

model = tf.saved_model.load(download_model('metrabs_mob3l_y4t'))
@csrf_exempt
def sendFrame(request):
    
    #start= time.time()
    if request.method == 'POST':
        data = unquote(request.body)
        # data = str(request.body)
        
        data = data.split("jpeg;base64,")[1].split("------")[0]
        # data = data.replace(" ","")     
        temp = base64.b64decode(data+ '==')
        image = Image.open(io.BytesIO(temp))
        
        image_np = np.array(image)
        Tens = tf.convert_to_tensor(image_np)
        # input_image=tf.cast(Tens, tf.int32)
        # input_image = input_image[None,:,:,:]
        pred = model.detect_poses(Tens, skeleton='smpl_24')

        # result = np.squeeze(movenet(input_image))
        #print(result)
        #new_dict = dict(zip(KEYPOINT_DICT.keys(), list(result)))
        #print(time.time()- start)
        d = {}
        d["persons"] =  pred['boxes'].numpy().shape[0]
        d["edges"] = model.per_skeleton_joint_edges['smpl_24'].numpy().tolist()
        d["boxes"] = pred['boxes'].numpy().tolist()
        d["poses3d"] = pred['poses3d'].numpy().tolist()
        d["poses2d"] = pred['poses2d'].numpy().tolist()
        return HttpResponse(json.dumps(d)) 
        
       
    else:    
        return render(request,'index.html')




mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils 
mp_drawing_styles = mp.solutions.drawing_styles
pose = mp_pose.Pose( min_detection_confidence=0.5,enable_segmentation=True)
@csrf_exempt
def mediapipe(request):
    
    #start= time.time()
    if request.method == 'POST':
        data = unquote(request.body)
        data = str(request.body)
        # data = data.split("base64,")[1].split("------")[0]
        data = data.split("------")[1].split("base64,")[1]  
        temp = base64.b64decode(data+ '==')
        image = Image.open(io.BytesIO(temp)).convert('RGB') 
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # print("converted image"+image)
        results = pose.process(image)
        # annotated_image = image.copy()
        # mp_drawing.draw_landmarks(annotated_image,results.pose_landmarks,mp_pose.POSE_CONNECTIONS,landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        return HttpResponse(json.dumps(str(results.pose_landmarks)) )
               
    else:    
        return render(request,'index.html')