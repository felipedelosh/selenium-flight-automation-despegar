from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configurar Selenium
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")

browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, 10)

# URL de resultados (ajústala según tus parámetros)
search_url = "https://www.despegar.com.co/shop/flights/results/oneway/BOG/MDE/2025-03-19/1/0/0?from=SB&di=1"

# Navegar a la página
browser.get(search_url)
time.sleep(5)  # Esperar para que cargue el contenido dinámico

# Obtener HTML completo después de cargar con JS
html = browser.page_source

# Cerrar navegador
browser.quit()

# Procesar con BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Buscar contenedores de vuelos (ajusta el selector según el HTML real)
flight_containers = soup.find_all("div", class_="cluster-container")  

# Extraer información
flights = []
for flight in flight_containers:
    airline = flight.find("span", class_="airline-name").text.strip() if flight.find("span", class_="airline-name") else "Desconocido"
    price = flight.find("span", class_="amount").text.strip() if flight.find("span", class_="amount") else "Sin precio"
    
    flights.append({"aerolinea": airline, "precio": price})

# Mostrar resultados
for f in flights:
    print(f"Aerolínea: {f['aerolinea']} - Precio: {f['precio']}")
