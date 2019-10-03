#!/bin/bash

#Check for Python 3.x.x version
if [[ $(python3 --version | cut -c 8) -eq "3" || $(python --version | cut -c 8) -eq "3" ]]; then
	echo "Python 3.x is installed"
else
	echo "Python 3.x is not installed"
	exit 1
fi

#Install Python requirements
pip3 install -qr requirements.txt

#Check for Chrome/Chromium installation
if [[ $(chromium-browser --version &> /dev/null; echo $?) -eq "0" || $(google-chrome --version &> /dev/null; echo $?) -eq "0" ]]; then
	echo "Chrome/Chromium is installed"
else
	echo "Chrome/Chromium is not installed"
fi

#Chromedriver check
if [[ $(chromedriver -v &> /dev/null; echo $?) -eq 0 ]]; then
	echo "Chromedriver is installed"
else
	echo "Chromedriver is not installed, installing now"
	cd_ver=$(curl -SsL https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
	wget -nv -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/"$cd_ver"/chromedriver_linux64.zip
	unzip -q /tmp/chromedriver.zip -d /tmp/
	chmod a+x /tmp/chromedriver
	sudo mv /tmp/chromedriver /usr/bin/
fi
