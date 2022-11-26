import os
import smtplib
import ssl
from email import encoders
from email.mime import text
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from colorama import Fore, Style, Back
from cryptography import x509
from M2Crypto import BIO, Rand, SMIME, X509
from cryptography.hazmat.primitives import serialization
import secrets_py

def makebuf(text, pdf_bytes):
    # create multipart message
    msg = MIMEMultipart()
    
    # attach message text as first attachment
    msg.attach(MIMEText(text))
    
    # attach files to be read from file system
    part = MIMEBase('application', "pdf")
    if pdf_bytes:
        part.set_payload(pdf_bytes)
    else:
        raise Exception("Pas de fichier PDF indiqué")
    
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % "diplome.pdf")
    msg.attach(part)
    
    # put message with attachments into into SSL' I/O buffer
    msg_str = msg.as_bytes()
    buf = BIO.MemoryBuffer(msg_str)
    
    return buf

# def verify():
#   # Instantiate an SMIME object.
#   s = SMIME.SMIME()
#
#   # Load the signer's cert.
#   x509 = X509.load_cert('certs/v4/key_sign_mail2.crt')
#   # x509 = X509.load_cert('certs/v4/cert_diplome_fin.crt')
#   sk = X509.X509_Stack()
#   sk.push(x509)
#   s.set_x509_stack(sk)
#
#   # Load the signer's CA cert. In this case, because the signer's
#   # cert is self-signed, it is the signer's cert itself.
#   st = X509.X509_Store()
#   st.load_info('certs/v4/CERT_WEB_4_DIPLOME.crt')
#   s.set_x509_store(st)
#
#   # Load the data, verify it.
#   p7, data = SMIME.smime_load_pkcs7('sign.p7')
#   v = s.verify(p7, data)
#   print(v)
#   # print(data)
#   # print(data.read())

def send_mail(text: str, destinataire: str, pdf_bytes: bytes | bytearray, sujet="M2Crypto S/MIME testing"):
    buf = makebuf(text, pdf_bytes)
    
    # Make a MemoryBuffer of the message.
    # buf = makebuf(b'a sign of our times')
    # with open("diplomes/diplome_239509144.pdf", encoding='utf-8', errors='replace') as opened:
    #   openedfile = opened.read()
    # buf.write(openedfile)
    
    # Seed the PRNG.
    Rand.load_file('randpool.dat', -1)
    
    # Instantiate an SMIME object; set it up; sign the buffer.
    s = SMIME.SMIME()
    s.load_key('certs/v5/key_sign_mail.key', 'certs/v5/key_sign_mail.crt')
    # s.load_key('certs/v4/key_sign_mail.key', 'certs/v4/key_sign_mail.crt')
    st = X509.X509_Store()
    st.load_info('certs/v4/CY_ROOT_SERVEUR_CA.crt')
    st.load_info('certs/v4/CA_ROOT_CY.crt')
    s.set_x509_store(st)
    p7 = s.sign(buf, SMIME.PKCS7_DETACHED)
    
    # Recreate buf.
    buf = makebuf(text, pdf_bytes)
    # buf.write(openedfile)
    
    # Output p7 in mail-friendly format.
    out = BIO.MemoryBuffer()
    out.write(f'From: {secrets_py.email}\n')
    out.write(f'To: {destinataire}\n')
    out.write(f'Subject: {sujet}\n')
    s.write(out, p7, buf)
    
    # load save seed file for PRNG
    Rand.save_file('/tmp/randpool.dat')
    
    # extend list of recipents with bcc adresses
    # to.extend(bcc)
    
    # finaly send mail
    sortie_smime_signee = out.read()
    print("Creation contexte SSL")
    context = ssl.create_default_context()
    
    # verify()
    
    with smtplib.SMTP_SSL(secrets_py.smtp, secrets_py.port, context=context) as server:
        print(Fore.LIGHTCYAN_EX+"Login..."+Fore.RESET)
        server.login(secrets_py.email, secrets_py.email_pw)
        print(Fore.LIGHTCYAN_EX+"Envoi..."+Fore.RESET)
        server.sendmail(secrets_py.email, destinataire, sortie_smime_signee)
        server.close()
        return sortie_smime_signee
    
if __name__ == "__main__":
    pdf = open("Mail/Diplomes/diplome_239509144.pdf", "rb").read()
    sortie_smime_signee = send_mail("Bonjour,\n\nCi-joint votre diplôme au format PDF.\n\nCordialement,"
                                    ,"loic.2010@live.fr", pdf, "Remise de vôtre diplôme")
    # print(out.read())
    sortie = open("sign.p7", 'wb')
    tx = sortie_smime_signee
    sortie.write(tx)
    sortie.close()
    
    # verify()