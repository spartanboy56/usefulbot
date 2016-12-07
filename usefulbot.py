from slackbot.bot import respond_to
from slackbot.bot import listen_to
from os.path import dirname
from slackbot.bot import Bot
import inspect
import sys
import re
import random
import pyowm

#sys.path.append(dirname("/home/jbird/dicemaniac/"))
# to get the slackbot_settings.py file that contains the API token

# some default info
DEFAULT_REPLY = "Sorry but I'm a complete wank"
ERRORS_TO = 'jeremy'

owm = pyowm.OWM('6a47e3b888d6f1962270697e72ed9f99')


######
# IMPORTANT MACROS
###
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
#####

### custom plugins. let's see if this actually works.


@listen_to('usefulbot help')
def usefulHelp(message):
    message.reply('Commands: weather [city] [state/country]')

@listen_to('relevant xkcd', re.IGNORECASE)
def relevant(message):
    message.reply('I no work yet!')

@listen_to('weather', re.IGNORECASE)
def weather(message):
    if(re.search('weather', tx(message))):
       location = getLocation(message)
       observation = owm.weather_at_place(location)
       w = observation.get_weather()
       outputweather = getBotWeather(w)
       message.reply(outputweather)

   
# Revamped roll function. Checking for + and - modifiers at the end. Maybe separate functions per scenario?


# main loop
def main():
    bot = Bot()
    bot.run()

# no idea why this is necesary but the docs said to put this here lol
if __name__ == "__main__":
    main()
