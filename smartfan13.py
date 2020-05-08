##
#!/usr/bin/python
# smart fan by Granpino. June 2019
# Rev1.3
import sys, pygame
from pygame.locals import *
import time
import datetime
import subprocess
import Adafruit_DHT
import os
import requests

pygame.init()

settings = {
    'api_key':'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'zip_code':'44100',
    'country_code':'MX',
    'temp_unit':'metric'} #unit can be metric, imperial, or kelvin

set_point = 25 # setpoint of desired temperature

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?appid={0}&zip={1},{2}&units={3}"

## dh100 smart plug IP
hs100_1IP = '192.168.0.198'
#hs100_2IP = '192.168.0.149' # second smart plug if needed
HS100 = False
plug_status = '??'
degSymF = unichr(0x2109)         # Unicode for Degree F
degSymC = unichr(0x2103)	 #Unicode for Deg C
degSym = unichr(0x00B0)          #unicode for degree symbol
pin = '4' 
sensor = Adafruit_DHT.DHT22
inhibit = False
current_time = "00:00"

#set size of the screen
size = width, height = 650, 410  #To fit in a 720x480 screen

#screen = pygame.display.set_mode(size) # use this for troubleshooting
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

#define colors
cyan = 50, 255, 255
blue = 130, 75, 200
black = 0, 0, 0
white = 255, 235, 235
lblue = 75, 140, 200
green = 0, 255, 0
silver = 192, 192, 192
yellow = 255, 255, 0


temp = 0

localH = 0
localT = 0

#define function that checks for mouse location
def on_click():
    print('clicked')
    #check to see if exit has been pressed
    if 599 < click_pos[0] < 639 and 1 < click_pos[1] < 41:
#	print "-- exit" 
	button(0)
	#now check to see if play was pressed
    if 540 <= click_pos[0] <= 580 and 70 <= click_pos[1] <=110:
#        print "-- up"
        button(1)
	#now check to see if mp3 was pressed
    if 540 <= click_pos[0] <= 580 and 280 <= click_pos[1] <=320:
#        print "-- down"
        button(2)
	#now check to see if previous  was pressed
    if 22 <= click_pos[0] <= 128 and 270 <= click_pos[1] <=304:
        print "-- Future button"
        button(3)


#define action on pressing buttons
def button(number):
    global set_point
    print "You pressed button ",number
    if number == 0:    # exiting
	screen.fill(black)
	font=pygame.font.Font(None,30)
        subprocess.Popen(["sudo", "./hs100.sh", "-i", hs100_1IP, "off"]) 
 #       subprocess.Popen(["sudo", "./hs100.sh", "-i", hs100_2IP, "off"]) #second plug
	label=font.render("Turning HS100 OFF! ", 1, (white))
        screen.blit(label,(40,170))
	pygame.display.flip()
	time.sleep(2)
	pygame.quit()
	sys.exit()

    if number == 1: # -- up
        set_point += 1
        print(set_point)
        refresh_screen()

    if number == 2: # -- down
        set_point -= 1
	print('down')
	refresh_screen()

    if number == 3: #  -- Future button

	refresh_screen()
# ========================================

def __del__(self):
	"Destructor to make sure pygame shuts down"


def update_weather():
    global current_temperature 
    global current_humidity
    global HS100
    global city_name
    global sunrise
    print ('updating weather')
    print (current_time)
    final_url = BASE_URL.format(settings["api_key"],settings["zip_code"],settings["country_code"],settings["temp_unit"])
    weather_data = requests.get(final_url).json()
    response = requests.get(final_url)
    x = response.json()
    zip_code = (settings["zip_code"])
    if x["cod"] != "404":
            y = x["main"]
	    city_name = x["name"]
	    current_temperature = y["temp"]
	    feels_like = y["feels_like"]
	    current_humidity = y["humidity"]
	    temp_max = y["temp_max"]
	    temp_min = y["temp_min"]

	    z = x["weather"]
	    weather_description = z[0]["description"]
	    Icon = z[0]["icon"]

            u = x["sys"]
            sunrise = u["sunrise"]


       # check for temperature and control the smart plug 
    if float(localT) >= set_point and float(current_temperature) < float(localT) and HS100 == False and inhibit == False:
        subprocess.Popen(["sudo", "./hs100.sh", "-i", hs100_1IP, "on"]) 
       # subprocess.Popen(["sudo", "./hs100.sh", "-i", hs100_2IP, "on"])

        print('Plug is ON')
        HS100 = True

    if float(current_temperature) > float(localT) and HS100 == True:
        subprocess.Popen(["sudo", "./hs100.sh", "-i", hs100_1IP, "off"]) 
       # subprocess.Popen(["sudo", "./hs100.sh", "-i", hs100_2IP, "off"])
        HS100 = False
        print(HS100)
        print(plug_status)

    if float(localT) < set_point and HS100 == True:
        subprocess.Popen(["sudo", "./hs100.sh", "-i", hs100_1IP, "off"]) 
       # subprocess.Popen(["sudo", "./hs100.sh", "-i", hs100_2IP, "off"])
        print('plug is off')
        HS100 = False
 
