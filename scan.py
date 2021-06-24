# MIT License
# 
# Copyright (c) 2017 Akshit Bhalla
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import requests
import zbarlight
import time

from PIL import Image
import cv2

def ouvir():
    print("Ouverture de la porte")
    time.sleep(3)
    
def fermer():
    print("Fermetture de la porte")
    time.sleep(3)
    

def demande():
    print("Demande d'autorisation pour ouvrir la porte")
    URL_ETUDIANT="http://479791e0c179.ngrok.io/open-door/door/"+str(1)+"/etudiant/"+"X000000510"
    r = requests.get(URL_ETUDIANT)
    data_etu=r.json()
    
    if str(data_etu) == "true":
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

            if codes:
                print('QR CODE détecté et décodé..')
                print(codes)
                pause = True
                demande()
                pause = False
                
        

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
