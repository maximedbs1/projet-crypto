import os
import random
import datetime
from flask import Flask, render_template, request, redirect, url_for


import stegano as st
from PIL import Image 
from PIL import ImageFont
from PIL import ImageDraw
import pyotp
import base64


# credential_path = "h:\Desktop\Cloud Programming\Labs\env/assignment01-343611-d88e3f82d83b.json"
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

app = Flask(__name__)
#datastore_client = datastore.Client()
#firebase_request_adapter = requests.Request()

auth = True

bdd_tsr = {}
bdd_tsq = {}

def initializeBdd():
    tsr = os.popen("ls timestamp_files/tsr_files/").read()
    tsq = os.popen("ls timestamp_files/tsq_files/").read()
    lst_tsr = tsr.split("\n")
    lst_tsq = tsq.split("\n")
    lst_tsr = lst_tsr[:len(lst_tsr) -1]
    lst_tsq = lst_tsq[:len(lst_tsq) -1]

    for tsr_file in lst_tsr:
        with open("timestamp_files/tsr_files/" + tsr_file, "rb") as timestamp_file:
            encoded_string = base64.b64encode(timestamp_file.read())
        final_string = str(encoded_string)
        bdd_tsr[final_string] = tsr_file
        bdd_tsq[final_string] = lst_tsq[lst_tsr.index(tsr_file)]

initializeBdd()

@app.route('/')
def root():
    if auth:
        return render_template('index.html')
    else:
        return render_template('authentication.html')

@app.route('/authentication', methods=['POST'])
def authentication():
    nom = request.form['nom']
    mdp = request.form['mdp']
    global auth
    if nom == 'admin' and mdp == '1234':     
        auth = True
    else:
        auth = False
    return redirect('/')


@app.route('/formulaire')
def formulaire():
    if auth:
        return render_template('formulaire.html', creation="")
    else:
        return redirect('/')





#font = ImageFont.truetype("arial.ttf", 50)
def ajoutNomPrenom(nom, prenom, img):
    txt = nom + " " + prenom
    draw = ImageDraw.Draw(img)
    draw.text((700, 300),txt,(0,0,0))
    return img

def ajoutIntitule(intitule, img):
    draw = ImageDraw.Draw(img)
    draw.text((700, 400),intitule,(0,0,0))
    return img


def ajoutTxtVisible(nom, prenom, intitule, img1):

    img2 = ajoutNomPrenom(nom, prenom, img1)
    img = ajoutIntitule(intitule, img2)

    #font = ImageFont.truetype("times-ro.ttf", 34)
    #img = Image.open('image_test.png')
    #draw = ImageDraw.Draw(img)
    #draw.text((1000, 200),txt,(0,0,0))

def ajoutTxtInvisible(nom, prenom, intitule, timestamp, img):
    txt = nom + prenom + intitule
    while (len(txt) < 64):
        txt = txt + "0"
    bloc =  txt + timestamp 
    st.cacher(img, bloc)


def creerPass():
    #secret = pyotp.random_base32()
    secret = 'base32secret3232'
    totp = pyotp.TOTP(secret)
    return totp
    

def getTimestamp(img, nom, prenom, intitule):
    txt = nom + prenom + intitule
    request_file = txt + ".tsq"
    timestamp_file_name = txt + ".tsr"
    os.system("openssl ts -query -data " + img.filename + " -no_nonce -sha512 -cert -out " + request_file)
    os.system("curl -H \"Content-Type: application/timestamp-query\" --data-binary '@" + request_file + "' https://freetsa.org/tsr > " + timestamp_file_name)
    os.system("mv " + request_file + " timestamp_files/tsq_files/")
    os.system("mv " + timestamp_file_name + " timestamp_files/tsr_files/")

    with open("timestamp_files/tsr_files/" + timestamp_file_name, "rb") as timestamp_file:
        encoded_string = base64.b64encode(timestamp_file.read())
    final_string = str(encoded_string)
    bdd_tsq[final_string] = request_file
    bdd_tsr[final_string] = timestamp_file_name
    #print(final_string)
    return final_string



@app.route('/creation_diplome', methods=['POST'])
def creation_diplome():
    if auth:
        nom = request.form['nom']
        prenom = request.form['prenom']
        intitule = request.form['intitule']
        otp = request.form['otp']
        img = Image.open('image_test.png')

        totp = creerPass()

        if totp.verify(otp):
            timestamp=getTimestamp(img, nom, prenom, intitule)
            ajoutTxtVisible(nom, prenom, intitule, img)
            ajoutTxtInvisible(nom, prenom, intitule, timestamp, img)
            img.save('img2.png')
            return render_template('formulaire.html', creation="success")

        else:
            return render_template('formulaire.html', creation="OTP incorrect")
    
    else:
        return redirect('/')




@app.route('/verif_page')
def verifPage():
    if auth:
        return render_template('verifPage.html')
    else:
        return redirect('/')



def verifTimestamp(encoded):
    timestamp_file = bdd_tsr[encoded]
    request_file = bdd_tsq[encoded]
    verif = os.popen("openssl ts -verify -in timestamp_files/tsr_files/" + timestamp_file + " -queryfile timestamp_files/tsq_files/" + request_file + " -CAfile timestamp_files/cacert.pem -untrusted timestamp_files/tsa.crt").read()
    return verif 


@app.route('/verif_diplome', methods=['POST'])
def verifDiplome():
    if auth:
        img1 = request.files['img']
        img = Image.open(img1)
        nom = request.form['nom']
        prenom = request.form['prenom']
        intitule = request.form['intitule']
        txt = str(nom) + str(prenom) + str(intitule)
        while (len(txt)<64):
            txt = txt + "0"
        longueur = 64 + 7331
        msg = st.recuperer(img, longueur)
        bloc1 = msg[:64]
        bloc2 = msg[64:]
        #print("bloc1: " + bloc1)
        #print("txt: " + txt)
        #print("bloc2: " + bloc2)
        verif=verifTimestamp(bloc2)


        if bloc1 == txt and verif == "Verification: OK\n":
            ind = 1
        elif bloc1 != txt and verif != "Verification: OK\n":
            ind = 2
        elif bloc1 != txt:
            ind = 3
        elif verif != "Verification: OK\n":
            ind = 4
        return redirect(url_for('rapport', ind=ind))

    else:
        return redirect('/')


@app.route('/rapport/<int:ind>')
def rapport(ind):

    error1 = "-Le texte caché ne correspond pas avec les informations que vous avez rentrées."
    error2 = "-La vérification du timestamp a échoué."
    lst_errors = []
    if auth:
        if ind == 1:
            rapport = "Diplôme valide"
        elif ind == 2:
            rapport = "Diplôme invalide:"
            lst_errors.append(error1)
            lst_errors.append(error2)
        elif ind == 3:
            rapport = "Diplôme invalide:"
            lst_errors.append(error1)
        elif ind == 4:
            rapport = "Diplôme invalide:"
            lst_errors.append(error2)
        return render_template('rapport.html', rapport = rapport, lst_errors=lst_errors)

    else:
        return redirect('/')





if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
