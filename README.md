# projet-crypto

## TODO

- AC :
    - Chercher où implémenter l'AC
    - Créer l'AC
    - Créer certificat permettant la signature
- Mail :
    - Envoi de courrier avec smtplib
    - Envoi de courrier sécurisé avec S/MIME (openssl)

<br/>

- Page "Créer certificat" :
  - Formulaire de saisie : 
    - Nom 
    - Prénom
    - intitulé de la formation
    - email de l'étudiant
    - OTP
  - *Verification de l'OTP*
  - Création de l'image :
    - Utilisation du template
    - *Création du QRcode contenant la signature en ASCII*
    - Intégration du texte en clair (Nom, Prénom, Intitulé de la formation)
    - Construction du bloc d'info secret AVEC TIMESTAMP
    - Insérer ce bloc dans l'image par stégano
    - *Insertion du QRcode*
  - Envoi de l'image par courrier sécurisé S/MIME
- Page "Extraire preuve"
  - Upload de fichier image (png)
  - Extraction des infos cachées (code exemple)
  - Extraction des infos visibles
  - Comparaison des deux
  - Vérifier timestamp
  - *Vérifier certification (dans QRcode) avec clé publique de l'autorité*
  - Afficher le résultat

## Rappel Travail à réaliser

- créer une AC avec une configuration bien choisie
- créer un certificat permettant la signature ;
- créer un programme construisant un OTP à la manière de celui utilisé par Google ;
- choisir un algorithme de signature et déduire la taille n de la signature ;
- écrire l’application chargée de traiter les données soumises par l’utilisateur :
  - calcul OTP et comparaison avec celui fourni à l’application ;
  - construction du bloc d’informations à insérer dans l’image (concaténations et
signature) ;
  - insertion de ce bloc par stéganographie et envoi sécurisé de l’image obtenue ;
  - envoi par courrier au format S/MIME, dérivé de PKCS#7.
- créer le programme d’extraction de preuve permettant de vérifier l’attestation.
