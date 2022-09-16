from django.shortcuts import render
from django.http import HttpResponse
from urllib.parse import unquote
from django.views.decorators.csrf import csrf_exempt
import json
import tensorflow as tf
import numpy as np
import io
from PIL import Image
import base64
import tensorflow_hub as hub

model_name = "movenet_lightning"
module = hub.load("https://tfhub.dev/google/movenet/singlepose/thunder/4")
input_size = 256

KEYPOINT_DICT = {
    'nose': 0,
    'left_eye': 1,
    'right_eye': 2,
    'left_ear': 3,
    'right_ear': 4,
    'left_shoulder': 5,
    'right_shoulder': 6,
    'left_elbow': 7,
    'right_elbow': 8,
    'left_wrist': 9,
    'right_wrist': 10,
    'left_hip': 11,
    'right_hip': 12,
    'left_knee': 13,
    'right_knee': 14,
    'left_ankle': 15,
    'right_ankle': 16
}

config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth=True
sess=tf.compat.v1.Session(config=config)


def movenet(input_image):
    """Runs detection on an input image.

    Args:
      input_image: A [1, height, width, 3] tensor represents the input image
        pixels. Note that the height/width should already be resized and match the
        expected input resolution of the model before passing into this function.

    Returns:
      A [1, 1, 17, 3] float numpy array representing the predicted keypoint
      coordinates and scores.
    """
    model = module.signatures['serving_default']

    # SavedModel format expects tensor type of int32.
    input_image = tf.cast(input_image, dtype=tf.int32)
    # Run model inference.
    outputs = model(input_image)
    # Output is a [1, 1, 17, 3] tensor.
    keypoints_with_scores = outputs['output_0'].numpy()
    return keypoints_with_scores

@csrf_exempt
def sendFrame(request):
    
    #start= time.time()
    if request.method == 'POST':
        data = unquote(request.body)
        data = str(request.body)
        data = data.split("------")[1].split("jpeg;base64,")[1]       
        temp = base64.b64decode(data+ '==')
        image = Image.open(io.BytesIO(temp))
        
        image_np = np.array(image)
        Tens = tf.convert_to_tensor(image_np)
        input_image=tf.cast(Tens, tf.int32)
        input_image = input_image[None,:,:,:]
        
        result = np.squeeze(movenet(input_image))
        new_dict = dict(zip(KEYPOINT_DICT.keys(), list(result)))
        #print(time.time()- start)
        return HttpResponse(json.dumps(str(new_dict)))
    else:    
        return render(request,'index.html')  

## Source : https://www.tensorflow.org/hub/tutorials/movenet
#input_image = tf.expand_dims(input_image, axis=0)
#input_image = tf.image.resize_with_pad(input_image)
#temp = base64.urlsafe_b64decode(data)
#data = (data + '='*(4-len(data)%4)) if len(data)%4 != 0 else data  
#loaded = posenet.decode_multiple_poses
#from . import drawing
#import cv2
#from matplotlib import pyplot as plt
#from django.contrib import messages
#import time
#from tensorflow_docs.vis import embed