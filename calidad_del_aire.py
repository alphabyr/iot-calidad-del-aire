import requests
import time
import os
from dotenv import load_dotenv
import os

load_dotenv()  # Cargar variables de entorno desde el archivo .env

# CONFIGURACIÓN
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
THINGSPEAK_API_KEY = os.getenv("THINGSPEAK_API_KEY")
INTERVALO = 10  # Tiempo entre cada aeropuerto (en segundos)

# LISTA DE AEROPUERTOS
AEROPUERTOS = [
    {"nombre": "JFK - New York", "lat": 40.6413, "lon": -73.7781, "codigo": "JFK"},
    {"nombre": "LHR - London Heathrow", "lat": 51.4700, "lon": -0.4543, "codigo": "LHR"},
    {"nombre": "CDG - Paris Charles de Gaulle", "lat": 49.0097, "lon": 2.5479, "codigo": "CDG"},
    {"nombre": "HND - Tokyo Haneda", "lat": 35.5494, "lon": 139.7798, "codigo": "HND"},
    {"nombre": "GRU - São Paulo", "lat": -23.4356, "lon": -46.4731, "codigo": "GRU"},
]

def obtener_datos_calidad_aire(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        datos = r.json()
        info = datos["list"][0]
        aqi = info["main"]["aqi"]
        pm25 = info["components"]["pm2_5"]
        pm10 = info["components"]["pm10"]
        co = info["components"]["co"]
        return aqi, pm25, pm10, co
    except requests.RequestException as req_err:
        raise Exception(f"Error de red al consultar OpenWeather: {req_err}")
    except (KeyError, IndexError, ValueError) as parse_err:
        raise Exception(f"Error al procesar datos de OpenWeather: {parse_err}")

def enviar_a_thingspeak(aqi, pm25, pm10, co, codigo_aeropuerto):
    try:
        url = (
            f"https://api.thingspeak.com/update?api_key={THINGSPEAK_API_KEY}"
            f"&field1={aqi}&field2={pm25}&field3={pm10}&field4={co}"
            f"&status=Aeropuerto: {codigo_aeropuerto}"
        )
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        print(f"Enviado: {codigo_aeropuerto} | Respuesta: {r.text}")
    except requests.RequestException as req_err:
        print(f"Error al enviar a ThingSpeak para {codigo_aeropuerto}: {req_err}")

def main():
    while True:
        for aeropuerto in AEROPUERTOS:
            try:
                print(f"\nConsultando datos de {aeropuerto['nombre']}...")
                aqi, pm25, pm10, co = obtener_datos_calidad_aire(aeropuerto["lat"], aeropuerto["lon"])
                print(f"   AQI: {aqi} | PM2.5: {pm25} | PM10: {pm10} | CO: {co}")
                enviar_a_thingspeak(aqi, pm25, pm10, co, aeropuerto["codigo"])
            except Exception as e:
                print(f"Error con {aeropuerto['codigo']}: {e}")
            time.sleep(INTERVALO)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nEjecución interrumpida por el usuario.")
