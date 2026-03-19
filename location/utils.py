import requests
import time

def get_lat_lon(city, state, pin):
    address = f"{city}, {state}, {pin}, India"

    url = "https://nominatim.openstreetmap.org/search"

    headers = {
        "User-Agent": "CarLelo/1.0 (carleloteam@gmail.com)"
    }

    params = {
        "q": address,
        "format": "json"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        time.sleep(1)  # respect API rate limit
        print("Response:", data)
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])

    except requests.exceptions.RequestException as e:
        print("Error fetching location:", e)

    return None, None