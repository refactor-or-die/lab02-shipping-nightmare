"""
Unit tests for shipping cost calculator.
DON'T MODIFY TESTS! They should pass both before and after refactoring.
"""
import pytest
from datetime import datetime, timedelta
from shipping_calculator import Package, ShippingCalculator


class TestShippingCalculator:
    
    @pytest.fixture
    def calculator(self):
        return ShippingCalculator()
    
    @pytest.fixture
    def small_package(self):
        return Package(0.5, (20, 15, 10), 50)
    
    @pytest.fixture
    def medium_package(self):
        return Package(5, (40, 30, 20), 200, is_fragile=True)
    
    @pytest.fixture
    def large_package(self):
        return Package(15, (60, 50, 40), 500)
    
    def test_standard_shipping_basic(self, calculator, small_package):
        result = calculator.calculate_shipping(small_package, "standard", 50)
        assert result["cost"] == 15.0
        assert "Standard" in result["info"]
    
    def test_standard_shipping_with_weight_penalty(self, calculator):
        heavy_package = Package(7, (30, 30, 30), 100)
        result = calculator.calculate_shipping(heavy_package, "standard", 50)
        # Base 15 + (7-5)*2 = 15 + 4 = 19
        assert result["cost"] == 19.0
    
    def test_standard_shipping_with_distance(self, calculator, small_package):
        result = calculator.calculate_shipping(small_package, "standard", 200)
        # Base 15 + (200-100)*0.1 = 15 + 10 = 25
        assert result["cost"] == 25.0
    
    def test_express_weight_limit(self, calculator):
        heavy_package = Package(20, (40, 40, 40), 300)
        result = calculator.calculate_shipping(heavy_package, "express", 100)
        assert result["cost"] is None
        assert "over 15kg" in result["info"]
    
    def test_express_fragile_fee(self, calculator, medium_package):
        result = calculator.calculate_shipping(medium_package, "express", 100)
        # Base 30 + (5-3)*4 + 100*0.2 + 15(fragile) = 30 + 8 + 20 + 15 = 73
        assert result["cost"] == 73.0
    
    def test_same_day_distance_limit(self, calculator, small_package):
        result = calculator.calculate_shipping(small_package, "same_day", 100)
        assert result["cost"] is None
        assert "up to 50km" in result["info"]
    
    def test_same_day_vip_free(self, calculator, small_package):
        result = calculator.calculate_shipping(small_package, "same_day", 30, "vip")
        assert result["cost"] == 0.0
    
    def test_economy_no_fragile(self, calculator, medium_package):
        result = calculator.calculate_shipping(medium_package, "economy", 100)
        assert result["cost"] is None
        assert "fragile" in result["info"]
    
    def test_economy_long_distance_discount(self, calculator):
        package = Package(2, (30, 30, 30), 50)
        result = calculator.calculate_shipping(package, "economy", 600)
        # Base 10 + 2*1.5 = 13, then *0.8 = 10.4
        assert result["cost"] == 10.4
    
    def test_international_customs(self, calculator):
        valuable_package = Package(1, (20, 20, 20), 200)
        result = calculator.calculate_shipping(valuable_package, "international_standard", 500)
        # Base 45 + customs(200*0.23=46) = 91
        assert result["cost"] == 91.0
        assert "customs" in result["info"]
    
    def test_drone_weight_limit(self, calculator, medium_package):
        result = calculator.calculate_shipping(medium_package, "drone", 10)
        assert result["cost"] is None
        assert "up to 2kg" in result["info"]

    def test_drone_distance_limit(self, calculator, small_package):
        result = calculator.calculate_shipping(small_package, "drone", 30)
        assert result["cost"] is None
        assert "20km" in result["info"]
    
    def test_locker_size_limit(self, calculator):
        oversized = Package(10, (70, 40, 40), 300)
        result = calculator.calculate_shipping(oversized, "locker", 30)
        assert result["cost"] is None
        assert "too large" in result["info"]
    
    def test_locker_vip_free(self, calculator, small_package):
        result = calculator.calculate_shipping(small_package, "locker", 30, "vip")
        assert result["cost"] == 0.0
    
    def test_premium_discount_standard(self, calculator, small_package):
        regular = calculator.calculate_shipping(small_package, "standard", 50, "regular")
        premium = calculator.calculate_shipping(small_package, "standard", 50, "premium")
        assert premium["cost"] == regular["cost"] * 0.9
    
    def test_unknown_shipping_type(self, calculator, small_package):
        result = calculator.calculate_shipping(small_package, "teleportation", 50)
        assert result["cost"] is None
        assert "Unknown" in result["info"]
    
    def test_delivery_dates(self, calculator, small_package):
        # Test if delivery dates are reasonable
        standard = calculator.calculate_shipping(small_package, "standard", 50)
        express = calculator.calculate_shipping(small_package, "express", 50)
        same_day = calculator.calculate_shipping(small_package, "same_day", 20)

        now = datetime.now()

        # Standard: 3 days
        assert (standard["delivery_date"] - now).days >= 2

        # Express: 1 day
        assert (express["delivery_date"] - now).days >= 0

        # Same day: today
        assert same_day["delivery_date"].date() == now.date()