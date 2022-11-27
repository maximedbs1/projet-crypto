import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

def envoi_mail(receveur) :
    sender = "maximeygg02@gmail.com"
    mdp = "rclphkqivtrxthho"
    subject="Diplôme Cy Tech"
    text="Bonjour\nVous trouverez ci-joint un diplôme authentique délivré par CY Tech.\nCordialement"
    files = ["img2.png"]

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receveur
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)


    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(sender, mdp)
    smtp.sendmail(sender, receveur, msg.as_string())
    smtp.close()
    

