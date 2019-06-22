#!/usr/bin/python
# smart fan
# Rev1
import sys, pygame
from pygame.locals import *
import time
import datetime
import subprocess
import Adafruit_DHT
import pywapi
import string
import socket
import os

pygame.init()

disp_units = "imperial"
#disp_units = "metric"
#zip_code = 'USIN0286'
zip_code = "60617"
## dh100 smart plug IP
hs100IP = '192.168.43.82'
HS100 = False
plug_status = '??'
degSymF = unichr(0x2109)         # Unicode for DegreeF
degSym = unichr(0x00B0)          #unicode for degree
pin = '4'
sensor = Adafruit_DHT.DHT22

#set size of the screen
size = width, height = 650, 410  #to fit in a 720x480 screen

#screen = pygame.display.set_mode(size) #,pygame.FULLSCREEN)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

#define colors
cyan = 50, 255, 255
blue = 130, 75, 200
black = 0, 0, 0
white = 255, 235, 235
lblue = 75, 140, 200
green = 0, 255, 0
silver = 192, 192, 192

#other
wLastUpdate = ''
set_point = 70
temp = 0
#raspberry IP
IPAddr = socket.gethostbyname('raspberrypi.local')

localH = 0
localT = 0
location = '??'

#define function that checks for mouse location
def on_click():
    print('clicked')
    #check to see if exit has been pressed
    if 599 < click_pos[0] < 639 and 1 < click_pos[1] < 41:
	print "-- exit" 
	button(0)
	#now check to see if play was pressed
    if 540 <= click_pos[0] <= 580 and 70 <= click_pos[1] <=110:
        print "-- up"
        button(1)
	#now check to see if mp3 was pressed
    if 540 <= click_pos[0] <= 580 and 280 <= click_pos[1] <=320:
        print "-- down"
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
        subprocess.Popen(["sudo", "./hs100.sh", "-i", hs100IP, "off"]) 
	label=font.render("Turning HS100 OFF! ", 1, (white))
        screen.blit(label,(40,150))
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
#    global cpu
    global temp 
    global humid
    global HS100
    global location
#    cpu = os.popen("vcgencmd measure_temp").readline()
#    cpu = cpu[-7:] #remove characters not needed
#    cpu = cpu[:-1]

    # Use Weather.com for source data.
    cc = 'current_conditions'
    f = 'forecasts'
    w = { cc:{ f:1 }}  # Init to something.
    wLastUpdate = ''

    # read the weather 
    try:
	w = pywapi.get_weather_from_weather_com( zip_code, units=disp_units )
#        w = pywapi.get_weather_from_yahoo(zip_code, units=disp_units)

    except:
	print "Error getting update from weather.com"
	errCount += 1
	return

    try:
	if ( w[cc]['last_updated'] != wLastUpdate ):
	    wLastUpdate = w[cc]['last_updated']
	    print "New Weather Update: " + wLastUpdate
	    temp = string.lower( w[cc]['temperature'] )
	    humid = string.upper( w[cc]['humidity'] )
            location = string.upper( w[cc]["station"])
            print(location)

	if ( w[f][0]['high'] == 'N/A' ):
	    temps[0][0] = '--'
	else:
	    errCount = 0

    except KeyError:
	print "KeyError -> Weather Error"
	if errCount >= 15:
	    temp = '??'
	    wLastUpdate = ''
	return False
    except ValueError:
	print "ValueError -> Weather Error"

       # check for temperature and control the smart plug 
    if float(localT) >= set_point and float(temp) < float(localT) and HS100 == False:
        subprocess.Popen(["sudo", "./hs100.sh", "-i", hs100IP, "on"]) 

        print('Plug is ON')
        HS100 = True

    if float(temp) > float(localT) and HS100 == True:
        subprocess.Popen(["sudo", "./hs100.sh", "-i", hs100IP, "off"]) 

        HS100 = False
        print(HS100)
