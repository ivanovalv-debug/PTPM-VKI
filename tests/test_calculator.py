import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from pages.calculator_page import CalculatorPage


class TestSimpleCalculator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._options = Options()
        cls._options.add_argument("--headless=new")
        cls._options.add_argument("--window-size=1280,1024")
        cls._options.add_argument("--no-sandbox")
        cls._options.add_argument("--disable-dev-shm-usage")

    def setUp(self):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.driver = webdriver.Chrome(options=self._options)
                self.page = CalculatorPage(self.driver).open()
                return
            except TimeoutException:
                if attempt < max_retries - 1:
                    self.driver.quit()
                    time.sleep(2)
                else:
                    raise

    def tearDown(self):
        self.driver.quit()

    def test_addition(self):
        self.assertEqual(self.page.calculate(2, 3, "+"), "5")

    def test_subtraction(self):
        self.assertEqual(self.page.calculate(10, 4, "-"), "6")

    def test_multiplication(self):
        self.assertEqual(self.page.calculate(6, 7, "*"), "42")

    def test_division(self):
        self.assertEqual(self.page.calculate(9, 3, "/"), "3")
   
    def test_power_operation(self):
        self.assertEqual(self.page.calculate(2, 10, "**"), "1024")

    def test_boundary_values(self):
        self.assertEqual(self.page.calculate(100, 0, "*"), "0")
        self.assertEqual(self.page.calculate(-5, 3, "+"), "-2")
        self.assertEqual(self.page.calculate(999, 1, "+"), "1000")

    def test_division_by_zero(self):
        result = self.page.calculate(10, 0, "/")
        self.assertIn("null", result)


if __name__ == "__main__":
    unittest.main()