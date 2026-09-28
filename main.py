import data
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages import UrbanRoutesPage
from helpers import retrieve_phone_code


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.maximize_window()

    def test_1_set_route(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)
        page.set_from(data.address_from)
        page.set_to(data.address_to)
        assert page.driver.find_element(*page.from_field).get_attribute('value') == data.address_from
        assert page.driver.find_element(*page.to_field).get_attribute('value') == data.address_to

    def test_2_select_comfort_tariff(self):
        page = UrbanRoutesPage(self.driver)
        page.click_request_taxi()
        page.select_comfort_tariff()

    def test_3_fill_phone_number(self):
        page = UrbanRoutesPage(self.driver)
        page.click_phone_number_button()
        page.set_phone_number(data.phone_number)
        page.click_next_phone_button()
        code = retrieve_phone_code(self.driver)
        page.set_sms_code(code)
        page.click_confirm_phone_button()

    def test_4_fill_credit_card_data(self):
        page = UrbanRoutesPage(self.driver)
        page.click_payment_method_button()
        page.click_add_card_button()
        page.set_card_number(data.card_number)
        page.set_card_code(data.card_code)

    def test_5_link_and_confirm_card(self):
        page = UrbanRoutesPage(self.driver)
        page.click_link_card_button()
        page.select_added_card()
        page.click_close_payment_modal()

    def test_6_set_driver_message(self):
        page = UrbanRoutesPage(self.driver)
        page.set_driver_message(data.message_for_driver)

    def test_7_toggle_blanket_and_tissues(self):
        page = UrbanRoutesPage(self.driver)
        page.toggle_blanket_and_tissues()

    def test_8_add_ice_cream(self):
        page = UrbanRoutesPage(self.driver)
        page.add_ice_cream(2)

    def test_9_order_taxi_modal(self):
        page = UrbanRoutesPage(self.driver)
        page.click_order_taxi_button()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(page.order_modal)
        )

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()