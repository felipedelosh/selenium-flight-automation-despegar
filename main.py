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
_current_day_mark = "HOY"


def write_logs():
    with open("bot_logs.log", "a", encoding="UTF-8") as log_file:
        log_file.write(_LOGS + "\n")


def extact_flight_information(_url, _one_way_flight, _origin, _destination):
    """
    Enter args and generate File: Pandas with flight information.
    """

    def verify_integrity_input_args(input_origin, input_destination):
        _integrity = [False, False, False, False]

        print(input_origin.get_attribute("value"))
        print(input_destination.get_attribute("value"))
        print("===========================================")

        _integrity[0] = True if input_origin is not None and input_origin.get_attribute("value") != "" else False
        _integrity[1] = True if input_destination is not None and input_destination.get_attribute("value") != "" else False

        return _integrity

    def fill_details_origin(_origin):
        global _LOGS
        try:
            origin_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchbox-v2"]/div/div/div/div/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div/div/input')))
            origin_input.send_keys(Keys.CONTROL + "a")
            #origen_input.send_keys(Keys.DELETE)
            for i in _origin:
                origin_input.send_keys(i)
                time.sleep(random.uniform(0.05, 0.2))


            time.sleep(1)
            current_value = origin_input.get_attribute("value")
            _LOGS = _LOGS + f"Origin: {current_value}\n"
        except:
            _LOGS = _LOGS + "ERROR Selecting Flight ORIGIN.\n"

        return origin_input


    def fill_details_destination(_destination):
        global _LOGS
        try:
            destination_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchbox-v2"]/div/div/div/div/div/div[3]/div[1]/div[1]/div[1]/div/div[2]/div/div/input')))
            destination_input.click()
            for i in _destination:
                destination_input.send_keys(i)
                time.sleep(random.uniform(0.05, 0.2))
            destination_input.send_keys(Keys.TAB)

            time.sleep(1)
            current_value = destination_input.get_attribute("value")
            _LOGS = _LOGS + f"Destination: {current_value}\n"
        except:
            _LOGS = _LOGS + "ERROR Selecting Flight DESTINATION.\n"


        return destination_input

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
        
        origin_input = fill_details_origin(_origin)
        destination_input = fill_details_destination(_destination)

        # TIME
        try:
            btn_scheluder_A = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dates-input1"]/div/div/input')))
            btn_scheluder_A.click()

            global _current_day_mark
            btn_date_today = None
            # Extract information of current date
            _current_YYYY = None
            _current_MM = None
            _current_DD = None
            # Get despegar scheluded
            calendar_container = browser.find_element(By.XPATH, '//*[@id="component-modals"]/div[1]')

            dates = calendar_container.find_elements(By.XPATH, './/div[contains(@class, "sbox5-monthgrid-datenumber")]')
            for index, itter_date in enumerate(dates):
                try:
                    txt = itter_date.text

                    if _current_day_mark == txt:
                        btn_date_today = itter_date
                        text_date_DD_today = dates[index - 1]
                        _current_DD = text_date_DD_today.text

                        break

                except:
                    _LOGS = _LOGS + "ERROR FATAL Selecting DATE Flight.\n"


            _LOGS = _LOGS + f"SERVER DATE: {_current_DD}/{"MM"}/{"YYYY"}.\n"

            if btn_date_today:
                btn_date_today.click()

        except:
            pass
        
        # Search Flight information
        # try:
        #     while True:
        #         _integrity = verify_integrity_input_args(origin_input, destination_input)
        #         print(verify_integrity_input_args(origin_input, destination_input))

        #         if _integrity[0] and _integrity[1]:  # Verifica que ambos sean True
        #             break
        #         else:
        #             if not _integrity[0]:
        #                 _LOGS = _LOGS + "Retry FILL orgin\n"
        #                 time.sleep(random.uniform(1, 3))
        #                 origin_input = fill_details_origin(_origin)

        #             if not _integrity[1]:
        #                 _LOGS = _LOGS + "Retry FILL Destination\n"
        #                 time.sleep(random.uniform(1, 3))
        #                 destination_input = fill_details_destination(_destination)

        #     btn_search_flight = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchbox-v2"]/div/div/div/div/div/div[3]/div[3]/button/em')))
        #     browser.execute_script("arguments[0].click();", btn_search_flight)

        #     # Save current data
        #     html = browser.page_source
        #     with open("temp.html", "w") as f:
        #         f.write(html)

        # except:
        #     _LOGS = _LOGS + "ERROR TO TRY PRESS BUTTON SEARCH!!!!\n"

        time.sleep(50)
        # END TRY
    except:
        print("FATAL ERROR!")
    finally:
        _LOGS = _LOGS + "DAS ENDE.\n"
        browser.quit()

    write_logs()


extact_flight_information(_url, True, _origin, _destination)
