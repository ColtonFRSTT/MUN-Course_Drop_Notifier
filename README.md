# Course Drop Notifier
Course Drop Notifier is a python script using selenium chrome driver and pushover to notify you when a position becomes available for courses offered at Memorial University.

### How It Works
Course Drop Notifier uses a web crawler to log you into your Mun Login account and take control of the Mun self serve menus to notify you when a seat is available.

### Logging in
Course Drop Notifier asks for your Mun Login and Password. Keep in mind this is required for the code to work and no information is stored or sent anywhere other than the script itself.

# Getting Started
In order to use Course Drop Notifier you must have installed and set up:

1. Python 3.10 with selenium package
2. Chrome Web Driver
3. Pushover app and API keys

### Installing Python 3.10
- **Windows** Follow [this](https://www.digitalocean.com/community/tutorials/install-python-windows-10) digital ocean turorial
- **MacOS** Follow [this](https://www.dataquest.io/blog/installing-python-on-mac/) Dataquest tutorial
- **Linux** You can do it

### Installing Selenium Python Package
- Run the following command in your terminal
```
pip install selenium
```

### Installing Chrome WebDriver
- navigate to the Chrome WebDriver [downloads](https://developer.chrome.com/docs/chromedriver/downloads) page and install the webdriver that corresponds to your version of Chrome **it is very important both versions match**
- unzip and install the chromedriver in your path and update code on line 61 if needed

### Installing and seting up Pushover
- Install the Pushover app to your [iPhone](https://play.google.com/store/apps/details?id=net.superblock.pushover&hl=en) or [Android](https://apps.apple.com/us/app/pushover-notifications/id506088175) device via the App Store and Google Play Store

- You will then need to set your USER KEY equal to USER_KEY in configs.py
and your API KEY equal to API_KEY in configs.py. [here](https://www.youtube.com/watch?v=2RHqWr6QWHc) is how you can do that

# Running
Course Drop Notifier is set by default to check course availability every 30 minutes after it is ran. You can change this by changin the INTERVAL on line 55.

Enter your personal and course information into the fields provided and then go enjoy your life while Course Drop Notifier does its work
 



