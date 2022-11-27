import os
import binascii
import qrcode
from PIL import Image
from pyzbar.pyzbar import decode


def create_qrcode(nom, prenom, intitule):
    # Les regrouper en un bloc
    info_bloc =  nom + prenom + intitule

    # Ecrire ce bloc dans un fichier
    with open("SignInfo/info_file.txt", "w") as infofile:
        infofile.write(info_bloc)

    # Signer + Encoder ce fichier dans un nouveau fichier
    os.system("openssl dgst -passin pass:bonsoir -sign CA/private/diplomaca.key -keyform PEM -sha256 -out SignInfo/info_file.txt.sign -binary SignInfo/info_file.txt")
    
    # Ouvrir le fichier encodé et signé
    with open("SignInfo/info_file.txt.sign", "rb") as signedfile:
        signed_info = signedfile.read()
    
    # Convertir les infos en ascii
    ascii_info = binascii.b2a_hex(signed_info)

    # Créer le qrcode à partir de cette string ascii
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=2, border=4)
    qr.add_data(ascii_info)
    qr.make(fit=True)
    
    # Convertir le qrcode en image
    qrcode_img = qr.make_image()

    return qrcode_img


def verif_qrcode(nom, prenom, intitule):
    # Aller chercher la clé publique du CA pour la vérification
    os.system("openssl x509 -pubkey -noout -in CA/certs/diplomaca.pem  > VerifyInfo/pubkey.pem")

    # Les regrouper en un bloc
    info_bloc = nom + prenom + intitule

    # Ecrire ce bloc dans un fichier
    with open("VerifyInfo/info_file.txt", "w") as infofile:
        infofile.write(info_bloc)
    
    # Lire le qrcode
    img = Image.open('extracted_qrcode.png')
    decoded_list = decode(img)
    val=decoded_list[0].data
    
    # Reconvertir ces infos ascii en bytes hexa
    binary_info = binascii.a2b_hex(val)
    
    # Ecrire ces infos (encodées et signées) dans un fichier
    with open("VerifyInfo/info_file.txt.sign", "wb") as signedfile:
        signedfile.write(binary_info)
    
    # Vérifier la signature de ces infos avec la clé pub + vérifier qu'elles concordent avec les infos qu'on a donné au début
    verif = os.popen("openssl dgst -verify VerifyInfo/pubkey.pem -keyform PEM -sha256 -signature VerifyInfo/info_file.txt.sign -binary VerifyInfo/info_file.txt").read()

    os.system("rm -Rf extracted_qrcode.png")
    return verif
    