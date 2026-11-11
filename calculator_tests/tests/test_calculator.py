import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pages.calculator_page import CalculatorPage


class TestCalculator(unittest.TestCase):
    
    def setUp(self):
        """Инициализация браузера перед каждым тестом"""
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        self.page = CalculatorPage(self.driver).open()

    def tearDown(self):
        """Закрытие браузера после каждого теста"""
        self.driver.quit()

    def test_addition(self):
        self.page.enter_first_number("10").enter_second_number("5").select_operation("+").click_go()
        self.assertEqual(self.page.get_result(), "15")

    def test_subtraction(self):
        self.page.enter_first_number("20").enter_second_number("8").select_operation("-").click_go()
        self.assertEqual(self.page.get_result(), "12")

    def test_multiplication(self):
        self.page.enter_first_number("6").enter_second_number("7").select_operation("*").click_go()
        self.assertEqual(self.page.get_result(), "42")

    def test_division(self):
        self.page.enter_first_number("15").enter_second_number("3").select_operation("/").click_go()
        self.assertEqual(self.page.get_result(), "5")

    def test_power(self):
        self.page.enter_first_number("2").enter_second_number("10").select_operation("**").click_go()
        self.assertEqual(self.page.get_result(), "1024")

    def test_division_by_zero(self):
        """Проверка обработки деления на ноль"""
        self.page.enter_first_number("10").enter_second_number("0").select_operation("/").click_go()
        result = self.page.get_result()
        self.assertIn("Infinity", result)

    def test_negative_numbers(self):
        self.page.enter_first_number("-5").enter_second_number("3").select_operation("+").click_go()
        self.assertEqual(self.page.get_result(), "-2")