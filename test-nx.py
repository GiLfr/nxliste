import requests

url = "https://unogsng.p.rapidapi.com/title"

querystring = {"netflixid":"81404896"}

headers = {
    'x-rapidapi-key': "90826ec83fmsh7438b570307f238p19e1f0jsnf5dd231dd200",
    'x-rapidapi-host': "unogsng.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)