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
    citweather, conweather = withweather.split('weather ', 1) 
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

   



# main loop
def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    main()
