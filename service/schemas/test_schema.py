import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

# class TestSchema(BaseModel):
#     id: int
#     name: str
#     description: str


class TaxiEstimated(BaseModel):
    """
    Schema for response of calculate_price endpoint.
    """

    eta_price: Optional[float] = Field(example=1000.09, description="Estimated price")
    eta_time: Optional[datetime.datetime] = Field(
        example="2022-01-05T16:41:24+03:30", description="Estimated arrival time"
    )

    class Config:
        schema_extra = {
            "example": {
                "eta_price": 1000.09,
                "eta_time": "2022-01-05T16:41:24+03:30",
            }
        }


class CalculatePriceRequest(BaseModel):
    """
    Schema for calculate price request.
    """

    phone: str = Field(example="79998887755", description="Client phone number")
    place_from: str = Field(example="ул. Московская", description="Place from")
    place_to: str = Field(example="ул. Ленина", description="Place to")
    arrive_date: datetime.datetime = Field(
        example="2022-01-05T16:41:24+03:30", description="Arrival date"
    )
    car_class_id: str = Field(example="econom", description="Car class id")

    class Config:
        schema_extra = {
            "example": {
                "place_from": "ул. Московская",
                "place_to": "ул. Ленина",
                "arrival_date": "2022-01-05T16:41:24+03:30",
                "car_class_id": "econom",
            }
        }
