#!/bin/sh
set -x

# DNS Setting
echo 'DNS=192.168.0.1 8.8.8.8' | sudo tee -a /etc/systemd/resolved.conf

# Network addvance setting
sudo rfkill unblock all
sudo dhclient wlan0

sudo apt update
sudo apt upgrade -y
sudo apt install expect -y

# Change Raspi Password
CURRENT_PASSWORD="raspberry"
NEW_PASSWORD="wxyz789?*"

sleep 1m
sudo pwconv
expect -c "
  set timeout ${TIMEOUT}
  spawn passwd pi
  expect \"password:\"
  send \"${CURRENT_PASSWORD}\n\"
  expect \"New password:\"
  send \"${NEW_PASSWORD}\n\"
  expect \"Retype new password:\"
  send \"${NEW_PASSWORD}\n\"
  interact
"

# Enable ssh
sudo mv /etc/wpa_supplicant/wpa_supplicant.conf /boot/wpa_supplicant.conf
sudo touch /boot/ssh
sudo systemd enable ssh

# Enable Greengrass Install Service
# sudo systemctl enable setup_greengrass_device.service
sudo systemctl enable setup_python.service

# Disable Setup Device Service
sudo systemctl disable setup_device.service

# daemon reload
sudo systemctl daemon-reload

# reboot
sudo reboot
