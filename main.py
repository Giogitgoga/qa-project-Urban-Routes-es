import time
import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

def retrieve_phone_code(driver) -> str:
    import json
    from selenium.common import WebDriverException

    all_logs = []

    for _ in range(10):
        try:
            all_logs.extend(driver.get_log('performance'))
            matching_logs = [
                log["message"] for log in all_logs
                if log.get("message") and 'api/v1/number?number' in log.get("message")
            ]

            for log in reversed(matching_logs):
                message_data = json.loads(log)["message"]
                params = message_data.get("params", {})
                request_id = params.get("requestId")

                if request_id:
                    body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
                    code = ''.join([x for x in body['body'] if x.isdigit()])
                    if code:
                        return code
        except WebDriverException:
            pass
        time.sleep(1)

    raise Exception("No se encontró el código de confirmación del teléfono.")

class UrbanRoutesPage:
    # Localizadores principales
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    request_taxi_button = (By.XPATH, "//button[contains(text(), 'Pedir un taxi')]")

    # Tarifa Comfort
    comfort_tariff_card = (By.XPATH, "//div[contains(@class, 'tarriff-card')]//div[text()='Comfort'] | //div[contains(text(), 'Comfort')]/ancestor::div[contains(@class, 'tarriff-card')]")

    # Teléfono (Usando CSS_SELECTOR como solicitó el revisor)
    phone_number_button = (By.CSS_SELECTOR, '.np-text')
    phone_input_field = (By.ID, 'phone')
    next_phone_button = (By.XPATH, "//button[text()='Siguiente']")
    sms_code_field = (By.ID, 'code')
    confirm_phone_button = (By.XPATH, "//button[text()='Confirmar']")

    # Tarjeta de Crédito (Usando CSS_SELECTOR)
    payment_method_button = (By.CSS_SELECTOR, '.pp-text')
    add_card_button = (By.CLASS_NAME, 'pp-plus-container')
    card_number_field = (By.ID, 'number')
    card_code_field = (By.XPATH, "//div[@class='card-code-input']//input[@id='code']")
    link_card_button = (By.XPATH, "//button[text()='Agregar']")
    close_payment_modal_button = (By.XPATH, "//div[@class='payment-picker open']//button[contains(@class, 'close-button')]")

    # Requisitos Adicionales
    driver_message_field = (By.ID, 'comment')
    blanket_switch = (By.XPATH, "//div[contains(text(), 'Manta y pañuelos')]/following-sibling::div//span[contains(@class, 'slider')]")
    blanket_input = (By.XPATH, "//div[contains(text(), 'Manta y pañuelos')]/following-sibling::div//input")
    ice_cream_plus_button = (By.XPATH, "//div[contains(text(), 'Helado')]/following-sibling::div//div[contains(@class, 'counter-plus')]")
    ice_cream_counter_value = (By.XPATH, "//div[contains(text(), 'Helado')]/following-sibling::div//div[contains(@class, 'counter-value')]")

    # Pedir taxi (Usando CSS_SELECTOR)
    order_taxi_button = (By.CSS_SELECTOR, '.smart-button-main')
    order_search_modal = (By.CLASS_NAME, 'order-body')
    driver_info_modal = (By.XPATH, "//div[contains(@class, 'order-header') or contains(@class, 'order-number') or contains(@class, 'order-sub-header')]")

    def __init__(self, driver):
        self.driver = driver

    def _scroll_to(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    # --- Acciones (Setters / Clicks) ---

    def set_from(self, from_address):
        elem = WebDriverWait(self.driver, 15).until(
            expected_conditions.presence_of_element_located(self.from_field)
        )
        self._scroll_to(elem)
        elem.clear()
        elem.send_keys(from_address)

    def set_to(self, to_address):
        elem = WebDriverWait(self.driver, 15).until(
            expected_conditions.presence_of_element_located(self.to_field)
        )
        self._scroll_to(elem)
        elem.clear()
        elem.send_keys(to_address)

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)
        
        # Clic en "Pedir un taxi"
        elem = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.request_taxi_button)
        )
        self._scroll_to(elem)
        elem.click()

    def select_comfort_tariff(self):
        elem = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.comfort_tariff_card)
        )
        self._scroll_to(elem)
        elem.click()

    def fill_phone_flow(self, phone, code_retriever_func):
        phone_btn = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.phone_number_button)
        )
        self._scroll_to(phone_btn)
        phone_btn.click()

        phone_input = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.phone_input_field)
        )
        phone_input.clear()
        phone_input.send_keys(phone)
        time.sleep(1)

        phone_input.send_keys(Keys.ENTER)

        try:
            next_btn = WebDriverWait(self.driver, 2).until(
                expected_conditions.element_to_be_clickable(self.next_phone_button)
            )
            next_btn.click()
        except Exception:
            pass

        time.sleep(2)
        code = code_retriever_func(self.driver)

        sms_input = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.sms_code_field)
        )
        sms_input.clear()
        sms_input.send_keys(code)

        confirm_btn = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.confirm_phone_button)
        )
        confirm_btn.click()

    def add_credit_card_flow(self, card_number, card_code):
        pay_btn = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.payment_method_button)
        )
        self._scroll_to(pay_btn)
        pay_btn.click()

        add_card_btn = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.add_card_button)
        )
        add_card_btn.click()

        card_num_elem = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.card_number_field)
        )
        card_num_elem.send_keys(card_number)
        time.sleep(1)

        card_code_elem = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.card_code_field)
        )
        card_code_elem.send_keys(card_code)

        card_code_elem.send_keys(Keys.TAB)
        self.driver.execute_script("arguments[0].blur();", card_code_elem)
        time.sleep(1)

        link_btn = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.link_card_button)
        )
        link_btn.click()

        close_btn = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.close_payment_modal_button)
        )
        close_btn.click()

    def set_driver_message(self, message):
        elem = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.driver_message_field)
        )
        self._scroll_to(elem)
        elem.send_keys(message)

    def toggle_blanket_and_tissues(self):
        elem = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.blanket_switch)
        )
        self._scroll_to(elem)
        elem.click()

    def add_ice_cream(self, count):
        btn = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.ice_cream_plus_button)
        )
        self._scroll_to(btn)
        for _ in range(count):
            btn.click()

    def click_order_taxi(self):
        elem = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.order_taxi_button)
        )
        self._scroll_to(elem)
        elem.click()

    # --- Consultas (Getters para las validaciones POM) ---

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def get_comfort_tariff_class(self):
        # Retorna el atributo class para confirmar que dice 'active'
        elem = WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located(self.comfort_tariff_card)
        )
        return elem.get_attribute('class')

    def get_phone_number_text(self):
        # Espera que el texto cambie y se actualice al número
        WebDriverWait(self.driver, 10).until(
            expected_conditions.text_to_be_present_in_element(self.phone_number_button, data.phone_number)
        )
        return self.driver.find_element(*self.phone_number_button).text

    def get_payment_method_text(self):
        # Espera a que el texto cambie a "Tarjeta"
        WebDriverWait(self.driver, 10).until(
            expected_conditions.text_to_be_present_in_element(self.payment_method_button, "Tarjeta")
        )
        return self.driver.find_element(*self.payment_method_button).text

    def get_driver_message(self):
        return self.driver.find_element(*self.driver_message_field).get_property('value')

    def is_blanket_checked(self):
        return self.driver.find_element(*self.blanket_input).is_selected()

    def get_ice_cream_count(self):
        return self.driver.find_element(*self.ice_cream_counter_value).text

    def is_order_modal_displayed(self):
        modal = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.order_search_modal)
        )
        return modal.is_displayed()

    def is_driver_info_displayed(self):
        driver_info = WebDriverWait(self.driver, 60).until(
            expected_conditions.visibility_of_element_located(self.driver_info_modal)
        )
        return driver_info.is_displayed()


