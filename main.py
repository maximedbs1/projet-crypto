from flask import Flask, render_template, request, redirect, url_for
from PIL import Image 

import pyotp
import os

import timestamp as tmstp
import ajout_texte as aj_txt
import stegano as st
import sign_verify as sv
import testmail as tm


app = Flask(__name__)

tmstp.initializeBdd()

auth = False


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




def creerPass():
    secret = 'KillyanPovoaMaximeDubus'
    totp = pyotp.TOTP(secret)
    return totp


@app.route('/creation_diplome', methods=['POST'])
def creation_diplome():
    if auth:
        nom = request.form['nom']
        prenom = request.form['prenom']
        intitule = request.form['intitule']
        mail = request.form['mail']
        otp = request.form['otp']
        img = Image.open('image_test.png')

        totp = creerPass()

        if totp.verify(otp):
            timestamp = tmstp.getTimestamp(img, nom, prenom, intitule)
            aj_txt.ajoutTxt(nom, prenom, intitule, timestamp, img)
            qrcode = sv.create_qrcode(nom, prenom, intitule)
            img.paste(qrcode, (1430, 950))
            img.save('img2.png')
            tm.envoi_mail(mail)
            os.system("rm -Rf img2.png")
            return redirect(url_for('conf_creation', ind=0))

        else:
            return redirect(url_for('conf_creation', ind=1))
    
    else:
        return redirect('/')

@app.route('/conf_creation/<int:ind>')
def conf_creation(ind):
    if ind == 0:
        rapport = "Diplôme créé et envoyé avec succès."
    else:
        rapport = "Erreur lors de la création du diplôme. L'OTP fourni est inexact."
    return render_template('conf_creation.html', rapport=rapport)


@app.route('/verif_page')
def verifPage():
    if auth:
        return render_template('verifPage.html')
    else:
        return redirect('/')



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
        
        verif_tmstp = tmstp.verifTimestamp(bloc2)
        img.crop((1430, 950, 1600, 1120)).save('extracted_qrcode.png')

        verif_qrcode=sv.verif_qrcode(nom, prenom, intitule)
        
        bool1 = bloc1 == txt 
        bool2 = verif_tmstp == "Verification: OK\n"
        bool3 = verif_qrcode == "Verified OK\n"


        if bool1 and bool2 and bool3 :
            ind = 1
        elif not bool1 and not bool2 and not bool3:
            ind = 2
        elif not bool1 and not bool2:
            ind = 3
        elif not bool1 and not bool3:
            ind = 4
        elif not bool3 and not bool2:
            ind = 5
        elif not bool1:
            ind = 6
        elif not bool2:
            ind = 7
        elif not bool3:
            ind = 8
        return redirect(url_for('rapport', ind=ind))

    else:
        return redirect('/')


@app.route('/rapport/<int:ind>')
def rapport(ind):

    error1 = "-Le texte caché ne correspond pas avec les informations que vous avez rentrées."
    error2 = "-La vérification du timestamp a échoué."
    error3 = "-La vérification de la signature a échoué."
    lst_errors = []

    if auth:
        if ind == 1:
            rapport = "Diplôme valide"
        elif ind == 2:
            rapport = "Diplôme invalide"
            lst_errors.append(error1)
            lst_errors.append(error2)
            lst_errors.append(error3)
        elif ind == 3:
            rapport = "Diplôme invalide"
            lst_errors.append(error1)
            lst_errors.append(error2)
        elif ind == 4:
            rapport = "Diplôme invalide"
            lst_errors.append(error1)
            lst_errors.append(error3)
        elif ind == 5:
            rapport = "Diplôme invalide"
            lst_errors.append(error2)
            lst_errors.append(error3)
        elif ind == 6:
            rapport = "Diplôme invalide"
            lst_errors.append(error1)
        elif ind == 7:
            rapport = "Diplôme invalide"
            lst_errors.append(error2)
        elif ind == 8:
            rapport = "Diplôme invalide"
            lst_errors.append(error3)
        return render_template('rapport.html', rapport = rapport, lst_errors=lst_errors, ind=ind)

    else:
        return redirect('/')





if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
