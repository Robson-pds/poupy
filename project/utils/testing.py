import time

from django.test.selenium import LiveServerTestCase
from pytest import mark
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from project.utils.browser import make_chrome_browser


@mark.functional_test
class FunctionalTestBase(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()  # Is necessary to quit the browser to avoid memory leak
        return super().tearDown()

    @staticmethod
    def sleep(seconds: int = 1) -> None:
        """
        Method to sleep the browser for a while.
        Args:
            seconds: seconds to sleep the browser

        Returns:
            None
        """
        time.sleep(seconds)

    def get_content(self, html_tag_name: str, url: str = ''):
        """
        Method to get the content of an HTML tag.
        Args:
            html_tag_name: HTML tag name to get the content
            url: URL to get the content

        Returns:
            content of an HTML tag
        """
        self.browser.get(self.live_server_url + url)
        return self.browser.find_element(By.TAG_NAME, html_tag_name)

    def login(self, username: str, password: str) -> None:
        """
        Method to login user.
        Args:
            username: username of the user to login
            password: password of the user to login
        """
        self.browser.get(self.live_server_url + '/app/')
        # Input username
        username_input = self.browser.find_element(
            By.XPATH, '//input[@placeholder="Enter your username"]'
        )
        username_input.send_keys(username)
        username_input.send_keys(Keys.TAB)

        # Input password
        password_input = self.browser.find_element(
            By.XPATH, '//input[@placeholder="Enter your password"]'
        )
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

    def user_register(
        self,
        first_name: str = 'Tester',
        last_name: str = 'Last',
        username: str = 'test',
        email: str = 'test@email.com',
        password: str = 'Test@123',
    ) -> dict[str, str]:
        """
        Method to register user for functional tests.
        Args:
            first_name: fist name of the user to register
            last_name: last name of the user to register
            username: username of the user to register
            email: email of the user to register
            password: password of the user to register

        Returns:
            dict with username and password of the user
        """
        # User open page
        self.browser.get(self.live_server_url + '/app/signup/')

        inputs = [
            ['Enter your first name', first_name],
            ['Enter your last name', last_name],
            ['Enter a username', username],
            ['Enter your best email', email],
            ['Enter a secure password', password],
            ['Enter your password again', password],
        ]

        for item in inputs:
            # You see an input field with the text "Enter your first name"
            signup_inputs = self.browser.find_element(
                By.XPATH, f'//input[@placeholder="{item[0]}"]'
            )
            # Input first name
            signup_inputs.send_keys(item[1])
            # Go to next input
            signup_inputs.send_keys(Keys.TAB)

            # Verify if is last repeat and press enter
            if item[0] == inputs[5][0]:
                signup_inputs.send_keys(Keys.ENTER)

        return {'password': password, 'username': username}
