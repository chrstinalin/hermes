"""
Class files.
"""
# import urllib.request
import requests
import json
from typing import Any
from unidecode import unidecode
import backoff
import datetime
import openai
from iso3166 import countries
from openai.error import RateLimitError

openai.api_key = "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"
google_cloud_key = "AIzaSyA0InFNkcG7UtX5Fd9A5i0vZUpZCDwP6d4"

class Attraction:
    """
    A city attraction.
    # _name: name of the attraction.
    # _desc: description of the attraction.
    """
    _name: str
    _desc: str
    _type: str
    coordinates: tuple[float, float]  # longitude-latitude

    def __init__(self, name: str, desc: str, type_name: str) -> None:
        self._name = name
        self._desc = desc
        self._type = type_name

    def name(self) -> str:
        """:return: name of attraction.
        """
        return self._name

    def desc(self) -> str:
        """:return: description.
        """
        return self._desc

    def type(self) -> str:
        """:return: description.
        """
        return self._type

    def get_coordinates(self) -> tuple[float, float]:
        """:return: coordinates.
        """
        return self.coordinates

class CityItinerary:
    """ The itinerary for a given city.
    city: name of the city.
    desc: description.
    start_date: the first day of the city trip
    end_date: the last day of the city trip
    image: image url of the city.
    attractions: list of attractions.
    restaurants: list of restaurants.
    coordinates: tuple, longitude-latitude
    """
    city: str
    desc: str
    start_date: datetime.date
    end_date: datetime.date
    image: str
    attractions: list[Attraction]
    restaurants: list[Attraction]
    coordinates: tuple[float, float]  # longitude-latitude

    def __init__(self, city: str, desc: str, start_date: datetime.datetime, end_date: datetime.datetime, image: str, attractions: list[Attraction], restaurants: list[Attraction]) -> None:
        self.city = city
        self.desc = desc
        self.start_date = start_date
        self.end_date = end_date
        self.image = image
        self.attractions = attractions
        self.restaurants = restaurants


def daterange(start_date: datetime.datetime, end_date: datetime.datetime):
    """
    Helper function. Given a start and end date, returns an iterator through each day.
    :param start_date: Day to start at.
    :param end_date: Day to end at.
    :return:
    """
    for i in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(i)


def generate_single_day_attractions(number_of_attractions: int, city: str, keywords: str, attraction_type: str) -> list[Attraction]:
    """
    Bundles and generates metadata for a list of attractions to visit in the given city.

    :param city: name of the city.
    :param number_of_attractions: number of attractions to generate for.
    :param keywords: to generate with.
    :param attraction_type: type of attraction, attraction or restaurant.
    :return: a list of Attraction objects.
    """
    attractions = list()
    attraction_names = list(filter(None, ai_call(max_tokens=50, temperature=0, prompt="Reddit List of Names of " + number_of_attractions.__str__() + " " + attraction_type + "s to visit in \"" + city + "\", based on the keywords: \"" + keywords + "\"").choices[0].text.split("\n")))
    #
    for attraction in attraction_names:
        desc = ai_call(max_tokens=200, temperature=0, prompt="Describe the " + attraction_type + " " + attraction + " in " + city + "in one paragraph").choices[0].text.strip()

        # Loads the json file containing the coordinates of the attraction
        attraction_name = unidecode(attraction[3:].replace(" ", "%").replace("\'", "") + "%" + city)

        json_url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + attraction_name + "&key=" + google_cloud_key

        r = requests.get(json_url)
        data = r.json()

        # Extracts the coordinates
        try:
            lat = data["results"][0]["geometry"]["location"]["lat"]
            long = data["results"][0]["geometry"]["location"]["lng"]
            coordinates = lat, long

        except IndexError:
            print("Error, location not found of " + attraction)

        # Creates an Attraction
        a = Attraction(attraction, desc, attraction_type)
        a.coordinates = (lat, long)
        attractions.append(a)

    return attractions


def generate_city_itinerary(city: str, start_end: tuple[datetime.datetime, datetime.datetime], keywords: str) -> CityItinerary:
    """ Generates an itinerary for a given city.
    """
    start_date, end_date = start_end
    total_days = int((end_date - start_date).days)

    attractions = generate_single_day_attractions(total_days * 3, city, keywords, "attraction")  # TODO: Remove hardcode, perhaps as a user slider
    restaurants = generate_single_day_attractions(total_days * 3, city, keywords, "restaurant")

    desc = ai_call(max_tokens=200, temperature=0, prompt="Describe " + city + " in " + "in one paragraph").choices[0].text

    image = ""  # TODO: Image of the city

    return CityItinerary(city, desc, start_date, end_date, image, attractions, restaurants)


def generate_itinerary(locations: dict[str: tuple[datetime.datetime, datetime.datetime]], keywords: str) -> list[CityItinerary]:
    """ Generates the full itinerary from a list of locations given by the user.
    """
    final_itinerary = list()

    for location_name in locations:

        if countries.__contains__(location_name):  # TODO: Countries, add variability in number of cities (will require calculating date ranges)
            cities = ai_call(max_tokens=100, prompt="Best city to visit in " + countries.get(location_name).name + "").choices[0].text.split("\n")
            for city in cities:
                final_itinerary.append(generate_city_itinerary(city, locations[location_name], keywords))
        else:
            final_itinerary.append(generate_city_itinerary(location_name, locations[location_name], keywords))

    # TODO: sort final itinerary to be most efficient path. MAY COME NATURALLY THROUGH PATHS API.

    return final_itinerary


@backoff.on_exception(backoff.expo, RateLimitError)
def ai_call(max_tokens: int, temperature: float, prompt: str) -> Any:
    return openai.Completion.create(max_tokens=max_tokens, temperature=temperature, engine="text-curie-001", prompt=prompt)


if __name__ == '__main__':
    itinerary = generate_itinerary({"Toronto, Canada": (datetime.datetime(2020, 1, 1), datetime.datetime(2020, 1, 3)), "Vancouver, Canada":(datetime.datetime(2020, 1, 4), datetime.datetime(2020, 1, 5))}, "Family-Friendly, Vegetarian")

    for cityitinerary in itinerary:
        print(cityitinerary.city + " " + cityitinerary.desc)

        for attraction in cityitinerary.attractions:
            print(attraction.name() + ": " + attraction.desc())
            print(attraction.get_coordinates())

        for restaurant in cityitinerary.restaurants:
            print(restaurant.name() + ": " + restaurant.desc())
            print(restaurant.get_coordinates())

        print("\n")
