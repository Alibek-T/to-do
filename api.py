import requests
from apikey import API_KEY


url = "https://weatherapi-com.p.rapidapi.com/current.json"
headers = {
    'X-RapidAPI-Key': API_KEY,
    'X-RapidAPI-Host': 'weatherapi-com.p.rapidapi.com'
}
params = {
    'q': 'Astana'
}

response = requests.get(
    url=url,
    headers=headers,
    params=params
)

if response:
    data = response.json()
    City = 'City: ' + data['location']['name']
    Date = 'Date: ' + data['location']['localtime'][0:10]
    Temperature = 'Temperature now: ' + str(data['current']['temp_c']) + " oC"
    Wind = "Wind speed now: " + str(data['current']['wind_kph']) + " km/h"
    print(City)
    print(Date)
    print(Temperature)
    print(Wind)

else:
    print("there is an error")
    print(response)
