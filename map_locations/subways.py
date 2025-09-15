from map_locations.base_models import Address, Subway

__all__ = ["SUBWAYS"]


# Add subways to the list here
SUBWAYS = [
    # 9th avenue
    Subway(Address(9, 23)),
    Subway(Address(9, 52)),
    Subway(Address(9, 86)),
    Subway(Address(9, 120)),
    # 1st avenue
    Subway(Address(1, 40)),
    Subway(Address(1, 75)),
    Subway(Address(1, 110)),
    # 5th avenue
    Subway(Address(5, 23)),
    Subway(Address(5, 52)),
    #
]
