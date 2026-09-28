from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class UrbanRoutesPage:
    # Localizadores principales
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    request_taxi_button = (By.XPATH, '//button[contains(text(), "Pedir un taxi")]')

    # Tarifa Comfort (localizador directo y robusto)
    comfort_tariff_button = (By.XPATH, '//div[text()="Comfort"]')

    # Teléfono
    phone_number_button = (By.CLASS_NAME, 'np-text')
    phone_input = (By.ID, 'phone')
    next_phone_button = (By.XPATH, '//button[contains(text(), "Siguiente")]')
    sms_code_input = (By.ID, 'code')
    confirm_phone_button = (By.XPATH, '//button[contains(text(), "Confirmar")]')

    # Método de Pago
    payment_method_button = (By.CLASS_NAME, 'pp-button')
    add_card_button = (By.XPATH, '//div[contains(text(), "Agregar tarjeta")]')
    card_number_input = (By.ID, 'number')
    card_code_input = (By.XPATH, '//div[@class="card-code-input"]//input[@id="code"]')

    # Botón enlazar/agregar tarjeta (soporta ambos textos posibles)
    link_card_button = (By.XPATH,
                        '//div[contains(@class, "modal")]//button[contains(text(), "Agregar") or contains(text(), "Enlazar")]')
    added_card_option = (By.XPATH, '//div[contains(@class, "pp-title") and contains(text(), "Tarjeta")]')

    # Botón de cierre de la sección activa del modal de pago
    close_payment_modal_button = (By.CSS_SELECTOR, '.payment-picker .section.active .close-button')

    # Requisitos adicionales y Pedido
    driver_comment_input = (By.ID, 'comment')
    blanket_tissues_switch = (By.XPATH,
                              '//div[contains(text(), "Manta y pañuelos")]/following-sibling::div//span[contains(@class, "slider")]')
    ice_cream_plus_button = (By.XPATH,
                             '//div[contains(text(), "Helado")]/following-sibling::div//div[contains(@class, "counter-plus")]')
    order_taxi_button = (By.CLASS_NAME, 'smart-button')
    order_modal = (By.CLASS_NAME, 'order-body')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, address):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.from_field)).send_keys(address)

    def set_to(self, address):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.to_field)).send_keys(address)

    def click_request_taxi(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.request_taxi_button)).click()

    def select_comfort_tariff(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.comfort_tariff_button)).click()

    def click_phone_number_button(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.phone_number_button)).click()

    def set_phone_number(self, phone):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.phone_input)).send_keys(phone)

    def click_next_phone_button(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.next_phone_button)).click()

    def set_sms_code(self, code):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.sms_code_input)).send_keys(code)

    def click_confirm_phone_button(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.confirm_phone_button)).click()

    def click_payment_method_button(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.payment_method_button)).click()

    def click_add_card_button(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.add_card_button)).click()

    def set_card_number(self, card_number):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.card_number_input)).send_keys(
            card_number)

    def set_card_code(self, card_code):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.card_code_input))
        element.send_keys(card_code)
        element.send_keys(Keys.TAB)

    def click_link_card_button(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.link_card_button)).click()

    def select_added_card(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.added_card_option)).click()

    def click_close_payment_modal(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.close_payment_modal_button)).click()

    def set_driver_message(self, message):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.driver_comment_input)).send_keys(
            message)

    def toggle_blanket_and_tissues(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.blanket_tissues_switch)).click()

    def add_ice_cream(self, count=2):
        for _ in range(count):
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.ice_cream_plus_button)).click()

    def click_order_taxi_button(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.order_taxi_button)).click()