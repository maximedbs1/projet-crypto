import base64
import os
import smtplib

sender_email = "maximeygg02@gmail.com"
rec_email = "maxime.dubus0@gmail.com"
password = input(str("Please enter your email password : ")) #rclphkqivtrxthho

with open("image_test.png", "rb") as img_file:
    b64_string = base64.b64encode(img_file.read())
    print("image is encoded")

MIMEHeader = "Content-Type: image/png\r\nContent-Transfer-Encoding: base64\r\n"
message_content = MIMEHeader + str(b64_string)

with open("Mail/content.txt", "w") as content_file:
    content_file.write(message_content)
    print("email is built")

os.system("cat Mail/content.txt | openssl smime -signer CA/ca.pem -from 'maximeygg02@gmail.com' -to 'maxime.dubus0@gmail.com' -subject 'Envoi avec signature' -sign -inkey CA/private/ca.key -out final_message.txt")
print("email is signed")

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender_email, password)
print("login success")
with open("final_message.txt", "r") as final_message:
    to_send = final_message.read()
    server.sendmail(sender_email, rec_email, to_send)
    print("email has been sent to ", rec_email)
    
server.quit()
print("server is closed")