# @Author: Colton Fridgen
# @Date: 2021-09-30

# import libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import API_KEY, USER_KEY
import time, http.client, urllib

# gets user info from user
def get_user_info():

    user_info = [] # list to store user info
    print("Welcome to the course drop notifier!")
    username = input("Enter your Mun Login ID: ")
    password = input("Enter your Mun Login Password: ")
    term = input("Enter appropriate term: (ex: 2024-2025 Fall): ")
    subject = input("Enter course subject: (ex: Computer Science): ")
    course_number = input("Enter course number: (ex: 3200): ")
    course_position = int(input("Enter course position on table as seen on Mun Self Serve: (ex: 1, 2, 3, 4): "))
    course_position += 4 # needed to ensure Mun slef serve tables are read correctly
    course_position = str(course_position)

    # checks if course is offered at more than one campus and assigns a value to course_offering
    offerings = input("Press Y if the course is offered at more than one campus (ie: online and st. Johns). press N if not: ")
    if offerings == "Y" or offerings == "y":
        course_offering = input("Enter which campus the course is offered (ex: online, st. johns): ")
    if course_offering == "st. Johns":
        course_offering == 1
    elif course_offering == "Grenfell":
        course_offering == 2
    elif course_offering == "online":
        course_offering == 3

    # adds all user info to list
    user_info.append(username)
    user_info.append(password)
    user_info.append(term)
    user_info.append(subject)
    user_info.append(course_number)
    user_info.append(course_position)
    user_info.append(offerings)
    user_info.append(course_offering)

    return user_info

# main function
def main():

    INTERVAL = 1800 # sets time between checking course availability
    user_info = get_user_info()

    while True:

        # sets up chrome driver
        DRIVER_PATH = "/usr/local/bin/chromedriver"
        service = Service(DRIVER_PATH)
        chrome_options = Options()
        chrome_options.headless = True
        chrome_options.add_argument("--window-size=1920,1200")

        # opens chrome and logs into Mun self serve
        driver = webdriver.Chrome(service = service, options = chrome_options)
        driver.get("https://my.mun.ca")
        time.sleep(0.5) 

        username_feild = driver.find_element(By.ID, "username")
        username_feild.send_keys(user_info[0])
        time.sleep(0.5)

        password_feild = driver.find_element(By.ID, "password")
        password_feild.send_keys(user_info[1])
        time.sleep(0.5)

        login_button = driver.find_element(By.NAME, "submitBtn")
        login_button.click()
        time.sleep(0.5)

        # navigates to course offerings
        student_tab = driver.find_element(By.CSS_SELECTOR, "a[href='https://my.mun.ca/student']")
        student_tab.click()
        time.sleep(0.5)

        self_service = driver.find_element(By.PARTIAL_LINK_TEXT, "Self-Service")
        self_service.click()
        time.sleep(0.5)

        student_main_menu = driver.find_element(By.PARTIAL_LINK_TEXT, "Student Main Menu")
        student_main_menu.click()
        time.sleep(0.5)

        registration = driver.find_element(By.LINK_TEXT, "Registration")
        registration.click()
        time.sleep(0.5)

        course_offerings = driver.find_element(By.LINK_TEXT, "Look up Course Offerings")
        course_offerings.click()
        time.sleep(0.5)

        # selects course and checks if seats are available
        dropdown = driver.find_element(By.NAME, "p_term")
        select = Select(dropdown)
        select.select_by_visible_text(user_info[2])
        time.sleep(0.5)

        submit = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Submit']")
        submit.click()
        time.sleep(0.5)

        course_list = driver.find_element(By.ID, "subj_id")
        desired_option_text = user_info[3]
        options = course_list.find_elements(By.TAG_NAME, "option")
        for option in options:
            if option.text == desired_option_text:
                option.click()
                break
        time.sleep(3)

        search_button = driver.find_element(By.NAME, "SUB_BTN")
        search_button.click()
        time.sleep(3)

        course_row = driver.find_element(By.XPATH, f"//td[contains(text(), \"{user_info[4]}\")]/..")
        form = course_row.find_element(By.TAG_NAME, "form")
        submit_button = form.find_element(By.NAME, "SUB_BTN")
        submit_button.click()
        time.sleep(3)

        # finds the corect information regarding remaining seats of the course
        if user_info[6] == "Y" or user_info[6] == "y":
            remaining_seats = driver.find_element(By.XPATH, f"/html/body/div[4]/form/table/tbody/tr[{user_info[5]}]/td[14]")
        else:
            remaining_seats = driver.find_element(By.XPATH, f"/html/body/div[4]/form/table[{user_info[7]}]/tbody/tr[{user_info[5]}]/td[11]")

        # sends push notification if seats are available
        if int(remaining_seats.text) > 0:
            conn = http.client.HTTPSConnection("api.pushover.net:443")
            conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
            "token": API_KEY,
            "user": USER_KEY,
            "message": "!!! Seats Available Register Now !!!",
        }), { "Content-type": "application/x-www-form-urlencoded" })
            conn.getresponse()
        else:
            conn = http.client.HTTPSConnection("api.pushover.net:443")
            conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
            "token": API_KEY,
            "user": USER_KEY,
            "message": "no seats available",
        }), { "Content-type": "application/x-www-form-urlencoded" })
            conn.getresponse()

        time.sleep(INTERVAL) # waits for interval before checking again
        driver.quit() # closes chrome

main()