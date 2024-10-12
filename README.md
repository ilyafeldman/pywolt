# PyWolt

PyWolt is a Python library that provides an open API for interacting with the popular food delivery application Wolt. It utilizes the native, internal Wolt web API and wraps it in a Pythonic interface.

## Features

- **List Available Venues**: Retrieve a list of available venues for a given set of coordinates.
- **Search Venues**: Search for venues based on coordinates and a text query.
- **Search Food Items**: Search for food items based on coordinates and a text query.
- **List Venue Menu**: Retrieve the menu of a specific venue.
- **List Cities**: Retrieve a list of cities and their coordinates using Wolt's buit-in api
Upcoming Features:
- **Authentication**: Authenticate to get access to the user's basket and make orders.

## Usage Examples

### Get Venues
```python
from pywolt.api import Wolt
import asyncio

# Initialize Wolt instance with latitude and longitude
wolt = Wolt(lat="35.0844", lon="106.6504")

# Get venues available at specified coordinates
venues = asyncio.run(wolt.get_venues())

# Get details of a specific venue (e.g., Los Pollos Hermanos)
los_pollos = venues[0]

print(los_pollos.venue.name)
```
```python
Los Pollos Hermanos
```

### Get the menu of the venue
```python
los_pollos_menu = asyncio.run(wolt.get_menu(los_pollos.venue.slug))
```

### Search Venues
```python
los_pollos_menu = asyncio.run(wolt.search_venues("pizza"))
```
### Search Items
```python
los_pollos_menu = asyncio.run(wolt.search_items("pizza"))
```
### Get Cities
```python
los_pollos_menu = asyncio.run(wolt.get_cities())
```


## License

This project is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike (CC BY-NC-SA) 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).
