import requests

# API URL'si
url = "http://127.0.0.1:8000/user-suggestion/"
# Göndermek istediğiniz veriler
data = {
    "uid": "4345353425",
    "name": "John",
    "surname": "Doe",
    "usingCigar": True,
    "usingAlcohol": False,
    "height": 180,
    "weight": 75,
    "birth_date": "1994-09-12" 
}

response = requests.post(url, json=data)
print(response.status_code, response.text)
