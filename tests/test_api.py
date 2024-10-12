import pytest
from pywolt import Wolt, VenueData, MenuItem, ItemSearchResult, City


@pytest.mark.asyncio
async def test_get_venues():
    wolt = Wolt("32.0764967", "34.7626044")

    venues = await wolt.get_venues()

    assert isinstance(venues, list)
    assert len(venues) > 1
    assert isinstance(venues[0], VenueData)


@pytest.mark.asyncio
async def test_get_menu():
    wolt = Wolt("32.0764967", "34.7626044")

    menu = await wolt.get_menu("pizza-place")

    assert isinstance(menu, list)
    assert len(menu) > 1
    assert isinstance(menu[0], MenuItem)


@pytest.mark.asyncio
async def test_search_items():
    wolt = Wolt("32.0764967", "34.7626044")

    items = await wolt.search_items("pizza")

    assert isinstance(items, list)
    assert len(items) > 1
    assert isinstance(items[0], ItemSearchResult)


@pytest.mark.asyncio
async def test_get_cities():
    wolt = Wolt("00.0000", "00.0000")

    items = await wolt.get_cities()

    assert isinstance(items, list)
    assert len(items) > 1
    assert isinstance(items[0], City)
