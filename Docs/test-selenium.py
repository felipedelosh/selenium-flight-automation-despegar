import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import pandas as pd

# Configuración de Chrome para bloquear recursos externos
caps = DesiredCapabilities.CHROME
caps["goog:loggingPrefs"] = {"performance": "ALL"} 

service = Service()  # Puedes especificar la ruta del driver si es necesario
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")

# Iniciar el driver con capacidades modificadas
driver = webdriver.Chrome(service=service, options=options)

# Bloquear solicitudes externas con Chrome DevTools
driver.execute_cdp_cmd("Network.setBlockedURLs", {
    "urls": ["*.css", "*.js", "*.png", "*.jpg", "*.svg", "*.gif", "https://*", "http://*"]
})
driver.execute_cdp_cmd("Network.enable", {})

# Cargar el archivo HTML localmente
file_path = os.path.abspath("Docs/data.html")
driver.get(f"file:///{file_path}")

# Esperar a que el documento esté completamente cargado
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

# Buscar todos los clusters
clusters = driver.find_elements(By.CSS_SELECTOR, "cluster.COMMON")
print(f"Se encontraron {len(clusters)} elementos con la clase 'COMMON'.")

_output_data = []
if clusters:
    for itter_cluster in clusters:
        _airline = ""
        spans_airline = itter_cluster.find_elements(By.CSS_SELECTOR, "span[_ngcontent-gjg-c200]")
        for span in spans_airline:
            if str(span.text).strip() != "":
                _airline = span.text
                break


        _isDirect = []
        stop_span = itter_cluster.find_elements(By.CSS_SELECTOR, 'span[data-sfa-id="stops-text"]')
        for span in stop_span:
            if str(span.text).strip() != "" and span.text == "Directo":
                _isDirect.append(1)
            else:
                _isDirect.append(0)

        _date_arrival = ""
        date_spans = itter_cluster.find_elements(By.CSS_SELECTOR, 'span[data-sfa-id="route-date"]')
        for span in date_spans:
            _date_arrival = span.text


        _isHourOrigin = True
        _hours_origin = []
        _hours_destination = []
        spans_hour = itter_cluster.find_elements(By.CSS_SELECTOR, "span.hour")
        for span in spans_hour:
            if _isHourOrigin:
                _hours_origin.append(span.text)
            else:
                _hours_destination.append(span.text)

            _isHourOrigin = not _isHourOrigin

        span_price = itter_cluster.find_element(By.CSS_SELECTOR, "span.amount.price-amount")
        _price = span_price.text


        if len(_hours_origin) == len(_hours_destination):
            data = {}
            data["Airline"] = [_airline] * len(_hours_origin)

            if _isDirect:
                data["is_direct"] = _isDirect
            else:
                data["is_direct"] = [0] * len(_hours_origin)

            data["date_arrival"] = [_date_arrival] * len(_hours_origin)
            data["Boarding_time"] = _hours_origin
            data["Arrival_time"] = _hours_destination
            data["Price"] = [_price] * len(_hours_origin)

            _output_data.append(data)

expanded_data = []
for entry in _output_data:
    # Obtener la cantidad de vuelos en la entrada
    num_flights = len(entry['Airline'])
    
    # Expandir los datos por cada vuelo
    for i in range(num_flights):
        expanded_data.append({
            'Airline': entry['Airline'][i],
            'is_direct': entry['is_direct'][i],
            'date_arrival': entry['date_arrival'][i],
            'Boarding_time': entry['Boarding_time'][i],
            'Arrival_time': entry['Arrival_time'][i],
            'Price': entry['Price'][i]
        })

df = pd.DataFrame(expanded_data)
df.to_csv("despegar.csv", sep="|", index=False)

driver.quit()
