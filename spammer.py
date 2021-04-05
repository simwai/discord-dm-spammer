from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import settings
import platform

def start_spam():

    # Checks if on Mac or Windows
    print("Opening Chrome")
    if platform.system() == "Windows":
        driver = webdriver.Chrome('chromedriver.exe')
    else:
        driver = webdriver.Chrome()

    # Loggin into selected platform
    print("Starting Log in....")
    # Opens Discord
    driver.get('https://discordapp.com/login')
    sleep(5)
    # Login
    driver.find_element_by_xpath('//*[@name="email"]').send_keys(settings.username_email)
    driver.find_element_by_xpath('//*[@name="password"]').send_keys(settings.password)
    driver.find_element_by_xpath('//*[@type="submit"]').click()

    # Waits 8 seconds to finish loading page
    print("Waiting for a few seconds...")
    sleep(8)

    while True:
      try:
        driver.find_element_by_id("checkbox")
        break
      except NoSuchElementException:
        print("Captcha control detected. Solve it manually. Check for captcha solve state in some second.")
        sleep(10)

    for friend_name in settings.friend_names:
      # Finds user in DM list
      driver.find_element_by_xpath("//*[contains(text(), '" + friend_name + "')]").click()

      # Starts message sending
      print("Starting messages...")
      with open(settings.script, "r") as f:
          for line in f.readlines():
              for i in range(settings.iterations):
                  for word in line.split():
                      print("Sending: " + word)
                      # Types words and submits
                      actions = ActionChains(driver)
                      actions.send_keys(word, Keys.ENTER)
                      actions.perform()
                      sleep(float(settings.delay))
