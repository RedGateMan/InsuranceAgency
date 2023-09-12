import requests


def get_joke_of_the_day():
	request = requests.get('https://icanhazdadjoke.com', headers={'Accept': 'application/json'})
	response = request.json()
	return response['joke']
