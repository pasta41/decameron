import requests

url = "http://backend.bibliotecaitaliana.it/wp-json/muruca-core/v1/xml/bibit000267"

response = requests.get(url)
with open('../data/raw-decameron.xml', 'wb') as file:
    file.write(response.content)
