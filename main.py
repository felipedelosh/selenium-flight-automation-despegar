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
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

# Kons
_MM = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
_CURRENT_DAY_HTML_MARK = "HOY"

# CONFIG
_LOGS = ""
_url = "https://www.despegar.com.co"
_origin = "Bogotá, Bogotá D.C., Colombia"
_destination = "Medellín, Antioquia, Colombia"


def write_logs():
    with open("bot_logs.log", "a", encoding="UTF-8") as log_file:
        log_file.write(_LOGS + "\n")


def extact_flight_information(_url, _one_way_flight, _origin, _destination):
    """
    Enter args and generate File: Pandas with flight information.
    """

    def verify_integrity_input_args(input_origin, input_destination):
        global _origin
        global _destination
        _integrity = [False, False, False, False]

        _integrity[0] = True if input_origin is not None and input_origin.get_attribute("value") != "" and input_origin.get_attribute("value") == _origin else False
        _integrity[1] = True if input_destination is not None and input_destination.get_attribute("value") != "" and input_destination.get_attribute("value") == _destination else False

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
            origin_input.send_keys(Keys.ARROW_DOWN)
            origin_input.send_keys(Keys.ENTER)
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
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")
        options.add_argument("--enable-javascript")

        browser = webdriver.Chrome(options=options) # Vr > 115 Not NEED WebDriver
        # VIEW Browser config
        _LOGS = _LOGS + f"{browser.execute_script("return navigator.userAgent;")}\n"
        _LOGS = _LOGS + f"EXECUTE JS: {browser.execute_script("return window.navigator.javaEnabled();")}\n"

        _LOGS = _LOGS + f"{_url}\n"
        browser.get(_url)
        #browser.maximize_window()

        wait = WebDriverWait(browser, 8)
        action = ActionChains(browser) # Clicks like a human

        # GO TO Flights
        btn_go_flights = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/nav/div[2]/div/div[3]/ul/li[2]/a/div/div')))
        action.move_to_element(btn_go_flights).pause(1).click().perform()
        time.sleep(3)

        if _one_way_flight:
            btn_one_way = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="oneWay"]/span/button')))
            time.sleep(random.uniform(0.1, 0.4))
            action.move_to_element(btn_one_way).pause(1).click().perform()
        else:
            btn_round_trip_flight = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="oneWay"]/span/button')))
            time.sleep(random.uniform(0.2, 0.5))
            action.move_to_element(btn_round_trip_flight).pause(1).click().perform()

        try:
            btn_ok_cookies = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="lgpd-banner"]/div/div')))
            time.sleep(random.uniform(0.4, 0.7))
            action.move_to_element(btn_ok_cookies).pause(1).click().perform()
        except:
            _LOGS = _LOGS + "Error PRESS OK COOKIES.\n"

        # try:
        #     btn_close_google_sign_in = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/div/div[1]/div[2]/svg')))
        #     btn_close_google_sign_in.click()
        # except:
        #     _LOGS = _LOGS + "Error GOOGLE Sign in.\n"

        try:
            btn_no_benefit = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tooltip-not-logged-incentive"]/span/div[3]/div[3]/em')))
            time.sleep(random.uniform(0.3, 0.5))
            action.move_to_element(btn_no_benefit).pause(1).click().perform()
        except:
            _LOGS = _LOGS + "Error NO BENEFIT.\n"
        
        origin_input = fill_details_origin(_origin)
        destination_input = fill_details_destination(_destination)

        # TIME
        try:
            btn_scheluder_A = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dates-input1"]/div/div/input')))
            action.move_to_element(btn_scheluder_A).pause(1).click().perform()

            global _CURRENT_DAY_HTML_MARK
            btn_date_today = None
            # Extract information of current date
            _current_YYYY = None
            _current_MM = None
            _current_DD = None
            # Get despegar scheluded
            calendar_container = browser.find_element(By.XPATH, '//*[@id="component-modals"]/div[1]')

            dates = calendar_container.find_elements(By.XPATH, './/div[contains(@class, "sbox5-monthgrid-datenumber")]')
            for itter_date in dates:
                try:
                    txt = itter_date.text

                    if _CURRENT_DAY_HTML_MARK == txt:
                        btn_date_today = itter_date
                        # DD
                        day_container = itter_date.find_element(By.XPATH, "..")
                        day_container = day_container.text
                        # Save day
                        _current_DD = str(day_container).split("\n")[0]

                        # MM & YYYY
                        month_container = calendar_container.find_element(By.XPATH, f".//div[contains(@class, 'sbox5-monthgrid') and .//div[text()='{_current_DD}']]")
                        _current_YYYY_MM = month_container.get_attribute("data-month")
                        _current_YYYY_MM = str(_current_YYYY_MM).split("-")
                        # Save YYYY & MM
                        _current_YYYY = _current_YYYY_MM[0]
                        _current_MM = _current_YYYY_MM[1]
                        break

                except:
                    _LOGS = _LOGS + "ERROR FATAL Selecting DATE Flight.\n"


            _LOGS = _LOGS + f"SERVER DATE: {_current_DD}/{_current_MM}/{_current_YYYY}.\n"

            if btn_date_today:
                btn_date_today.click()

        except:
            pass
        
        # Search Flight information
        try:
            # Refill information
            while True:
                _integrity = verify_integrity_input_args(origin_input, destination_input)
                # print(verify_integrity_input_args(origin_input, destination_input))

                if _integrity[0] and _integrity[1]:  # Verifica que ambos sean True
                    break
                else:
                    if not _integrity[0]:
                        _LOGS = _LOGS + "Retry FILL orgin\n"
                        time.sleep(random.uniform(1, 3))
                        origin_input = fill_details_origin(_origin)

                    if not _integrity[1]:
                        _LOGS = _LOGS + "Retry FILL Destination\n"
                        time.sleep(random.uniform(1, 3))
                        destination_input = fill_details_destination(_destination)

            btn_search_flight = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchbox-v2"]/div/div/div/div/div/div[3]/div[3]/button/em')))
            browser.execute_script("arguments[0].click();", btn_search_flight)

            # SAVE FINAL DATA USING URL
            WebDriverWait(browser, 10).until(lambda driver: "results" in driver.current_url)
            rich_info_url = browser.current_url
            _LOGS = _LOGS + rich_info_url + "\n"
            # No need Browser continue with beufifullsoup
            _LOGS = _LOGS + "bs4\n"

            driver = webdriver.Chrome()
            driver.get(rich_info_url)
            time.sleep(5)
            html = driver.page_source

            with open("data.html", "w") as f:
                f.write(html)

            driver.quit()

        except:
            _LOGS = _LOGS + "ERROR TO TRY PRESS BUTTON SEARCH!!!!\n"

        time.sleep(10)
        # END TRY
    except:
        print("FATAL ERROR!")
    finally:
        _LOGS = _LOGS + "DAS ENDE.\n"
        browser.quit()

    write_logs()


extact_flight_information(_url, True, _origin, _destination)
