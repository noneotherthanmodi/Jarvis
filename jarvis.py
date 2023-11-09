#query - your audio or command from your mouth
#chatStr - Jarvis random talks 


import speech_recognition as sr 
import win32com.client
import webbrowser
import os 
import openai
import datetime

from config import apikey, weather_api, news_api
import requests





speaker = win32com.client.Dispatch("SAPI.SpVoice")

chatStr = ""



#random chat
def chat(query):
    global chatStr
    chatStr += f"Sir : {query} \n Jarvis: "
    openai.api_key = apikey



    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=1,                 # (R->0-2)higher the temp more "creative and randomness" in your model answer you will get, Think it of as a level of surprise or unpredictability in models responses.
        max_tokens=256,
        top_p=1,                       #top-percentage - another parameter that is used to generate randomness in your language model by nlp.helps in generating diverse and interesting languages
                                       # -> helps to choose the next word in a sentence. Instead of similar words it chooses more diversified words everytime. eg- i like to have 'cereals, pancakes' in breakfast, instead of 'eggs and toasts'.
  
        frequency_penalty=0,
        presence_penalty=0
    )


    #todo : wrap this inside a try catch case to check for 0th choices generated or not 
    speaker.Speak(response['choices'][0]['text'])
    chatStr= f"{response['choices'][0]['text']}"
    return response['choices'][0]['text']






#AI
def ai(prompt):
    openai.api_key = apikey
    text = f"Open AI response for Prompt - {prompt} \n *******************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )


    #todo : wrap this inside a try catch case to check for 0th choices generated or not 
    print(response['choices'][0]['text'])
    text += response['choices'][0]['text']

    if not os.path.exists("Openai"):
            os.mkdir("Openai")


    with open(f"Openai/{''.join(prompt.split('intelligence')[1:])}", "w") as f:
        f.write(text)





    

#listens to our command through microphone/audio
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1      #0.8 is default
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language= "en-in")
            print(f"User said: {query}")
            return query
        
        except Exception as e :
            speaker.Speak("Some Error Occurred. Sorry from Jarvis.")
            return "Some Error Occurred. Sorry from Jarvis."







#weather
def weather(api_key, city_id):
    api_key = weather_api
   
      # Moscow
    apiurl = "http://api.openweathermap.org/data/2.5/weather?" 
    params = {
        "id" : city_id,
        "units" : "metric",
        "appid": api_key
        }
    
    
    url = apiurl + "appid=" + api_key + "&q=" + city_id
    response = requests.get(url, params = params)
    data = response.json()
    # speaker.Speak(data)
    return data

def get_temp(data):
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    feels_like = data['main']['feels_like']
    

    return f"'temperature' :{temperature},'humidity':{humidity},'feels_like':{feels_like}"











#news 
def get_news():
    n = int(input("enter the number of news you want to know : "))
    key = news_api
    apiurl2 = 'https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey='+key
    
    response = requests.get(apiurl2)    
    data = response.json()
    # print(data)
    articles = data['articles']
    # print(articles)

    news_article = []
    for arti in articles:
        news_article.append(arti['title'])
        news_article.append(arti['description'])

    # print(news_article)
    
    for i in range(n):
        print(i+1,news_article[i])

    return data






#THE MAIN FUNCTION
if __name__ == "__main__":
    # print("Enter the word you want computer to speak")
    # s = input()
    speaker.Speak("Hellow im jarvis, a virtual assistant.")
    datetime.datetime.now()
    while True:
        print("Listening...")
        query = takecommand()
        # speaker.Speak(query)


        sites = [["youtube","https://www.youtube.com/"], ['wikipedia','https://www.wikipedia.org/'],
                 ["google","https://www.google.com/"], ['music','https://www.jiosaavn.com/featured/mere-ram/b6AFSx-Sh4XuCJW60TJk1Q__']]

        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                speaker.Speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        if "play music".lower() in query:
            musicPath = "D:\Starboy - The Weeknd-(DJMaza).mp3"
            os.system(f"start '{musicPath}'")


        elif "the time".lower() in query:
            strftime = datetime.datetime.now().strftime("%H:%M:%S")
            speaker.Speak(f"Sir the time is {strftime}")
            print(strftime)

        elif "the date".lower() in query.lower():
            strfdate = datetime.date.today()
            speaker.Speak(strfdate)
            print(strfdate)

        elif "camera".lower() in query.lower():
            os.system(f"start  '00000007'")

        
        elif "artificial intelligence".lower() in query.lower():
            ai(prompt=query)
       


        elif "Jarvis quit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        

        elif "weather of".lower() in query.lower():
            cities = [['bangalore'],['kolkata'],['patna'],['mumbai'],['Gorakhpur'],['lucknow'],['gaya'],['delhi'],['london']]       
            
            for city in cities:
                if f"weather of {city[0]}".lower() in query.lower():
                    dataa = weather(api_key=weather_api, city_id=f"{city[0]}")
                    print(dataa)


            temperature = get_temp(dataa)
            print(f"temp : {temperature} C")
            speaker.Speak(temperature)



        elif f"news".lower() in query.lower():
            get_news()
            
            
            # speaker.Speak(newss)



        else:
            print("chatting...")
            chat(query)

        
        
        
        