from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import Bot
from bs4 import BeautifulSoup
import requests
import inspect
import sys
import re
import pyowm
import datetime
import simplejson as json




# defaults
DEFAULT_REPLY = "Sorry but I'm a complete wank"
ERRORS_TO = 'chris'

owm = pyowm.OWM('6a47e3b888d6f1962270697e72ed9f99')



# functions for the @listeners below

def tx(message):
    return message._body.get('text')



def getLocation(message):
    withweather = message._body.get('text')
    try:
        citweather, conweather = withweather.split('weather ', 1) 
    except ValueError:
        return False
    citarray = conweather.split()
    try:
        citarray[1]
    except IndexError:
        return False
    if(citarray[0] == "in"):
        local = citarray[1] + "," + citarray[2]
    else:
        local = citarray[0] + "," + citarray[1]
    return local
    
                       
###
def getBotWeather(weather, location):
    rawtemp = weather.get_temperature('fahrenheit')
    temp = rawtemp['temp']
    rawstatus = weather.get_detailed_status()
    status = rawstatus
    humidity = weather.get_humidity()
    weatherstring = 'The weather in ' + location + " is " + status + ' with a temperature of ' + str(temp) + '°F' + ' and a humidity of ' + str(humidity) +'%'
    return weatherstring


#@listen_to('trigger word')
#def functionName(message):
#code triggered by word
@listen_to('usefulbot help', re.IGNORECASE)
def usefulHelp(message):
    message.reply('Commands: weather [city] [state/country]')

@listen_to('usefulbot github',re.IGNORECASE)
def usefulGithub(message):
    message.reply('https://github.com/spartanboy56/usefulbot')    

#next on the todo list.
@listen_to('relevant xkcd', re.IGNORECASE)
def relevant(message):
    message.reply("I don't work yet. Someone build me")

@listen_to('weather', re.IGNORECASE)
def weather(message):
    location = getLocation(message)
    if(location == False):
        message.reply("Please use the proper formatting. weather [city] [state/country]")
    else:
        observation = owm.weather_at_place(location)
        w = observation.get_weather()
        weatherphrase = getBotWeather(w,location)
        message.reply(weatherphrase)

@respond_to('weekly releases', re.IGNORECASE)
def weeklyReleases(message):
    now = datetime.datetime.now()
    year = now.year
    year = str(year)
    year = year.strip('20')
    month = now.month
    print(year,month)
    page = requests.get('http://www.releases.com/l/games/'+ year + "/" + str(month))
    soup = BeautifulSoup(page.content)
    samples = soup.find_all("span", " day")
    print(samples)

#obtains the top news stories off of google news. Needs input sanitation.    
@respond_to('news', re.IGNORECASE)
def getNews(message):
    prejsonformatnews = requests.get('https://newsapi.org/v1/articles?source=google-news&sortBy=top&apiKey=015df2efbcaa49a8b16d3cd0caaaaae3')
    article = []

    for i in prejsonformatnews.json()['articles']:
        article = [i['title'],i['author'],i['description'],i['url']]
        #sometimes one of the articles will contain 'None'. For now it just skips them and moves on to the next.'
        try:
            message.send('*' + article[0] + '*' + "\n" + 'Author: ' + article[1] + "\n" + 'Description: ' + article[2] + "\n" + article[3])
        except TypeError:
            print('NoneType')



# main loop
def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    main()
