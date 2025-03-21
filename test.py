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
        itinerary_containers = itter_cluster.find_elements(By.CSS_SELECTOR, ".itinerary-container")

        for itinerary in itinerary_containers:
            _airline = ""
            _isDirect = []
            _date_arrival = ""
            _hours_origin = []
            _hours_destination = []
            _price = ""


            spans_airline = itinerary.find_elements(By.CSS_SELECTOR, 'span')
            for span in spans_airline:
                text = span.text.strip()
                if text:
                    _airline = text
                    break  


            stop_span = itinerary.find_elements(By.CSS_SELECTOR, 'span[data-sfa-id="stops-text"]')
            for span in stop_span:
                if span.text.strip() == "Directo":
                    _isDirect.append(1)
                else:
                    _isDirect.append(0)
            if not _isDirect:  
                _isDirect.append(0)


            date_spans = itinerary.find_elements(By.CSS_SELECTOR, 'span[data-sfa-id="route-date"]')
            if date_spans:
                _date_arrival = date_spans[0].text  # Tomamos solo la primera fecha encontrada


            _isHourOrigin = True
            spans_hour = itinerary.find_elements(By.CSS_SELECTOR, "span.hour")
            for span in spans_hour:
                if _isHourOrigin:
                    _hours_origin.append(span.text.strip())
                else:
                    _hours_destination.append(span.text.strip())
                _isHourOrigin = not _isHourOrigin


            span_price = itinerary.find_elements(By.CSS_SELECTOR, "span.amount.price-amount")
            if span_price:
                _price = span_price[0].text.strip()


            if len(_hours_origin) == len(_hours_destination):
                data = {
                    "Airline": [_airline] * len(_hours_origin),
                    "is_direct": _isDirect if len(_isDirect) == len(_hours_origin) else [0] * len(_hours_origin),
                    "date_arrival": [_date_arrival] * len(_hours_origin),
                    "Boarding_time": _hours_origin,
                    "Arrival_time": _hours_destination,
                    "Price": [_price] * len(_hours_origin),
                }
                _output_data.append(data)


expanded_data = []
for entry in _output_data:
    num_flights = len(entry['Airline'])
    
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