#============================================

def refresh_screen():
#set up the fixed items on the menu
    global current_temperature
    global localT
    global current_time

    current_time = datetime.datetime.now().strftime('%H:%M')
    time_font=pygame.font.Font(None,36)
    time_label = time_font.render(current_time, 1, (silver)) 
    IP_label = time_font.render(hs100_1IP, 1, (silver))

    sfont = pygame.font.SysFont('sans', 20, bold=0)
    d_font = pygame.font.SysFont('sans', 30, bold=1)
    mfont = pygame.font.SysFont( 'sans', 50, bold=1)
    lfont = pygame.font.SysFont( 'sans', 110, bold=0)
    fontL = pygame.font.Font(None,32)
    skin = pygame.image.load("720skin.jpg")
    status_lbl = sfont.render('HS100', 1, (white))
    x_lbl = sfont.render('X', 1, (white))
    setP_lbl = mfont.render( str(set_point), 1, (cyan))

    screen.blit(skin,(0,0))

	# Outside Temp
    current_temperature = int(current_temperature)
    outsideT_lbl = mfont.render(str(current_temperature), 1, cyan )

    outside = sfont.render('Outside', True, white)
    outsideH = sfont.render(str(current_humidity) + '%', 1, silver)
	# Show degree  symbol
    degree = d_font.render( degSym, 1, cyan )

	# Local Temp
    insideT = lfont.render(str(localT), 1, cyan )
    localH_lbl = sfont.render('Humidity ' + str(localH) +'%', 1, silver)
    SetAt_lbl = sfont.render('Set to', 1, white)
    inside = sfont.render('Inside', 1, white)
    cityLbl = sfont.render(str(city_name), 1, white) # location

	# Show degree  F or C symbol 
    deg_symbol = d_font.render( degSymC, 1, cyan ) # use degSymC for deg C

    #put the main elements on the screen 

    pygame.draw.rect(screen, blue, (540, 70, 40, 40),0)
    pygame.draw.rect(screen, blue, (540, 280, 40, 40),0)
    pygame.draw.rect(screen, lblue, (599, 1, 40, 40), 0)

    if HS100 == True:
        pygame.draw.circle(screen, green, [560, 375], 10, 0)
    else:
        pygame.draw.circle(screen, black, [560, 375], 10, 0)
    if inhibit == True:
        pygame.draw.circle(screen, yellow, [560, 375], 10, 0)

    screen.blit(setP_lbl,(525, 180))
    screen.blit(SetAt_lbl, (525,145))
    screen.blit(IP_label,(10, 10))
    screen.blit(cityLbl, (15, 365))
    screen.blit(status_lbl, (480, 365))
    screen.blit(outside, (50, 145))
    screen.blit(outsideT_lbl, (50, 180))
    screen.blit(outsideH, (60, 235))
    screen.blit(degree, (110, 170))
    screen.blit(degree, (580, 170))
    screen.blit(insideT, (220, 125))
    screen.blit(deg_symbol, (420, 110))
    screen.blit(localH_lbl, (260, 235))
    screen.blit(inside, (290, 110))
    screen.blit(time_label, (495, 10))
    screen.blit(x_lbl, (613, 11))
    pygame.draw.line(screen, white,(550,90),(560,80)) #arrows
    pygame.draw.line(screen, white,(560,80),(570,90))
    pygame.draw.line(screen, white,(550,300),(560,310))
    pygame.draw.line(screen, white,(560,310),(570,300))

    time.sleep(.1)

    pygame.display.flip()

while True:
    # get the weather every 110 sec
    #detect inhibit time
    update_weather() # update indoor and outdoor
    sunRise = time.localtime(sunrise) # convert from unix time  
    sunRISE = time.strftime('%H:%M', sunRise)

    for y in range(5): # read DHT every 8 sec
        localH, localT = Adafruit_DHT.read_retry(sensor, pin)
       # localT = (int(localT)*1.8+32) #===== for  Deg F only
        localT = (int(localT)* 1.0)  # For Deg C only
        localH = (int(localH))

## inhibit will stop the fan from working at sunrise when the temperature
## begins to rise and continue at 9AM
        if current_time > sunRISE and current_time < "09:00:00": #inhibit between these hours
#            print("sunrise = " + sunRISE)
#            print("time now = " + current_time)
            inhibit = True
        else:
            inhibit = False
#	    print ("sunrise = " + sunRISE)
#	    print("time = " + current_time)

        for x in range(30): # scan mouse every 0.5 seconds
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = pygame.mouse.get_pos()
                    print "screen pressed" 
                    print click_pos 
                    on_click()
            #ensure there is always a safe way to end the 
            #program if the touch screen fails

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE: # ESC key will kill it
                        sys.exit()
            pygame.time.wait(100)
            refresh_screen()

pi.stop()
pygame.quit()
