#Prueba de la API
import cv2
import requests
import base64
import time

# URL de la API
# API_URL = "http://api/INE/back"
API_URL_BACK = 'http://192.168.100.11:5000/INE/back'
API_URL_BACK = 'http://192.168.100.11:5000/INE/front'
API_URL_FRONT = 'http://192.168.100.11:5000/INE/front'

URL = API_URL_BACK

# Inicializar la cámara
cap = cv2.VideoCapture(0)

# Loop principal
while True:
    # Leer un frame de la cámara
    ret, frame = cap.read()

    # Mostrar el frame en una ventana
    cv2.imshow("Frame", frame)

    if ret:

        # Codificar la imagen en base64
        _, buffer = cv2.imencode(".jpg", frame)
        img_base64 = base64.b64encode(buffer).decode("utf-8")

        # Enviar la imagen a la API
        print(URL)
        response = requests.post(URL, json={"image": img_base64}).json()

        # Imprimir la respuesta de la API
        print(response['status'], response['message'], response['data']['Clave_Elector'])

        # Tiene que ir antes que back porque si no, no se cambia la URL
        if(URL == API_URL_FRONT):

            if(response['status'] == 'OK'):
                #Salir de la camara
                break

        if(URL == API_URL_BACK):

            if(response['status'] == 'OK'):
                # Cambiar la URL de la API
                URL = API_URL_FRONT
                response = ''


        # Esperar 0.5 segundos antes de continuar
        time.sleep(1)

        # Verificar si se presionó la tecla "q"
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    else:
        print("Error al leer la cámara")
        break

# Liberar la cámara y cerrar la ventana
cap.release()
cv2.destroyAllWindows()
