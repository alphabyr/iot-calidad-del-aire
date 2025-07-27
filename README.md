
### PROYECTO IOT PARA ESTUDIAR LA CONTAMINACION DEL AIRE EN EL AEROPUERTO JFK DE NEW YORK

Este script recopila datos de contaminacion del aeropuerto JFK, usando los sensores y API publicos de Open Weather Map, y envia los resultados a un canal de ThingSpeak para su posterior analisis.

Desarrollado por:

* Jesus Delgado Ventajas
* Diego Villatoro Reyes
* Wilson Penaherrera Plua
* Steven Garcia Castrillon

#### Requisitos
* Python version ~3.10
* Instalar librerias necesarias: pip install -r requirements.txt
* Un canal preconfigurado de Thingspeak con campos para recibir valores como aqi, pm25, pm10 y co.
#### Instrucciones:

* Crear un archivo llamado ".env" con las claves secretas para las API con la siguiente estructura:
```
OPENWEATHER_API_KEY=claveAPIopenWeatherMapAqui
THINGSPEAK_API_KEY=ClaveWriteAPIThingSpeakAqui
```
* El script se ejecuta con el comando: python3 calidad_del_aire.py
