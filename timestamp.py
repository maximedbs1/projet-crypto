import os
import base64

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
    return final_string

def verifTimestamp(encoded):
    timestamp_file = bdd_tsr[encoded]
    request_file = bdd_tsq[encoded]
    verif = os.popen("openssl ts -verify -in timestamp_files/tsr_files/" + timestamp_file + " -queryfile timestamp_files/tsq_files/" + request_file + " -CAfile timestamp_files/cacert.pem -untrusted timestamp_files/tsa.crt").read()
    return verif 
