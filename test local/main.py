#Main
############################################################################################################
#Scritp (api) to receive a base64 image and process it to find a QR code
import cv2
import json
import base64
import numpy as np
from flask_cors import CORS
from pyzbar.pyzbar import decode
from flask import Flask, request, jsonify

from decode_image import decodeImage
from ine_ocr import ocrBack, ocrFront
############################################################################################################

############################################################################################################
#Flask_cors
flask_app = Flask(__name__,)
# cors = CORS(flask_app, resources={r"/api/*": {"origins": "*"}})
cors = CORS(flask_app)
flask_app.config['CORS_HEADERS'] = 'Content-Type'
############################################################################################################

############################################################################################################
#API to receive the image
@flask_app.route('/INE/<method>', methods=['POST'])
def INE(method):

    print('Method: ', method)

    #get the image
    # image = request.get_data(as_text=True)
    image = request.get_json()
    # image = image['image']

    #Clean the image
    image['image'] = image['image'].replace('data:image/jpeg;base64,', '')
    imageb64 = image['image']

    #decode the imageb64 and convert a imagen cv2
    frame = decodeImage(image)
    
    #OCR the image
    if method == 'back':

        #get the text
        text = ocrBack(frame)

        #get the SIC_INE and OCR_INE
        SIC_INE = text['SIC_INE']
        OCR_INE = text['OCR_INE']

        #Prube the validation
        if SIC_INE != 'No se encontro el SIC' and OCR_INE != 'No se encontro el OCR':

            #Build the json
            json_response = {
                'status': 'OK',
                'data': {
                    'SIC_INE': SIC_INE,
                    'OCR_INE': OCR_INE
                },
                'image': 'data:image/jpeg;base64,' + imageb64,
                'message': 'Se encontro el SIC y el OCR',
                'method': 'back'
            }

        else:
            json_response = {
                'status': 'ERROR',
                'data': {
                    'SIC_INE': SIC_INE,
                    'OCR_INE': OCR_INE
                },
                'image': 'data:image/jpeg;base64,' + imageb64,
                'message': 'No se encontro el SIC o el OCR',
                'method': 'back'
            }
    
    elif method == 'front':

        #get the text
        text = ocrFront(frame)

        #get the Clave_Elector and CURP
        Clave_Elector = text['Clave_Elector']
        # CURP = text['CURP']

        #Prube the validation
        # if Clave_Elector != 'No se encontro la Clave_Elector' and Clave_Elector != 'No se encontro la CURP':
        if Clave_Elector != 'No se encontro la clave_Elector':

            #Build the json
            json_response = {
                'status': 'OK',
                'data': {
                    'Clave_Elector': Clave_Elector
                    # 'CURP': CURP
                },
                'image': 'data:image/jpeg;base64,' + imageb64,
                'message': 'Se encontro la Clave_Elector y la CURP',
                'method': 'front'
            }
        else:
            json_response = {
                'status': 'ERROR',
                'data': {
                    'Clave_Elector': Clave_Elector,
                    # 'CURP': CURP
                },
                'image': 'data:image/jpeg;base64,' + imageb64,
                'message': 'No se encontro la Clave_Elector o la CURP',
                'method': 'front'
            }
    
    else:
        json_response = {
            'status': 'PRUEBA',
            'data': {
                'SIC_INE': 'Valor de prueba',
                'OCR_INE': 'Valor de prueba'
            },
            'image': 'image prube',
            'message': 'PRUEBA',
            'method': 'PRUEBA'
        }
    
    #Return the json
    return jsonify(json_response)
############################################################################################################

# 

############################################################################################################
#Run the app
if(__name__ == '__main__'):
    flask_app.run(host='0.0.0.0', port=5000, debug=True)
############################################################################################################