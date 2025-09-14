from map_locations.base_models import Address, Subway

__all__ = ["SUBWAYS"]


# Add subways to the list here
SUBWAYS = [
    Subway(Address(9, 86)),
    Subway(Address(1, 40)),
    Subway(Address(9, 52)),
]
