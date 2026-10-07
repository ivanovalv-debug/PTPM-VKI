import sys
import os
import unittest
import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from delivery_service import calculate_delivery_cost


class TestDeliveryService(unittest.TestCase):

    def test_valid_standard_package(self):
        result = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(result[0], 700)
        expected_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        self.assertEqual(result[1], expected_date)

    def test_weight_5kg_no_multiplier(self):
        result = calculate_delivery_cost(5.0, 100, "обычный")
        self.assertEqual(result[0], 840)

    def test_weight_20kg_multiplier_applied(self):
        result = calculate_delivery_cost(20.0, 100, "обычный")
        self.assertEqual(result[0], 1050)

    def test_fragile_package_surcharge(self):
        result = calculate_delivery_cost(1.0, 100, "хрупкий")
        self.assertEqual(result[0], 1000)

    def test_dangerous_package_surcharge(self):
        result = calculate_delivery_cost(1.0, 100, "опасный")
        self.assertEqual(result[0], 1700)

    def test_express_delivery_cost_halved(self):
        result = calculate_delivery_cost(1.0, 100, "обычный", is_express=True)
        self.assertEqual(result[0], 1050)

    def test_express_delivery_time_reduced(self):
        result = calculate_delivery_cost(1.0, 1000, "обычный", is_express=True)
        expected_date = (datetime.date.today() + datetime.timedelta(days=2)).strftime("%Y-%m-%d")
        self.assertEqual(result[1], expected_date)

    def test_invalid_weight_too_light(self):
        result = calculate_delivery_cost(0.05, 100, "обычный")
        self.assertEqual(result[0], -1)

    def test_invalid_weight_too_heavy(self):
        result = calculate_delivery_cost(55.0, 100, "обычный")
        self.assertEqual(result[0], -1)

    def test_invalid_distance_zero(self):
        result = calculate_delivery_cost(1.0, 0, "обычный")
        self.assertEqual(result[0], -1)

    def test_invalid_package_type(self):
        result = calculate_delivery_cost(1.0, 100, "животное")
        self.assertEqual(result[0], -1)

    def test_boundary_weight_5kg_exact(self):
        result = calculate_delivery_cost(5.0, 100, "обычный")
        self.assertEqual(result[0], 840)


if __name__ == "__main__":
    unittest.main()