import requests
import zbarlight
import time

from PIL import Image
import cv2

def ouvrir():
    print("Ouverture de la porte...")
    time.sleep(3)
    
def fermer():
    print("Fermetture de la porte...")
    time.sleep(3)
    

def demande():
    print("Demande d'autorisation pour ouvrir la porte")
    URL_ETUDIANT="http://479791e0c179.ngrok.io/open-door/door/"+str(1)+"/etudiant/"+"X000000510"
    r = requests.get(URL_ETUDIANT)
    data_etu=r.json()
    
    print(str(data_etu))
    if str(data_etu) == "True":
        print("Demande acceptée")
        ouvrir()
        time.sleep(3)
        fermer()
    else:
        print("Demande refusée")
    


def main():

    # Begin capturing video
    capture = cv2.VideoCapture(0)

    pause = False

    while True:
        # To quit this program press q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Breaks down the video into frames
        if pause == False:    
            ret, frame = capture.read()
        # Displays the current frame
            cv2.imshow('QR READER', frame)

            # Converts image to grayscale.
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Uses PIL to convert the grayscale image into an array that zbarlight can understand.
            pil_im = Image.fromarray(gray)

            # Scans the zbarlight image.
            #codes = zbarlight.scan_codes('qrcode', pil_im)
            codes = zbarlight.scan_codes(['qrcode', 'EAN8', 'EAN13', 'UPCE', 'UPCA', 'ISBN10', 'ISBN13', 'I25', 'CODE39', 'CODE128', 'PDF417'], pil_im)

            print(codes)
            if codes:
                print("Après")
                print('QR CODE détecté et décodé..')
                print(codes)
                pause = True
                demande()
        

        key = cv2.waitKey(1)
        if key == ord('p'):
            if pause == True:
                print("Continuons")
                pause = False
            else:
                print("Pause")
                pause = True

if __name__ == "__main__":
    main()
