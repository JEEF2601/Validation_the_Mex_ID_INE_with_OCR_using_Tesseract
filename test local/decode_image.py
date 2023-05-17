#DECODE IMAGE
import base64
import cv2
import numpy as np

#decode the image
def decodeImage(image):
    
    #convert the image to a numpy array
    nparr = np.fromstring(base64.b64decode(image['image']), dtype = np.uint8)
    #decode the image
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)