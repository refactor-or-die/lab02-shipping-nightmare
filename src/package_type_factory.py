from package_type import *

class PackageTypeFactory():
    def create(self, shipping_type: str) -> PackageType:
        match shipping_type:
            case "standard":
                return StandardPackage()
            case "express":
                return ExpressPackage()
            case "same_day":
                return SameDayPackage()
            case "economy":
                return EconomyPackage()
            case "international_standard":
                return InternationalStandardPackage()
            case "drone":
                return DronePackage()
            case "locker":
                return LockerPackage()
            case _:
                return UnknownPackage()