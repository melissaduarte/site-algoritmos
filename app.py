from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

@app.route("/biografia")
def biografia():
  return render_template("biografia.html")

@app.route("/raspagem")
def raspagem():
  return render_template("raspagem.html")

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/enviar", methods=['POST'])
def email():
   nome_remetente = "Maria"
   email_remetente = "maria@gmail.com"
   email_destinatario = "melissa.mmod@gmail.com"
   nome_destinatario = "Melissa"
   assunto = "teste"
   mensagem = "Olá"
   enviar_email(email_remetente, nome_remetente, email_destinatario, nome_destinatario, assunto, mensagem)
   return "E-mail enviado!"


def enviar_email(email_remetente, nome_remetente, email_destinatario, nome_destinatario, assunto, mensagem):
  url = "https://api.brevo.com/v3/smtp/email"
  api_key = os.environ.get("BREVO_API_KEY")
  headers = {
      "accept": "application/json",
      "api-key": api_key,
      "content-type": "application/json",
  }
  data = {
      "sender": {
          "name": nome_remetente,
          "email": email_remetente
      },
      "to": [
          {
              "email": email_destinatario,
              "name": nome_destinatario
          }
      ],
      "subject": assunto,
      "htmlContent": mensagem ## Lembre de colocar em HTML
  }
  response = requests.post(url, json=data, headers=headers)
  print(response.text)
  print("Email enviado")

if __name__ == '__main__':
    app.run(debug=True)


@app.route("/")
def home():
   return render_template("layout.html")

@app.route("/teste")
def teste():
   return render_template("teste.html")


# Raspa as noticias da BBC
def bbc():
    url = 'https://www.bbc.com/portuguese/topics/c5qvpqj1dy4t'
    response = requests.get(url)
    noticias_bbc = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links_titulos = soup.find_all('div', class_='bbc-bjn8wh e1v051r10')
        for link_titulo in links_titulos:
            titulo = link_titulo.find('a').text
            link = link_titulo.find('a')['href']
            noticias = {"titulo": titulo, "link": link} 
            noticias_bbc.append(noticias)
    return noticias_bbc

@app.route("/bbcresultado")
def bbcresultado():
    noticias_bbc = bbc()
    return render_template('resultadoraspagem.html', noticias_bbc=noticias_bbc)

if __name__ == '__main__':
    app.run(debug=True)