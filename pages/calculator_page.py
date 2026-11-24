import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import URL

class CalculatorPage():
    url = URL

    _INPUT_A = (By.CSS_SELECTOR, "input[ng-model='a']")
    _INPUT_B = (By.CSS_SELECTOR, "input[ng-model='b']")
    _OPERATION = (By.CSS_SELECTOR, "select[ng-model='operation']")
    _RESULT = (By.CSS_SELECTOR, "b.result")
    _INC_A = (By.CSS_SELECTOR, "button[ng-click='inca()']")
    _DEC_A = (By.CSS_SELECTOR, "button[ng-click='deca()']")
    _INC_B = (By.CSS_SELECTOR, "button[ng-click='incb()']")
    _DEC_B = (By.CSS_SELECTOR, "button[ng-click='decb()']")
    _RESULT_RE = re.compile(r"^\s*(.+?)\s*=\s*(.+?)\s*$")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        self.driver.get(self.url)
        self.wait.until(EC.visibility_of_element_located(self._INPUT_A))
        return self

    def enter_a(self, value):
        field = self.wait.until(EC.element_to_be_clickable(self._INPUT_A))
        field.clear()
        field.send_keys(str(value))
        return self

    def enter_b(self, value):
        field = self.wait.until(EC.element_to_be_clickable(self._INPUT_B))
        field.clear()
        field.send_keys(str(value))
        return self

    def increment_a(self):
        self.wait.until(EC.element_to_be_clickable(self._INC_A)).click()
        return self

    def decrement_a(self):
        self.wait.until(EC.element_to_be_clickable(self._DEC_A)).click()
        return self

    def increment_b(self):
        self.wait.until(EC.element_to_be_clickable(self._INC_B)).click()
        return self

    def decrement_b(self):
        self.wait.until(EC.element_to_be_clickable(self._DEC_B)).click()
        return self

    def select_operation(self, operation):
        if operation not in {"+", "-", "*", "/", "**"}:
            raise ValueError(f"Недопустимая операция: {operation!r}")
        select = Select(self.wait.until(EC.element_to_be_clickable(self._OPERATION)))
        select.select_by_value(operation)
        return self

    def get_result_text(self):
        element = self.wait.until(EC.visibility_of_element_located(self._RESULT))
        return element.text.strip()

    def get_result_value(self):
        text = self.get_result_text()
        match = self._RESULT_RE.match(text)
        if not match:
            raise AssertionError(f"Invalid parsing string: {text!r}")
        return match.group(2)

    def calculate(self, a, b, operation):
        self.enter_a(a)
        self.enter_b(b)
        self.select_operation(operation)
        return self.get_result_value()