from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import Bot
import inspect
import sys
import re
import pyowm



# defaults
DEFAULT_REPLY = "Sorry but I'm a complete wank"
ERRORS_TO = 'chris'

owm = pyowm.OWM('6a47e3b888d6f1962270697e72ed9f99')



# functions for the @listeners below

def tx(message):
    return message._body.get('text')

def getLocation(message):
    withweather = message._body.get('text')
    noweather = withweather.strip('weather ')
    citweather, conweather = noweather.split(' ', 1) 
    citweather = citweather.strip(' ')
    local = citweather + ',' + conweather
    return local      
###
def getBotWeather(weather):
    rawtemp = weather.get_temperature('fahrenheit')
    temp = rawtemp['temp']
    rawstatus = weather.get_detailed_status()
    status = rawstatus
    humidity = weather.get_humidity()
    weatherstring = 'The weather is ' + status + ' with a temperature of ' + str(temp) + '°F' + ' and a humidity of ' + str(humidity) +'%'
    return weatherstring


#@listen_to('trigger word')
#def functionName(message):
#code triggered by word
@listen_to('usefulbot  ' or 'usefulbot help')
def usefulHelp(message):
    message.reply('Commands: weather [city] [state/country]')

@listen_to('usefulbot github')
def usefulGithub(message):
    message.reply('https://github.com/spartanboy56/usefulbot')    

#next on the todo list.
@listen_to('relevant xkcd', re.IGNORECASE)
def relevant(message):
    message.reply("I don't work yet. Someone build me")

@listen_to('weather', re.IGNORECASE)
def weather(message):
       location = getLocation(message)
       observation = owm.weather_at_place(location)
       w = observation.get_weather()
       message.reply(getBotWeather(w))

   



# main loop
def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    main()
