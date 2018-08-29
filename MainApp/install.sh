ln -s /home/pi/Bixel/MainApp/bixel.service /etc/systemd/system/bixel.service
systemctl enable bixel.service
systemctl start bixel.service