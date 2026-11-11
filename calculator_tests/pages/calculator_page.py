from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CalculatorPage:
    """Page Object для Simple Calculator"""
    
    URL = "https://www.globalsqa.com/angularJs-protractor/SimpleCalculator/"
    
    _INPUT_FIRST = (By.CSS_SELECTOR, "input[ng-model='first']")
    _INPUT_SECOND = (By.CSS_SELECTOR, "input[ng-model='second']")
    _SELECT_OPERATOR = (By.CSS_SELECTOR, "select[ng-model='operator']")
    _BTN_GO = (By.CSS_SELECTOR, "button[ng-click='doAddition()']")
    _RESULT_SPAN = (By.CSS_SELECTOR, "span.ng-binding")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        """Открывает страницу калькулятора"""
        self.driver.get(self.URL)
        return self

    def enter_first_number(self, num: str):
        """Вводит первое число"""
        el = self.wait.until(EC.presence_of_element_located(self._INPUT_FIRST))
        el.clear()
        el.send_keys(num)
        return self

    def enter_second_number(self, num: str):
        """Вводит второе число"""
        el = self.wait.until(EC.presence_of_element_located(self._INPUT_SECOND))
        el.clear()
        el.send_keys(num)
        return self

    def select_operation(self, operation: str):
        """Выбирает операцию из выпадающего списка (+, -, *, /, **)"""
        from selenium.webdriver.support.ui import Select
        el = self.wait.until(EC.presence_of_element_located(self._SELECT_OPERATOR))
        Select(el).select_by_visible_text(operation)
        return self

    def click_go(self):
        """Нажимает кнопку Go"""
        btn = self.wait.until(EC.element_to_be_clickable(self._BTN_GO))
        btn.click()
        return self

    def get_result(self) -> str:
        """Получает текст результата"""
        el = self.wait.until(EC.visibility_of_element_located(self._RESULT_SPAN))
        return el.text.strip()