from bs4 import BeautifulSoup

with open("data.html", "r") as file:
    soup = BeautifulSoup(file, "html.parser")

# Buscar todos los elementos con la clase "reduced-cluster"
clusters = soup.find_all("cluster", class_="COMMON")

# Imprimir la cantidad de elementos encontrados
print(f"Se encontraron {len(clusters)} elementos con la clase 'reduced-cluster'.")

# Opcional: imprimir el contenido del primer elemento
if clusters:
    for cluster in clusters:
        _airline = ""
        spans_airline = cluster.find_all("span", attrs={"_ngcontent-aqu-c200": True})
        for span in spans_airline:
            _airline = span.get_text(strip=True)
            break

        _isHourOrigin = True
        _hours_origin = []
        _hours_destination = []
        spans_hour = cluster.find_all("span", class_="hour")
        for span in spans_hour:
            if _isHourOrigin:
                _hours_origin.append(span.get_text(strip=True))
            else:
                _hours_destination.append(span.get_text(strip=True))

            _isHourOrigin = not _isHourOrigin


        _price = cluster.find("span", class_="amount price-amount").get_text(strip=True)

        if len(_hours_origin) == len(_hours_destination):
            data = {}
            data["Airline"] = [_airline] * len(_hours_origin)
            data["Boarding_time"] = _hours_origin
            data["Arrival_time"] = _hours_destination
            data["Price"] = [_price] * len(_hours_origin)

            print(data)
        break