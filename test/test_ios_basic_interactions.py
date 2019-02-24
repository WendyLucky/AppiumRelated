import pytest
import os

from appium import webdriver
from helpers import take_screenhot_and_syslog, IOS_APP_PATH, EXECUTOR


class TestIOSBasicInteractions():

    @pytest.fixture(scope='function')
    def driver(self, request, device_logger):
        calling_request = request._pyfuncitem.name
        driver = webdriver.Remote(
            command_executor=EXECUTOR,
            desired_capabilities={
                'app': IOS_APP_PATH,
                'platformName': 'iOS',
                'automationName': 'XCUITest',
                'platformVersion': os.getenv('IOS_PLATFORM_VERSION') or '12.1',
                'deviceName': os.getenv('IOS_DEVICE_NAME') or 'iPhone XR',
            }
        )

        def fin():
            take_screenhot_and_syslog(driver, device_logger, calling_request)
            driver.quit()

        request.addfinalizer(fin)

        driver.implicitly_wait(10)
        return driver

    #test key input, click button and compute result
    def test_compute(self, driver):
        
        #type in "12" in the first text input
        text_field_el = driver.find_element_by_id('TextField1')
        assert text_field_el.get_attribute('value') is None
        text_field_el.send_keys('12')
        assert text_field_el.get_attribute('value') == '12'
        #type in "34" in the second text input
        text_field_e2 = driver.find_element_by_id('TextField2')
        assert text_field_e2.get_attribute('value') is None
        text_field_e2.send_keys('34')
        assert text_field_e2.get_attribute('value') == '34'
        #click "Compute Sum" button
        button_element_id = 'Compute Sum'
        button_element = driver.find_element_by_id(button_element_id)
        button_element.click()
        #check if the sum result is correct
        result_element_id = 'Answer'
        result_element = driver.find_element_by_id(result_element_id);
        assert result_element.get_attribute('value') == '46';
    
    #test alert dialog
    def test_alert(self, driver):
        #triger an alert
        button_element_id = 'show alert'
        button_element = driver.find_element_by_id(button_element_id)
        button_element.click()
        #check the alert dialog and info
        alert_content_element_id = 'this alert is so cool.'
        alert_content_element = driver.find_element_by_id(alert_content_element_id)
        alert_title = alert_content_element.get_attribute('name')
        assert alert_title == 'this alert is so cool.'
