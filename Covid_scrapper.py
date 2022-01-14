#modules
import requests
import pyttsx3
import json
import speech_recognition as sr
import re

API_KEY = "tTuRT16jTOLq"
PROJECT_TOKEN = "tK43FuDy5pyO"
RUN_TOKEN = "tFG-Oyi3sn9_"

#call get request from api on parsehub
#url to access info and return in json format                                       #get last run we did    #authentication for the get request


#setup a class
class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {                     #authentication for every request we pass
            "api_key": self.api_key
        }
        self.get_data = self.get_data()
#call the data from .get and set the data attribute for the object
    def get_data(self):
        response = requests.get(f"https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data", params= self.params)
        self.data = json.loads(response.text)

#parsing specific data
    def get_total_cases(self):
        data = self.data['Total']
#if the content name when we're looping through 'data' is equal to 'name' return content value
        for content in data:
            if content ['name'] == "Coronovirus Cases:":
                return content ['Value']

    def get_total_deaths(self):
        data = self.data['Total']

        for content in data:
            if content['name'] == "Deaths:":
                return content['Value']

    def get_total_recovered(self):
        data = self.data['Total']

        for content in data:
            if content['name'] == "Recovered:":
                return content['Value']

    #info related to countried

    def get_country_data(self, country):
        data = self.data["country"]

        for content in data:
            if content['name'].lower() == country.lower():
                return content

        return "0"

data = Data(API_KEY, PROJECT_TOKEN)



def speak(text):            #define a function that takes text
    engine = pyttsx3.init() #initialize engine
    engine.say(text)
    engine.runAndWait()

#speak and listen to us


def get_audio():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		audio = r.listen(source)
		said = ""

		try:
			said = r.recognize_google(audio)
		except Exception as e:
			print("Exception:", str(e))

	return said.lower()


def main():
	print("Started Program")
	data = Data(API_KEY, PROJECT_TOKEN)
	END_PHRASE = "stop"
	country_list = data.get_list_of_countries()

	TOTAL_PATTERNS = {
					re.compile("[\w\s]+ total [\w\s]+ cases"):data.get_total_cases,
					re.compile("[\w\s]+ total cases"): data.get_total_cases,
                    re.compile("[\w\s]+ total [\w\s]+ deaths"): data.get_total_deaths,
                    re.compile("[\w\s]+ total deaths"): data.get_total_deaths
					}

	COUNTRY_PATTERNS = {
					re.compile("[\w\s]+ cases [\w\s]+"): lambda country: data.get_country_data(country)['total_cases'],
                    re.compile("[\w\s]+ deaths [\w\s]+"): lambda country: data.get_country_data(country)['total_deaths'],
					}

	UPDATE_COMMAND = "update"


while True:
    print("Listening...")
    text = get_audio()
    print(text)
    result = None

    for pattern, func in COUNTRY_PATTERNS.items():
        if pattern.match(text):
            words = set(text.split(" "))
            for country in country_list:
                if country in words:
                    result = func(country)
                    break

    for pattern, func in TOTAL_PATTERNS.items():
        if pattern.match(text):
            result = func()
            break

    if text == UPDATE_COMMAND:
        result = "Data is being updated. This may take a moment!"
        data.update_data()

    if result:
        speak(result)

    if text.find(END_PHRASE) != -1:  # stop loop
        print("Exit")
        break

main()

r.json()