class TestUrbanRoutes:
    driver = None

    # Cambiamos setup_class a setup_method para que CADA prueba abra un navegador limpio
    def setup_method(self):
        options = webdriver.ChromeOptions()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.driver.get(data.urban_routes_url)

    # Cerramos el navegador al final de cada prueba
    def teardown_method(self):
        if self.driver:
            self.driver.quit()

    def test_set_route(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to

    def test_select_comfort(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.select_comfort_tariff()
        
        assert 'active' in routes_page.get_comfort_tariff_class()

    def test_fill_phone(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.select_comfort_tariff()
        routes_page.fill_phone_flow(data.phone_number, retrieve_phone_code)
        
        assert routes_page.get_phone_number_text() == data.phone_number

    def test_add_credit_card(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.select_comfort_tariff()
        routes_page.fill_phone_flow(data.phone_number, retrieve_phone_code)
        routes_page.add_credit_card_flow(data.card_number, data.card_code)
        
        assert "Tarjeta" in routes_page.get_payment_method_text()

    def test_set_driver_message(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.select_comfort_tariff()
        routes_page.fill_phone_flow(data.phone_number, retrieve_phone_code)
        routes_page.set_driver_message(data.message_for_driver)
        
        assert routes_page.get_driver_message() == data.message_for_driver

    def test_toggle_blanket_and_tissues(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.select_comfort_tariff()
        routes_page.fill_phone_flow(data.phone_number, retrieve_phone_code)
        routes_page.toggle_blanket_and_tissues()
        
        assert routes_page.is_blanket_checked() is True

    def test_add_ice_cream(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.select_comfort_tariff()
        routes_page.fill_phone_flow(data.phone_number, retrieve_phone_code)
        routes_page.add_ice_cream(2)
        
        assert routes_page.get_ice_cream_count() == '2'

    def test_order_taxi_and_wait_for_driver(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.select_comfort_tariff()
        routes_page.fill_phone_flow(data.phone_number, retrieve_phone_code)
        routes_page.add_credit_card_flow(data.card_number, data.card_code)
        routes_page.set_driver_message(data.message_for_driver)
        routes_page.toggle_blanket_and_tissues()
        routes_page.add_ice_cream(2)
        routes_page.click_order_taxi()
        
        assert routes_page.is_order_modal_displayed() is True
        assert routes_page.is_driver_info_displayed() is True
