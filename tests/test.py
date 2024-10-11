from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker
import time
import random

factory = Faker()

options = Options()
# options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

BASE = 'http://127.0.0.1:5000/'

# Load home page
driver.get(f'{BASE}')
print(driver.title)

time.sleep(5)

#Test Login Page
print("Testing Login page")
driver.get(f"{BASE}login")

time.sleep(3)
email_input = driver.find_element(By.ID, "email")
email_input.send_keys('jowsey@gmail.com')
time.sleep(3)

password_input = driver.find_element(By.ID, 'password')
password_input.send_keys('testpassword')
time.sleep(3)

driver.find_element(By.XPATH, '//button[@type="submit"]').click()

time.sleep(10)

# Test logout
driver.get(f'{BASE}logout')
time.sleep(4)
print('User logged out...')

# Test Registration
driver.get(f"{BASE}register")
time.sleep(5)

driver.find_element(By.ID, 'fullName').send_keys(factory.name())
time.sleep(3)
driver.find_element(By.ID, 'genderMale').click()
time.sleep(2)
driver.find_element(By.ID, 'email').send_keys(factory.email())
time.sleep(3)
driver.find_element(By.ID, 'password').send_keys('testpassword')
time.sleep(3)
password_confirmation = driver.find_element(By.ID, 'passwordConfirm')
password_confirmation.send_keys('testpasswordwrong')
time.sleep(3)
programs = Select(driver.find_element(By.ID, 'programs'))
# print(random.choice(programs.options).text)
programs.select_by_visible_text(random.choice(programs.options).text)
time.sleep(5)

button = driver.find_element(By.XPATH, '//button[@type="submit"]')
button.click()

time.sleep(4)
alert = driver.switch_to.alert
alert.accept()

time.sleep(2)
password_confirmation.clear()
time.sleep(2)
password_confirmation.send_keys('testpassword')
time.sleep(3)
button.click()

# Test update module
time.sleep(6)

modules = Select(driver.find_element(By.ID, 'changeModule'))
modules.select_by_visible_text(random.choice(modules.options).text)
time.sleep(2)
driver.find_element(By.XPATH, '//button[@type="submit"]').click()
time.sleep(6)

modules = Select(driver.find_element(By.ID, 'changeModule'))
modules.select_by_visible_text(random.choice(modules.options).text)
time.sleep(2)
driver.find_element(By.XPATH, '//button[@type="submit"]').click()
time.sleep(4)

time.sleep(10)
print('Testing completed....')
driver.close()

