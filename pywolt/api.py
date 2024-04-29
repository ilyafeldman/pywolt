from typing import Dict
from .data_structures import VenueData, MenuItem
import httpx as req


class Wolt:

    def __init__(
        self,
        lat: str,
        lon: str,
        access_token: str | None = None,
        refresh_token: str | None = None,
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
            auth_details = self.get_auth_details(refresh_token)
            self.refresh_token = auth_details["refresh_token"]
            self.access_token = auth_details["access_token"]

        else:
            self.access_token = access_token

    def get_venues(self) -> dict[str, VenueData]:
        return {
            item.get("title"): VenueData(**item)
            for item in req.get(
                self.consumer_endpoint + "pages/restaurants",
                params={"lat": self.lat, "lon": self.lon},
            ).json()["sections"][1]["items"]
        }

    def get_menu(self, venue_slug: str) -> Dict[str, MenuItem]:
        return {
            item.get("name"): MenuItem(**item)
            for item in req.get(
                self.restaurant_endpoint
                + "v4/venues/slug/"
                + venue_slug
                + "/menu/data",
                params={
                    "unit_prices": "true",
                    "show_weighted_items": "true",
                    "show_subcategories": "true",
                },
            ).json()["items"]
        }

    def search_venues(self, query: str) -> Dict[str, VenueData]:
        return {
            item.get("title"): VenueData(**item)
            for item in req.post(
                self.restaurant_endpoint + "v1/pages/search",
                json={
                    "q": query,
                    "target": "venues",
                    "lat": self.lat,
                    "lon": self.lon,
                },
            ).json()["sections"][0]["items"]
        }

    def search_items(self, query: str) -> Dict[str, VenueData]:
        return {
            item.get("title"): VenueData(**item)
            for item in req.post(
                self.restaurant_endpoint + "v1/pages/search",
                json={
                    "q": query,
                    "target": "venues",
                    "lat": self.lat,
                    "lon": self.lon,
                },
            ).json()["sections"][0]["items"]
        }

    def get_auth_details(self, refresh_token: str) -> Dict[str, str]:
        resp = req.post(
            self.auth_endpoint,
            data={
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
            },
        ).json()
        return resp

    def add_to_basket(self, item: MenuItem, amount: int = 1):
        basket_item = {
            "items": [
                {
                    "id": item.id,
                    "count": amount,
                    "name": item.name,
                    "price": item.baseprice,
                    "options": [],
                    "substitution_settings": {"is_allowed": "true"},
                }
            ],
            "venue_id": "5c51940046700c000a146181",
            "currency": "ILS",
        }
        req.post(
            self.basket_endpoint, auth="Bearer " + self.access_token, data=basket_item
        )
