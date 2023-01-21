"""
Class files.
"""
import datetime


class Attraction:
    """
    A pseudo-interface for an attraction.
    # _name: name of the attraction.
    # _desc: description of the attraction.
    # _approx_cost: approximate cost of the attraction
    # _rating: rating of the attraction, from 1-5
    """
    _name: str
    _desc: str
    _approx_cost: int
    _rating: int

    def name(self) -> str:
        """:return: name of attraction.
        """
        return self._name

    def desc(self) -> str:
        """:return: description.
        """
        return self._desc

    def approx_cost(self) -> int:
        """:return: approx cost.
        """
        return self._approx_cost

    def rating(self) -> int:
        """:return: rating.
        """
        return self._rating


class Restaurant(Attraction):
    def __init__(self, name: str, desc: str, approx_cost: int, rating: int) -> None:
        self._name = name
        self._desc = desc
        self._approx_cost = approx_cost
        self._rating = rating


class Landmark(Attraction):
    def __init__(self, name: str, desc: str, approx_cost: int, rating: int) -> None:
        self._name = name
        self._desc = desc
        self._approx_cost = approx_cost
        self._rating = rating


class CityItinerary:
    """ The itinerary for a given city.
    name: name of the city.
    desc: description.
    start_date: the first day of the city trip
    end_date: the last day of the city trip
    """
    name: str
    desc: str
    start_date: datetime.date
    end_date: datetime.date
    image: str
    attractions: list[Attraction]