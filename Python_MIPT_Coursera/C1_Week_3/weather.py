import pprint
import requests
from geopy.geocoders import Nominatim


class YandexWeatherAPI:
	def __init__(self):
		self._city_cache = {}

	def get(self, city):
		if city in self._city_cache:
			return self._city_cache[city]

		geolocator = Nominatim(user_agent="grol")
		location = geolocator.geocode(city)
		latitude = location.latitude
		longitude = location.longitude

		url = f"https://api.weather.yandex.ru/v2/forecast?lat={latitude}&lon={longitude}&\
		lang=ru_RU&&limit=2&hours=True&extra=True"

		pprint.pprint('Sending HTTP request')
		resp = requests.get(url, headers={'X-Yandex-API-Key':\
			'13da4012-3fdb-411a-bbd5-19ed85b61af7'})
		weather_resp = resp.json()['forecasts']
		max_temp_forecast = {elem['date']:elem['parts']['day']\
							['temp_max'] for elem in weather_resp}

		self._city_cache[city] = max_temp_forecast							
		return max_temp_forecast

class CityInfo:

	def __init__(self, city, weather_forecast=None):
		self.city = city 
		self._weather_forecast = weather_forecast or YandexWeatherAPI()
	def weather_forecast(self):
		return self._weather_forecast.get(self.city)

def _main():
	city_info = CityInfo(city="Moscow")
	weather_provider = YandexWeatherAPI()
	for i in range(5):
		city_info = CityInfo(city="Moscow", weather_forecast=weather_provider)
		forecast = city_info.weather_forecast()
		pprint.pprint(forecast)

if __name__=="__main__":
	_main()
