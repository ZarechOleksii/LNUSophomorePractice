from enum import Enum, unique


@unique
class RestaurantName(Enum):
    Delice = 1
    EuroHotel = 2
    Morio = 3

    def __gt__(self, other):
        return self.name.lower() > other.name.lower()

    def __str__(self):
        return self.name
