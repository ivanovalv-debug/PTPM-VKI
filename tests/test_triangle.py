import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.triangle import TriangleAnalyzer


class TestTriangleAnalysis(unittest.TestCase):

    def setUp(self):
        self.analyzer = TriangleAnalyzer()

    def test_equilateral_triangle(self):
        result = self.analyzer.analyze("3", "3", "3")
        self.assertEqual(result["type"], "равносторонний")

    def test_isosceles_triangle_ab(self):
        result = self.analyzer.analyze("5", "5", "8")
        self.assertEqual(result["type"], "равнобедренный")

    def test_isosceles_triangle_bc(self):
        result = self.analyzer.analyze("8", "5", "5")
        self.assertEqual(result["type"], "равнобедренный")

    def test_isosceles_triangle_ac(self):
        result = self.analyzer.analyze("5", "8", "5")
        self.assertEqual(result["type"], "равнобедренный")

    def test_scalene_triangle(self):
        result = self.analyzer.analyze("3", "4", "5")
        self.assertEqual(result["type"], "разносторонний")

    def test_float_sides_valid(self):
        result = self.analyzer.analyze("2.5", "2.5", "3.0")
        self.assertEqual(result["type"], "равнобедренный")

    def test_non_numeric_input_abc(self):
        result = self.analyzer.analyze("abc", "5", "5")
        self.assertEqual(result["type"], "")
        self.assertEqual(result["coordinates"], [(-2, -2), (-2, -2), (-2, -2)])

    def test_negative_side(self):
        result = self.analyzer.analyze("-5", "5", "5")
        self.assertEqual(result["type"], "не треугольник")
        self.assertEqual(result["coordinates"], [(-1, -1), (-1, -1), (-1, -1)])

    def test_zero_side(self):
        result = self.analyzer.analyze("0", "5", "5")
        self.assertEqual(result["type"], "не треугольник")

    def test_empty_string_input(self):
        result = self.analyzer.analyze("", "5", "5")
        self.assertEqual(result["type"], "")

    def test_special_chars_input(self):
        result = self.analyzer.analyze("5@", "#5", "5")
        self.assertEqual(result["type"], "")

    def test_inequality_violation_large_c(self):
        result = self.analyzer.analyze("1", "2", "10")
        self.assertEqual(result["type"], "не треугольник")

    def test_inequality_violation_sum_equal(self):
        result = self.analyzer.analyze("2", "3", "5")
        self.assertEqual(result["type"], "не треугольник")

    def test_all_zeros(self):
        result = self.analyzer.analyze("0", "0", "0")
        self.assertEqual(result["type"], "не треугольник")

    def test_coordinates_in_bounds_100x100(self):
        result = self.analyzer.analyze("10", "10", "10")
        for x, y in result["coordinates"]:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, 100)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, 100)

    def test_coordinates_count(self):
        result = self.analyzer.analyze("3", "4", "5")
        self.assertEqual(len(result["coordinates"]), 3)

    def test_coordinates_tuple_format(self):
        result = self.analyzer.analyze("3", "4", "5")
        for coord in result["coordinates"]:
            self.assertIsInstance(coord, tuple)
            self.assertEqual(len(coord), 2)

    def test_large_sides_scaling(self):
        result = self.analyzer.analyze("1000", "1000", "1000")
        self.assertEqual(result["type"], "равносторонний")
        for x, y in result["coordinates"]:
            self.assertLessEqual(x, 100)
            self.assertLessEqual(y, 100)

    def test_very_small_positive_sides(self):
        result = self.analyzer.analyze("0.001", "0.001", "0.001")
        self.assertEqual(result["type"], "равносторонний")

    def test_mixed_error_and_valid_coords(self):
        result = self.analyzer.analyze("-1", "5", "5")
        self.assertNotEqual(result["coordinates"][0], (-2, -2))
        self.assertEqual(result["coordinates"][0], (-1, -1))


if __name__ == "__main__":
    unittest.main()