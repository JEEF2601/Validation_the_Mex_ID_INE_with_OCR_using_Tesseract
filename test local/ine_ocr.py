#ine_ocr
import re
import cv2
import pytesseract

def validation_String(string, length):

    #validate the length of the string
    if(len(string) != length):
        return False
    
    #validate the string is a digit
    if not string.isdigit():
        return False
    
    #validate the string is a number of the INE
    return True

#OCR the back of the INE
def ocrBack(frame):

    #set the path of the tesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    #get the image
    image = frame

    #convert the image to gray
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #apply a threshold
    umbral = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 55, 25)

    #Config the tesseract
    config = '--psm 1'

    #get the text
    text = pytesseract.image_to_string(umbral, config=config)

    print(text)

    #clean the text
    match = re.search('MEX', text)

    #
    if match:

        #get the SIC_INE
        SIC_INE = text[match.end():text.find('<<')]
        SIC_VALIDATION = validation_String(SIC_INE, 10)

        #get the OCR_INE
        OCR_INE = text[text.find('<<') + 2:text.find('<<') + 2 + 13]
        OCR_VALIDATION = validation_String(OCR_INE, 13)

        #Print the validation
        print('SIC_INE: ', SIC_INE, ' - El SIC es valido: ', SIC_VALIDATION)
        print('OCR_INE: ', OCR_INE, ' - El OCR es valido: ', OCR_VALIDATION)


        #Prube the validation
        if SIC_VALIDATION and OCR_VALIDATION:
            json_return = {'SIC_INE': SIC_INE, 'OCR_INE': OCR_INE}
        else:
            json_return = {'SIC_INE': 'No se encontro el SIC', 'OCR_INE': 'No se encontro el OCR'}
        
    else:
        json_return = {'SIC_INE': 'No se encontro el SIC', 'OCR_INE': 'No se encontro el OCR'}
    
    return json_return

#OCR the front of the INE
def ocrFront(frame):

    #set the path of the tesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    #get the image
    image = frame

    #convert the image to gray
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #apply a threshold
    umbral = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 55, 25)

    #Config the tesseract
    config = '--psm 1'

    #get the text
    text = pytesseract.image_to_string(umbral, config=config)

    print(text)

    #clean the text
    match_main = re.search('VOTAR', text)
    match = re.search('ELECTOR', text)

    #
    if match_main:
            
        #get the SIC_INE
        clave_elector = text[match.end():]
        CLAVE_VALIDATION = validation_String(clave_elector, 18)

        #Print the validation
        print('Clave de elector: ', clave_elector, ' - La clave es valido: ', CLAVE_VALIDATION)


        #Prube the validation
        if CLAVE_VALIDATION:
            json_return = {'Clave_Elector': clave_elector}
        else:
            json_return = {'Clave_Elector': 'No se encontro la clave_Elector'}

    else:
        # json_return = {'Clave_Elector': 'Probablemente la imagen no sea de la parte frontal del INE'}
        json_return = {'Clave_Elector': 'No se encontro la clave_Elector'}

    
    #return the json
    return json_return