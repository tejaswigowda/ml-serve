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

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils 
mp_drawing_styles = mp.solutions.drawing_styles
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)


@csrf_exempt
def sendFrame(request):
    
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

        return HttpResponse(json.dumps(str(results.pose_landmarks)) )
        
       
    else:    
        return render(request,'index.html')