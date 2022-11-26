import os
import binascii
import qrcode
import cv2

# Choisir la fonctionnalité
print("1: Sign info\n2: Verify info")
command = int(input())

# Sign info
if command == 1:
    
    # Entrer les informations à signer
    Nom = str(input("Nom : "))
    Prenom = str(input("Prenom : "))
    Diplome = str(input("Intitulé du diplome : "))

    # Les regrouper en un bloc
    info_bloc = Nom + Prenom + Diplome

    # Ecrire ce bloc dans un fichier
    with open("SignInfo/info_file.txt", "w") as infofile:
        infofile.write(info_bloc)

    # Signer + Encoder ce fichier dans un nouveau fichier
    os.system("openssl dgst -sign CA/private/diplomaca.key -keyform PEM -sha256 -out SignInfo/info_file.txt.sign -binary SignInfo/info_file.txt")
    
    # Ouvrir le fichier encodé et signé
    with open("SignInfo/info_file.txt.sign", "rb") as signedfile:
        signed_info = signedfile.read()
    
    # Convertir les infos en ascii
    ascii_info = binascii.b2a_hex(signed_info)
    
    # Créer le qrcode à partir de cette string ascii
    qrcode_img = qrcode.make(ascii_info)
 
    # Sauvegarder le qrcode dans une image
    qrcode_img.save('SignInfo/signed_info_QRcode.png')
    
# Verify info
else:
    # Aller chercher la clé publique du CA pour la vérification
    os.system("openssl x509 -pubkey -noout -in CA/certs/diplomaca.pem  > VerifyInfo/pubkey.pem")
    
    # Entrer les informations qu'on est censés retrouver
    Nom = str(input("Nom : "))
    Prenom = str(input("Prenom : "))
    Diplome = str(input("Intitulé du diplome : "))

    # Les regrouper en un bloc
    info_bloc = Nom + Prenom + Diplome

    # Ecrire ce bloc dans un fichier
    with open("VerifyInfo/info_file.txt", "w") as infofile:
        infofile.write(info_bloc)
    
    # Lire le qrcode
    qrcode_img = cv2.imread("SignInfo/signed_info_QRcode.png")
    det = cv2.QRCodeDetector()
    
    # Récupérer les infos dans la variable val (on s'occupe pas des autres variables)
    val, pts, st_code = det.detectAndDecode(qrcode_img)
    
    # Reconvertir ces infos ascii en bytes hexa
    binary_info = binascii.a2b_hex(val)
    
    # Ecrire ces infos (encodées et signées) dans un fichier
    with open("VerifyInfo/info_file.txt.sign", "wb") as signedfile:
        signedfile.write(binary_info)
    
    # Vérifier la signature de ces infos avec la clé pub + vérifier qu'elles concordent avec les infos qu'on a donné au début
    os.system("openssl dgst -verify VerifyInfo/pubkey.pem -keyform PEM -sha256 -signature VerifyInfo/info_file.txt.sign -binary VerifyInfo/info_file.txt")