#!/bin/bash
#
#create shortcut


# create shortcut on desktop
 
touch fan.desktop
cat <<EOF > fan.desktop

#!/usr/bin/bash

[Desktop Entry]
Name=FAN
Type=Application
Exec=lxterminal -t "SMART FAN" --working-directory=/home/pi/smart-window-fan/ -e ./fan.sh
Icon=/home/pi/smart-window-fan/icon.png
Comment=test
Terminal=true

EOF

sudo chmod 755 fan.desktop
sudo mv fan.desktop /home/pi/Desktop
