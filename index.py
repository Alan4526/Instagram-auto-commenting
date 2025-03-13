
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
from time import sleep
import random
from selenium.webdriver.common.keys import Keys
import pyperclip
import pygetwindow as gw
from datetime import datetime
import pyautogui
from pywinauto import Application


from chatgptAPI import getComment

driver = ""
isPostSuccess = False

def update_status(msg):
    now_ = datetime.now()
    current_time = now_.strftime("%Y-%m-%d %H:%M:%S")
    print(str(current_time) + " - " + str(msg))


def activeChromeWindow(title):
    window = None
    try:
        window_title = title
        os_windows = gw.getAllTitles()
        for os_window in os_windows:
            if window_title in os_window:
                print(os_window)
                app = Application().connect(title=os_window)
                window = app.window(title=os_window)
                window.set_focus()
                sleep(0.5)
                window.bring_to_front()
                print(f"Focused window: {os_window}")
                return True
        print("No matching OS window found.")
        return False
    except Exception as e:
        print("Error focusing the latest driver window:", e)
    finally:
        if window:
            window_rect = window.rectangle()
            window_width = window_rect.right - window_rect.left
            window_height = window_rect.bottom - window_rect.top
            window_center_x = window_rect.left + window_width / 2
            window_center_y = window_rect.top + window_height / 2
            pyautogui.click(window_center_x, window_center_y)
    return False

# Set up Chrome options and WebDriver
update_status("Opening Chrome..")
options = Options()
options.add_argument("start-maximized")
options.add_argument("--log-level=3")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument(f"user-data-dir=" + os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromeProfile"))
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)  # Set up explicit wait

# Open Facebook login page
update_status("Navigating to base website..")
driver.get("https://www.instagram.com")

print('\n')
update_status("STEPS:")
update_status("1. Log in with your account")
update_status("2. Set the delay between posts via 'Config.txt' file.")
update_status("3. Once ready, press ENTER key to start posting.")

input("\nPress Enter!: ")
activeChromeWindow(driver.title)
update_status("Bot is running...")

# Load delay settings
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.txt")
with open(config_path, "r") as file:
    cont = file.readlines()
    min_delay = int(cont[0].replace("MIN_DELAY_IN_SECONDS=", "").strip())
    max_delay = int(cont[1].replace("MAX_DELAY_IN_SECONDS=", "").strip())

def get_random_int():
    randomTime = random.randint(min_delay, max_delay)
    update_status(f"delay for {randomTime}s")
    return randomTime

def find_and_paste(selector, text):
    try:
        driver.execute_script("arguments[0].focus();", selector)
        pyperclip.copy(text.replace("'", "").replace('"', ""))
        sleep(0.5)
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        return True
    except Exception as e:
        return False

# Load images and caption
while True:
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "article:not([data-commented])")))

        articles = driver.find_elements(By.CSS_SELECTOR, "article:not([data-commented])")
        for article in articles:
            driver.execute_script("arguments[0].setAttribute('data-commented', 'true');", article)
            
            textArea = article.find_element(By.TAG_NAME, "textarea")
            comment = getComment()
            find_and_paste(textArea, comment)

            sleep(2)

            button = article.find_element(By.XPATH, ".//textarea/following-sibling::div/div[@role='button']")
            button.click()

            update_status("left comment successfully!")
            sleep(get_random_int())
        
    except Exception as e:
        print("Something went wrong!!")
    finally:
        sleep(3) # 2 min