#    else:
        print (plug_status)
    if float(localT) < set_point and HS100 == True:
        subprocess.Popen(["sudo", "./hs100.sh", "-i", hs100IP, "off"]) 
        print('off')
        HS100 = False
    print ('end of checking')
#============================================

def refresh_screen():
#set up the fixed items on the menu
    global temp
    global localT
    
    current_time = datetime.datetime.now().strftime('%I:%M:%S')
    time_font=pygame.font.Font(None,36)
    time_label = time_font.render(current_time, 1, (silver)) 
#    IP_label = time_font.render(IPAddr, 1, (silver))
    IP_label = time_font.render(hs100IP, 1, (silver))

    sfont = pygame.font.SysFont('sans', 20, bold=0)
    d_font = pygame.font.SysFont('sans', 30, bold=1)
    mfont = pygame.font.SysFont( 'sans', 50, bold=1)
    lfont = pygame.font.SysFont( 'sans', 110, bold=0)
    fontL = pygame.font.Font(None,32)
 #   cpu_font = pygame.font.Font(None,32)

 #   cpu_label = cpu_font.render('Cpu ' + cpu, 1, (silver))
    skin = pygame.image.load("720skin.jpg")
    status_lbl = sfont.render('HS100', 1, (white))
    setP = mfont.render( str(set_point), 1, (cyan))

    screen.blit(skin,(0,0))

	# Outside Temp
    outsideT = mfont.render( temp, True, cyan )
    outside = sfont.render('Outside', True, white)
    outsideH = sfont.render(humid + '%', True, silver)
	# Show degree F symbol
    degree = d_font.render( degSym, True, cyan )

	# Local Temp
    insideT = lfont.render(str(localT), True, cyan )
    localHfnt = sfont.render('Humidity ' + str(localH) +'%', True, silver)
    SetAt = sfont.render('Set to', True, white)
    inside = sfont.render('Inside', True, white)
    locLbl = sfont.render(location, True, white) # location

	# Show degree F symbol 
    degreeF = d_font.render( degSymF, True, cyan )

	#draw the main elements on the screen 

    pygame.draw.rect(screen, blue, (540, 70, 40, 40),0)
    pygame.draw.rect(screen, blue, (540, 280, 40, 40),0)
    pygame.draw.rect(screen, lblue, (599, 1, 40, 40), 0)
    if HS100 == True:
        pygame.draw.circle(screen, green, [560, 375], 10, 0)
    else:
        pygame.draw.circle(screen, black, [560, 375], 10, 0)
#    screen.blit(cpu_label,(15, 365)) #cputemp
    screen.blit(setP,(525, 180))
    screen.blit(SetAt, (525,145))
    screen.blit(IP_label,(10, 10))
    screen.blit(locLbl, (15, 365))
    screen.blit(status_lbl, (480, 365))
    screen.blit(outside, (50, 145))
    screen.blit(outsideT, (50, 180) )
    screen.blit(outsideH, (60, 235))
    screen.blit(degree, (110, 170))
    screen.blit(degree, (580, 170))
    screen.blit( insideT, (220, 125) )
    screen.blit( degreeF, (420, 110) )
    screen.blit(localHfnt, (260, 235))
    screen.blit(inside, (290, 110))
    screen.blit(time_label, (495, 10))

    time.sleep(.1)

    pygame.display.flip()

while True:

    update_weather()
    for y in range(5):
#        print('first loop')
        localH, localT = Adafruit_DHT.read_retry(sensor, pin)
        localT = (int(localT)*1.8+32)
        localH = (int(localH))

        for x in range(8): # update every 30 seconds
#            print('second loop')
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = pygame.mouse.get_pos()
                    print "screen pressed" #for debugging purposes
                    print click_pos #for checking
                    on_click()
            #ensure there is always a safe way to end the 
            #program if the touch screen fails

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE: # ESC key will kill it
                        sys.exit()
            pygame.time.wait(300)
            refresh_screen()
    
pi.stop()
pygame.quit()
