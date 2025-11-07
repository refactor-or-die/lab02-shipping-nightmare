
from .drone import Drone
from .economy import Economy
from .express import Express
from .internationalstandard import InternationalStandard
from .locker import Locker
from .sameday import SameDay
from .standard import Standard
from .unknown import Unknown
from ..shipping_type import ShippingType


def create_shipping_type(shipping_type: str) -> ShippingType:
    match shipping_type:
        case "standard":
            return Standard()
        case "express":
            return Express()
        case "same_day":
            return SameDay()
        case "economy":
            return Economy()
        case "international_standard":
            return InternationalStandard()
        case "drone":
            return Drone()
        case "locker":
            return Locker()
    return Unknown()