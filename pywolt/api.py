from typing import NoReturn, Optional
from .data_structures import VenueData, MenuItem, ItemSearchResult, City
import httpx


class Wolt:
    def __init__(
        self,
        lat: str,
        lon: str,
        access_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
    ) -> None:
        self.consumer_endpoint = "https://consumer-api.wolt.com/v1/"
        self.restaurant_endpoint = "https://restaurant-api.wolt.com/"
        self.auth_endpoint = "https://authentication.wolt.com/v1/wauth2/access_token"
        self.basket_endpoint = (
            "url = 'https://consumer-api.wolt.com/order-xp/v1/baskets"
        )
        self.lat = lat
        self.lon = lon
        if refresh_token:
            self.refresh_auth_details(refresh_token)

        else:
            self.access_token = access_token
        self.sesh = httpx.AsyncClient(http2=True)

    async def get_venues(self) -> list[VenueData]:
        response = await self.sesh.get(
            f"{self.consumer_endpoint}pages/restaurants",
            params={"lat": self.lat, "lon": self.lon},
        )
        sections = response.json()["sections"]
        try:
            return [VenueData(**item) for item in sections[1]["items"]]
        except IndexError:
            raise ValueError(sections[0]["title"])

    async def get_menu(
        self,
        venue_slug: str,
        unit_prices: bool = True,
        show_weighted_items: bool = True,
        show_subcategories: bool = True,
    ) -> list[MenuItem]:
        response = await self.sesh.get(
            f"{self.restaurant_endpoint}v4/venues/slug/{venue_slug}/menu/data",
            params={
                "unit_prices": unit_prices,
                "show_weighted_items": show_weighted_items,
                "show_subcategories": show_subcategories,
            },
        )
        data = response.json()["items"]
        return [MenuItem(**item) for item in data]

    async def search_venues(self, query: str) -> list[VenueData]:
        response = await self.sesh.post(
            self.restaurant_endpoint + "v1/pages/search",
            json={
                "q": query,
                "target": "venues",
                "lat": self.lat,
                "lon": self.lon,
            },
        )
        data = response.json()["sections"][0]
        if "items" in data:
            return [VenueData(**item) for item in data["items"]]
        else:
            raise ValueError(data["title"])

    async def search_items(self, query: str) -> list[ItemSearchResult]:
        response = await self.sesh.post(
            self.restaurant_endpoint + "v1/pages/search",
            json={
                "q": query,
                "target": "items",
                "lat": self.lat,
                "lon": self.lon,
            },
        )
        response.raise_for_status()
        data = response.json()["sections"][0]
        if "items" in data:
            return [ItemSearchResult(**item["menu_item"]) for item in data["items"]]
        else:
            raise ValueError(data["title"])

    async def get_cities(
        self,
    ) -> list[ItemSearchResult]:
        response = await self.sesh.get(
            self.restaurant_endpoint + "v1/cities",
        )
        response.raise_for_status()
        data = response.json()["results"]
        return [City(**item) for item in data]

    def refresh_auth_details(self, refresh_token: str) -> NoReturn:
        resp = httpx.post(
            self.auth_endpoint,
            data={
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
            },
        )
        data = resp.json()
        self.access_token = data["access_token"]
        self.refresh_token = data["refresh_token"]

    # def add_to_basket(self, item: MenuItem, amount: int = 1) -> NoReturn:
    #     basket_item = {
    #         "items": [
    #             {
    #                 "id": item.id,
    #                 "count": amount,
    #                 "name": item.name,
    #                 "price": item.baseprice,
    #                 "options": [],
    #                 "substitution_settings": {"is_allowed": "true"},
    #             }
    #         ],
    #         # "venue_id": "5c51940046700c000a146181",
    #         # "currency": "ILS",
    #     }
    #     if self.access_token:

    #         resp = req.post(
    #             self.basket_endpoint,
    #             auth="Bearer " + self.access_token,
    #             data=basket_item,
    #         )
    #         if resp.status_code == 401:
    #             self.refresh_auth_details(self.refresh_token)
    #         else:
    #             pass
