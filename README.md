# PyWolt

PyWolt is a Python library that provides an open API for interacting with the popular food delivery application Wolt. It utilizes the native, internal Wolt web API and wraps it in a Pythonic interface, allowing developers to easily integrate Wolt's functionality into their Python projects.

## Features

- **List Available Venues**: Retrieve a list of available venues for a given set of coordinates.
- **Search Venues**: Search for venues based on coordinates and a text query.
- **Search Food Items**: Search for food items based on coordinates and a text query.
- **List Venue Menu**: Retrieve the menu of a specific venue.

Upcoming Features:
- **Authentication**: Authenticate to get access to the user's basket and make orders.

## How to Use PyWolt

1. Install Poetry:

   ```bash
   curl -sSL https://install.python-poetry.org | python -
   ```

2. Clone the project:

   ```bash
   git clone https://github.com/ilyafeldman/pywolt
   ```

3. Navigate into the project folder:

   ```bash
   cd pywolt
   ```

4. Install dependencies:

   ```bash
   poetry install
   ```

5. You are now ready to use PyWolt in your Python projects!

## Code Example

```python
from pywolt.api import Wolt

# Initialize Wolt instance with latitude and longitude
wolt = Wolt(lat="XX.XXXXXX", lon="XX.XXXXXX")

# Get venues available at specified coordinates
venues = wolt.get_venues()

# Get details of a specific venue (e.g., Los Pollos Hermanos)
los_pollos = venues["Los Pollos Hermanos"]

# Get the menu of the venue
los_pollos_menu = wolt.get_menu(los_pollos.venue.slug)

# Get details of a specific item from the menu (e.g., Chicken Fillet Burger)
burger = los_pollos_menu["Chicken Fillet Burger"]
```

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike (CC BY-NC-SA) 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).
