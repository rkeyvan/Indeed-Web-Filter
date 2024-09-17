# Indeed Web Filter

A program to automatically open your browser and search Indeed.com, select filters, and hide certain job posts with specific keywords in the job title. Modify the .json file to your desired search values and filter keywords before running the .py file.


## How to Install Selenium for Linux (Ubuntu)

### Install Chrome
- wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
- sudo apt install ./google-chrome-stable_current_amd64.deb
- sudo apt install google-chrome-stable
- sudo apt –only-upgrade install google-chrome-stable


### Install Oracle Java 8 or OpenJDK
- sudo apt update
- sudo apt install openjdk-11-jdk -y

### Download ChromeDriver (must match Chrome browser version)
Reference: https://googlechromelabs.github.io/chrome-for-testing/#stable 
- wget https://storage.googleapis.com/chrome-for-testing-public/128.0.6613.119/linux64/chromedriver-linux64.zip

- unzip chromedriver_linux64.zip
- cd chromedriver-linux64/
- sudo cp chromedriver /usr/localbin/chromedriver
- chromedriver -v

- sudo chown root:root /usr/bin/chromedriver
- sudo chmod 755 /usr/bin/chromedriver

### Install Selenium Tools on Linux
- https://www.geeksforgeeks.org/how-to-install-selenium-tools-on-linux/
- sudo apt install python3-selenium
- sudo apt update
