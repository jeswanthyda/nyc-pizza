from map_locations.base_models import Address, Home

__all__ = ["HOMES"]


# Add homes to the list here
HOMES = [
    Home(Address(8, 8)),
    Home(Address(1, 15)),
    Home(Address(2, 120)),
    Home(Address(5, 23)),
    Home(Address(7, 32)),
    Home(Address(10, 45)),
    Home(Address(10, 18)),
    Home(Address(4, 55)),
    Home(Address(11, 65)),
]
