# import os
import random
import datetime
from google.cloud import datastore, storage
import google.oauth2.id_token
from flask import Flask, render_template, request, redirect, url_for
from google.auth.transport import requests

from PIL import Image 
from PIL import ImageFont
from PIL import ImageDraw

# credential_path = "h:\Desktop\Cloud Programming\Labs\env/assignment01-343611-d88e3f82d83b.json"
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

app = Flask(__name__)
#datastore_client = datastore.Client()
#firebase_request_adapter = requests.Request()



@app.route('/')
def root():
    return render_template('index.html')

@app.route('/formulaire')
def formulaire():
    return render_template('formulaire.html')



def ajoutTxtVisible(txt):
    #font = ImageFont.truetype("times-ro.ttf", 34)
    img = Image.open('image_test.png')
    draw = ImageDraw.Draw(img)
    draw.text((1000, 200),txt,(0,0,0))

    img.save('img2.png')

@app.route('/ajout_texte', methods=['POST'])
def ajout_texte():
    ajoutTxtVisible('BONJOUR BONJOUR BONJOUR')
    return redirect('/formulaire')




@app.route('/connection')
def connection():
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    user = None

    if id_token:
        try:
            #claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
            #user = retrieveUser(claims)
            if user == None:
                return render_template('firstConnection.html', message="")
            else:
                return redirect('/index')
        except ValueError as exc:
            error_message = str(exc)
    return redirect('/')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
