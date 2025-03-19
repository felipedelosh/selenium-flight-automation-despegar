"""
Netactica
2025

Extract flight information of https://www.despegar.com.co/
"""
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# CONFIG
_LOGS = ""
_url = "https://www.despegar.com.co/vuelos/"
_origin = "Manizales, Caldas, Colombia"
_destination = "Armenia, Quindío, Colombia"


def extact_flight_information(_url, _one_way_flight, _origin, _destination):

    def verify_integrity_input_args(input_origin, input_destination):
        _integrity = [False, False, False, False]

        print(input_origin.get_attribute("value"))
        print(input_destination.get_attribute("value"))
        print("===========================================")

        _integrity[0] = True if input_origin is not None and input_origin.get_attribute("value") != "" else False
        _integrity[1] = True if input_destination is not None and input_destination.get_attribute("value") != "" else False

        return _integrity

    try:
        global _LOGS
        _LOGS = f"{date.today()}\n"


        # HTML elements
        origin_input = None
        destination_input = None


        # Configure BOT like a Human
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        browser = webdriver.Chrome(options=options) # Vr > 115 Not NEED WebDriver

        _LOGS = _LOGS + f"{_url}\n"
        browser.get(_url)
        #browser.maximize_window()

        wait = WebDriverWait(browser, 5)

        if _one_way_flight:
            btn_one_way = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="oneWay"]/span/button')))
            btn_one_way.click()
        else:
            btn_round_trip_flight = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="oneWay"]/span/button')))
            btn_round_trip_flight.click()

        try:
            btn_ok_cookies = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="lgpd-banner"]/div/div')))
            btn_ok_cookies.click()
        except:
            _LOGS = _LOGS + "Error PRESS OK COOKIES.\n"

        # try:
        #     btn_close_google_sign_in = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/div/div[1]/div[2]/svg')))
        #     btn_close_google_sign_in.click()
        # except:
        #     _LOGS = _LOGS + "Error GOOGLE Sign in.\n"

        try:
            btn_no_benefit = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tooltip-not-logged-incentive"]/span/div[3]/div[3]/em')))
            btn_no_benefit.click()
        except:
            _LOGS = _LOGS + "Error NO BENEFIT.\n"

        # ORIGIN
        try:
            origin_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchbox-v2"]/div/div/div/div/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div/div/input')))
            origin_input.send_keys(Keys.CONTROL + "a")
            #origen_input.send_keys(Keys.DELETE)
            for i in _origin:
                origin_input.send_keys(i)
                time.sleep(0.1)


            time.sleep(1)
            current_value = origin_input.get_attribute("value")
            _LOGS = _LOGS + f"Origin: {current_value}\n"
        except:
            _LOGS = _LOGS + "ERROR Selecting Flight ORIGIN.\n"

        # DESTINATION
        try:
            destination_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchbox-v2"]/div/div/div/div/div/div[3]/div[1]/div[1]/div[1]/div/div[2]/div/div/input')))
            destination_input.click()
            for i in _destination:
                destination_input.send_keys(i)
                time.sleep(0.1)
            destination_input.send_keys(Keys.TAB)

            time.sleep(1)
            current_value = destination_input.get_attribute("value")
            _LOGS = _LOGS + f"Destination: {current_value}\n"
        except:
            _LOGS = _LOGS + "ERROR Selecting Flight DESTINATION.\n"

        print(verify_integrity_input_args(origin_input, destination_input))

        # TIME
        try:
            btn_scheluder_A = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dates-input1"]/div/div/input')))
            btn_scheluder_A.click()

            # //*[@id="component-modals"]/div[1]
            # Leer todo el datepiker y situarse en la fecha de hoy.
            _schelude_date = "Crazy"
        except:
            pass

        try:
            pass
            #btn_search_flight = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchbox-v2"]/div/div/div/div/div/div[3]/div[3]/button/em')))
            #browser.execute_script("arguments[0].click();", btn_search_flight)
        except:
            _LOGS = _LOGS + "ERROR TO TRY PRESS BUTTON\n"


        time.sleep(10)

    finally:
        _LOGS = _LOGS + "ERROR FATAL\n"
        browser.quit()


extact_flight_information(_url, True, _origin, _destination)

# SAVE LOG FILE
with open("log.log", "a", encoding="UTF-8") as f:
    f.write(_LOGS)
