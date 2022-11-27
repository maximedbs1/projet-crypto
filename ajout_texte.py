from PIL import ImageFont
from PIL import ImageDraw
import stegano as st


font = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 80)

def ajoutNomPrenom(nom, prenom, img):
    txt = nom + " " + prenom
    draw = ImageDraw.Draw(img)
    draw.text((600, 500),txt,(0,0,0),font=font)
    

def ajoutIntitule(intitule, img):
    draw = ImageDraw.Draw(img)
    draw.text((600, 600),intitule,(0,0,0),font=font)
    


def ajoutTxtVisible(nom, prenom, intitule, img):
    ajoutNomPrenom(nom, prenom, img)
    ajoutIntitule(intitule, img)

def ajoutTxtInvisible(nom, prenom, intitule, timestamp, img):
    txt = nom + prenom + intitule
    while (len(txt) < 64):
        txt = txt + "0"
    bloc =  txt + timestamp 
    st.cacher(img, bloc)

def ajoutTxt(nom, prenom, intitule, timestamp, img):
    ajoutTxtVisible(nom, prenom, intitule, img)
    ajoutTxtInvisible(nom, prenom, intitule, timestamp, img)