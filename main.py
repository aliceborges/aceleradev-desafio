import requests
import json
import string
import hashlib


def request(url, method, params, files):
    if method == 'get':
        content = requests.get(url, params=params)
        return content.text
    if method == 'post':
        content = requests.post(url, params=params, files=files)
        return content.text


def open_json(path):
    with open(path) as json_file:
        content = json.loads(json_file.read())
        return content


def index(list, position):
    if position < 0:
        return index(list, len(list) + position)
    else:
        return position


def decifrar_texto(texto_cifrado, numero_casas):
    texto_decifrado = ''
    alfabeto = list(string.ascii_lowercase)
    for caracter in texto_cifrado:
        if caracter in alfabeto:
            texto_decifrado += alfabeto[index(alfabeto, alfabeto.index(caracter) - numero_casas)]
        else:
            texto_decifrado += caracter
    return texto_decifrado


def sha1(text):
    return hashlib.sha1(text.encode('utf-8')).hexdigest()


def main():
    params = {'token': '5ee52b7ba40304df4467ab2b85e462b726f75ca8'}
    content = request('https://api.codenation.dev/v1/challenge/dev-ps/generate-data', 'get', params, 0)

    if content:
        arquivo = open('answer.json', 'w')
        arquivo.write(content)
        arquivo.close()

        json_file = open_json('answer.json')
        if json_file:
            cifrado = json_file['cifrado']
            numero_casas = json_file['numero_casas']
            texto_decifrado = decifrar_texto(cifrado, numero_casas)
            resumo_criptografico = sha1(texto_decifrado)
            json_file['decifrado'] = texto_decifrado
            json_file['resumo_criptografico'] = resumo_criptografico

            with open('answer.json', 'w') as outfile:
                json.dump(json_file, outfile)

            files = {'answer': ('answer.json', open('answer.json', 'rb'))}

            envio = request('https://api.codenation.dev/v1/challenge/dev-ps/submit-solution', 'post', params, files)
            print('Enviado! Resposta: ', envio)


main()
