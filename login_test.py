import pyperclip
import pyautogui
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from google.cloud import bigquery
from google.oauth2 import service_account
from apscheduler.schedulers.background import BackgroundScheduler
import time
import datetime
import json
import os


def get_driver():
    options = ChromeOptions()
    # options.add_argument('--headless=new')
    # options.add_argument("disable-gpu")
    options.add_argument('window-size=1920x1080')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    return driver

def naver_login():
    screen = get_driver()
    # screen.maximize_window()
    screen.implicitly_wait(5)

    expire_date = datetime.datetime(2024, 12, 12, 3, 3, 3)
    time_stamp = expire_date.timestamp()
    SCROLL_PAUSE_SEC = 1
    delay = 3

    path = "https://auth.glad.naver.com/login?&destination=https%3A%2F%2Fgfa.naver.com%2F"
    screen.get(path)
    screen.implicitly_wait(3)
    time.sleep(3)

    # 로그인 버튼 클릭 - page 이동
    # elem = screen.find_element_by_class_name('MyView - module__link_login___HpHMW')
    elem = screen.find_element(By.LINK_TEXT, "네이버로 로그인")
    elem.click()
    screen.implicitly_wait(5)
    time.sleep(3)

    user_id = ''
    user_pw = ''

    # id pw 입력
    # log_id = screen.find_element(By.ID, "id")
    log_id = screen.find_element(By.CSS_SELECTOR, "#id")
    log_id.click()
    pyperclip.copy(user_id)
    # pyperclip.copy(user_id).send_keys(Keys.CONTROL+'v')
    # log_id.send_keys(Keys.CONTROL, 'v')
    log_id.send_keys(Keys.COMMAND, 'v')
    # pyautogui.hotkey("ctrl", "v")
    # pyautogui.keyDown('command')
    # pyautogui.press('v')
    # pyautogui.keyUp('command')
    screen.implicitly_wait(5)
    time.sleep(3)

    # log_pid = screen.find_element(By.ID, "pw")
    log_pid = screen.find_element(By.CSS_SELECTOR, "#pw")
    log_pid.click()
    pyperclip.copy(user_pw)
    log_pid.send_keys(Keys.COMMAND, 'v')
    # log_pid.send_keys(Keys.CONTROL, 'v')
    # pyautogui.hotkey('ctrl', 'v')
    # pyautogui.keyDown('command')
    # pyautogui.press('v')
    # pyautogui.keyUp('command')
    screen.implicitly_wait(5)
    time.sleep(3)

    # 로그인 클릭
    log_ent = screen.find_element(By.ID, "log.login")
    log_ent.click()
    screen.implicitly_wait(5)
    time.sleep(3)

    last_height = screen.execute_script("return document.body.scrollHeight")
    print("last_height : " + str(last_height))
    screen.implicitly_wait(5)
    time.sleep(3)

    all_cookies1 = screen.get_cookies()
    cookies_dict = {}
    for cookie in all_cookies1:
        cookies_dict[cookie['name']] = cookie['value']
    print("cookies_dict1 ; ", cookies_dict)

    nid_ses = ""
    nid_aut = ""
    nid_jkl = ""
    glad_ses = ""
    for key in cookies_dict:
        print("cookies_dict[key] ; ", cookies_dict[key])
        if key == "GLAD_SES":
            glad_ses = cookies_dict[key]
        elif key == "NID_JKL":
            nid_jkl = cookies_dict[key]
        elif key == "NID_SES":
            nid_ses = cookies_dict[key]
        elif key == "NID_AUT":
            nid_aut = cookies_dict[key]

    # print("nid_ses ; ", nid_ses)
    # print("nid_aut ; ", nid_aut)
    # print("nid_jkl ; ", nid_jkl)
    # print("glad_ses ; ", glad_ses)
    screen.implicitly_wait(5)
    time.sleep(5)

    screen.close()
    screen.quit()

def backgroundScheduler():
    scheduler = BackgroundScheduler()
    scheduler.start()

    scheduler.add_job(naver_login, 'cron', hour="6", minute="40", id="test_1")
    scheduler.add_job(naver_login, 'cron', hour="18", minute="40", id="test_2")

if __name__ == '__main__':
    backgroundScheduler()

    count = 0

    while True:
        time.sleep(1)

