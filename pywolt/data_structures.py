from typing import List, Optional, Dict, Any, Union
from pydantic_extra_types.color import Color
from pydantic_extra_types.currency_code import ISO4217
from pydantic_extra_types.country import CountryAlpha3, CountryAlpha2
from pydantic import BaseModel, Field
from pydantic_geojson import PointModel
from pydantic_geojson._base import Coordinates


class SortingSortables(BaseModel):
    """
    Sortable options for sorting venues.
    """

    id: str
    value: int


class FilteringFilters(BaseModel):
    """
    Filtering options for filtering venues.
    """

    id: str
    values: List[str]


class VenueRating(BaseModel):
    """
    Rating of a venue.
    """

    rating: int
    score: float


class Image(BaseModel):
    """
    Image associated with a venue.
    """

    blurhash: Optional[str]
    url: str


class Link(BaseModel):
    """
    Link associated with a venue.
    """

    selected_delivery_method: str
    target: str
    target_sort: str
    target_title: str
    title: str
    type: str
    venue_mainimage_blurhash: str


class OverlayV2(BaseModel):
    """
    Represents an overlay for a venue.
    """

    icon: Optional[str] = None
    primary_text: str
    secondary_text: Optional[str] = None
    telemetry_status: str
    variant: str


class Venue(BaseModel):
    """
    Represents a venue (e.g., restaurant, grocery shop) that can be ordered from.
    """

    address: str
    badges: List[dict]
    badges_v2: List[str]
    categories: List[str]
    city: str
    country: CountryAlpha3
    currency: ISO4217
    delivers: bool
    delivery_price: Optional[Union[str, dict]] = None
    delivery_price_highlight: bool
    delivery_price_int: Optional[int] = None
    estimate: int
    estimate_range: str
    franchise: str
    icon: Optional[str] = None
    id: str
    location: Coordinates
    name: str
    online: bool
    price_range: int
    product_line: str
    promotions: List[Dict[str, str]]
    rating: Optional[VenueRating] = None
    short_description: Optional[str] = None
    show_wolt_plus: bool
    slug: str
    tags: List[str]


class VenueData(BaseModel):
    """
    Represents data associated with a venue.
    """

    filtering: Dict[str, List[FilteringFilters]]
    image: Image
    link: Link
    sorting: Dict
    telemetry_venue_badges: List[str]
    template: str
    title: str
    track_id: str
    venue: Venue
    overlay: Optional[str] = None
    overlay_v2: Optional[OverlayV2] = None

    def __repr__(self):
        open_status = "Open" if self.venue.online else "Closed"
        price_range_desc = {
            1: "💲",
            2: "💲💲",
            3: "💲💲💲",
            4: "💲💲💲💲",
            5: "💲💲💲💲💲",
        }.get(self.venue.price_range, "Unknown")

        tags_str = (
            ", ".join(self.venue.tags) if self.venue.tags else "No tags available"
        )

        delivery_estimate = (
            f"{self.venue.estimate} mins" if self.venue.estimate else "Not available"
        )

        additional_fields = [
            f"Delivery Price: {self.venue.delivery_price}",
            (
                f"Score: {self.venue.rating.score}"
                if self.venue.rating
                else "No rating available"
            ),
        ]

        return (
            f"Name: {self.venue.name}\n"
            f"Address: {self.venue.address}\n"
            f"Price Range: {price_range_desc}\n"
            f"Status: {open_status}\n"
            f"Tags: {tags_str}\n"
            f"Delivery Estimate: {delivery_estimate}\n" + "\n".join(additional_fields)
        )


class MenuItemOption(BaseModel):
    """
    Represents an option for a menu item, which may have multiple choices.
    """

    id: str
    name: str
    maximum_single_selections: int
    maximum_total_selections: int
    minimum_total_selections: int
    parent: str
    required_option_selections: list


class MenuItem(BaseModel):
    """
    Represents a single item from a venue's menu.
    """

    advertising_badge: Optional[str]
    advertising_metadata: Optional[Dict[str, Any]]
    alcohol_percentage: float
    allowed_delivery_methods: List[str]
    barcode_gtin: Optional[str]
    baseprice: int
    brand_id: Optional[str]
    caffeine_content: Optional[dict]
    category: str
    checksum: str
    deposit: Optional[float]
    deposit_type: Optional[str]
    description: str
    dietary_preferences: List[str]
    disabled_info: Optional[Dict[str, Any]]
    enabled: bool
    exclude_from_discounts: bool
    exclude_from_discounts_min_basket: bool
    fulfillment_lead_time: Optional[int]
    has_extra_info: bool
    id: str
    images: List[Image]
    is_cutlery: bool
    lowest_historical_price: Optional[float]
    mandatory_warnings: List[str]
    max_quantity_per_purchase: Optional[int]
    min_quantity_per_purchase: Optional[int]
    name: str
    no_contact_delivery_allowed: bool
    options: List[MenuItemOption]
    original_price: Optional[float]
    quantity_left: Optional[int]
    quantity_left_visible: bool
    restrictions: Optional[List[Dict]]
    return_policy: Optional[str]
    sell_by_weight_config: Optional[Dict[str, Any]]
    tags: List[dict]
    times: List[Dict[str, Any]]
    type: str
    unformatted_unit_price: Optional[Dict]
    unit_info: Optional[str]
    unit_price: Optional[str]
    validity: Optional[dict]
    vat_percentage: float
    wolt_plus_only: bool

    def __repr__(self):
        return (
            f"Description: {self.description}\n"
            f"Price: {self.baseprice/100}₪\n"
            f"Availability: {'Available' if self.enabled else 'Not available'}\n"
        )


class Tag(BaseModel):
    background_color: Color
    name: str
    text_color: Color
    variant: str


class ItemSearchResult(BaseModel):
    country: CountryAlpha3
    currency: ISO4217
    delivery_price: Optional[int] = None
    delivery_price_highlight: bool
    estimate_range: str
    id: str
    image: Optional[Image] = None
    is_available: bool
    name: str
    price: int
    price_type: str
    show_wolt_plus: bool
    tags: List[Union[str, dict]]
    venue_id: str
    venue_name: str
    venue_rating: VenueRating


class City(BaseModel):
    country_code_alpha2: CountryAlpha2 = Field(
        ..., description="Alpha-2 code of the country"
    )
    country_code_alpha3: CountryAlpha3 = Field(
        ..., description="Alpha-3 code of the country"
    )
    has_frontpage: bool = Field(
        ..., description="Indicates if the city has a front page"
    )
    id: str = Field(..., description="Unique identifier for the city")
    location: PointModel = Field(
        ..., description="Location data including coordinates and type"
    )
    name: str = Field(..., description="Name of the city")
    slug: str = Field(..., description="URL-friendly string for the city name")
    subareas: List[str] = Field(
        default_factory=list, description="List of subareas within the city"
    )
    timezone: str = Field(..., description="Timezone of the city")
