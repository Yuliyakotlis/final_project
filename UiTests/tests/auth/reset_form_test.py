import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from support.app_config import BASE_URL


def go_to_reset_form():
    pytest.driver.find_element(By.ID, 'forgot_password').click()
    WebDriverWait(pytest.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'reset-form')))


def on_tab_phone():
    pytest.driver.find_element(By.ID, 't-btn-tab-phone').click()
    pytest.driver.find_element(By.XPATH, ".//input[@name='tab_type' and @value='phone']")


def on_tab_email():
    pytest.driver.find_element(By.ID, 't-btn-tab-mail').click()
    pytest.driver.find_element(By.XPATH, ".//input[@name='tab_type' and @value='mail']")


def on_tab_login():
    pytest.driver.find_element(By.ID, 't-btn-tab-login').click()
    pytest.driver.find_element(By.XPATH, ".//input[@name='tab_type' and @value='login']")


def on_tab_personal_acc():
    pytest.driver.find_element(By.ID, 't-btn-tab-ls').click()
    pytest.driver.find_element(By.XPATH, ".//input[@name='tab_type' and @value='ls']")


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome()
    pytest.driver.implicitly_wait(10)
    # Переходим на страницу авторизации
    pytest.driver.get(BASE_URL)
    go_to_reset_form()
    yield
    pytest.driver.quit()


@pytest.mark.skip(reason="Для восстановления аккаунта с помощью телефона нужно вводить капчу")
def test_reset_by_phone():
    """Проверка, что можно восстановить аккаунт по номеру телефона"""
    #Тут должен быть номер телефона существующего пользователя
    on_tab_phone()
    pytest.driver.find_element(By.ID, 'username').send_keys("77777777777")
    #Капчу не угадать
    pytest.driver.find_element(By.ID, 'captcha').send_keys("123")
    pytest.driver.find_element(By.ID, 'reset').click()
    WebDriverWait(pytest.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'reset-confirm-form')))


@pytest.mark.skip(reason="Для восстановления аккаунта с помощью почты нужно вводить капчу")
def test_reset_by_email():
    """Проверка, что можно восстановить аккаунт по емейл"""
    on_tab_email()
    pytest.driver.find_element(By.ID, 'username').send_keys("xemaden793@bitvoo.com")
    #Капчу не угадать
    pytest.driver.find_element(By.ID, 'captcha').send_keys("123")
    pytest.driver.find_element(By.ID, 'reset').click()
    WebDriverWait(pytest.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'reset-confirm-form')))


@pytest.mark.skip(reason="Для восстановления аккаунта с помощью логина нужно вводить капчу")
def test_reset_by_phone():
    """Проверка, что можно восстановить аккаунт по логину"""
    on_tab_login()
    pytest.driver.find_element(By.ID, 'username').send_keys("xemaden793@bitvoo.com")
    #Капчу не угадать
    pytest.driver.find_element(By.ID, 'captcha').send_keys("123")
    pytest.driver.find_element(By.ID, 'reset').click()
    WebDriverWait(pytest.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'reset-confirm-form')))


@pytest.mark.skip(reason="Для восстановления аккаунта с помощью лицевого счета нужно вводить капчу")
def test_reset_by_phone():
    """Проверка, что можно восстановить аккаунт с помощью лицевого счета"""
    #Тут должен быть номер телефона существующего пользователя
    on_tab_personal_acc()
    pytest.driver.find_element(By.ID, 'username').send_keys('123456789000')
    #Капчу не угадать
    pytest.driver.find_element(By.ID, 'captcha').send_keys("123")
    pytest.driver.find_element(By.ID, 'reset').click()
    WebDriverWait(pytest.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'reset-confirm-form')))


def test_reset_support_widget_works():
    """Проверка, что виджет чата с тех подержкой доступен"""
    pytest.driver.find_element(By.ID, 'widget_bar').click()
    pytest.driver.find_element(By.ID, 'full-name').send_keys("Тест")
    pytest.driver.find_element(By.ID, 'phone').send_keys("77777777777")
    pytest.driver.find_element(By.ID, 'widget_sendPrechat').click()
    chat_into_text = pytest.driver.find_element(By.XPATH, ".//div[contains(@class,'title-from-skill-group')]").text
    assert chat_into_text == "Здравствуйте! Мы с удовольствием ответим на интересующие Вас вопросы"


def test_reset_can_switch_fields_types():
    """Можно переключать тип поля для восстановления пароля"""
    on_tab_phone()
    on_tab_email()
    on_tab_login()
    on_tab_personal_acc()



def test_reset_support_phone_number_exist():
    """Проверка, что на странице указан верный номер тех поддержки"""
    sup_phone = pytest.driver.find_element(By.XPATH, ".//a[contains(@class, 'support-phone')]").text
    assert sup_phone.replace(" ", "") == '88001000800'


def test_reset_has_captcha_image_by_phone():
    """Проверка, что на странице восстановления по номеру телефона есть капча"""
    on_tab_phone()
    captcha_src = pytest.driver.find_element(By.XPATH, ".//img[@class='rt-captcha__image']").get_attribute("src")
    assert captcha_src != ""


def test_reset_has_captcha_image_by_email():
    """Проверка, что на странице восстановления по почте есть капча"""
    on_tab_email()
    captcha_src = pytest.driver.find_element(By.XPATH, ".//img[@class='rt-captcha__image']").get_attribute("src")
    assert captcha_src != ""


def test_reset_has_captcha_image_by_login():
    """Проверка, что на странице восстановления по логину есть капча"""
    on_tab_login()
    captcha_src = pytest.driver.find_element(By.XPATH, ".//img[@class='rt-captcha__image']").get_attribute("src")
    assert captcha_src != ""


def test_reset_has_captcha_image_by_personal_account():
    """Проверка, что на странице восстановления по лицевому счету есть капча"""
    on_tab_personal_acc()
    captcha_src = pytest.driver.find_element(By.XPATH, ".//img[@class='rt-captcha__image']").get_attribute("src")
    assert captcha_src != ""


def test_reset_can_go_back_to_auth():
    """Проверка, что со страницы восстановления можно вернуться на страницу авторизации"""
    pytest.driver.find_element(By.ID, 'reset-back').click()
    WebDriverWait(pytest.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'login-form')))


def test_reset_bad_if_not_filled_phone():
    """Проверка, что нельзя восстановить аккаунт без заполнения полей. Телефон + капча"""
    on_tab_phone()
    pytest.driver.find_element(By.ID, 'reset').click()
    pytest.driver.find_element(By.XPATH, ".//span[contains(@class,'meta--error')]")
    pytest.driver.find_element(By.CLASS_NAME, 'reset-form')


def test_reset_bad_if_not_filled_email():
    """Проверка, что нельзя восстановить аккаунт без заполнения полей. Почта + капча"""
    on_tab_email()
    pytest.driver.find_element(By.ID, 'reset').click()
    pytest.driver.find_element(By.XPATH, ".//span[contains(@class,'meta--error')]")
    pytest.driver.find_element(By.CLASS_NAME, 'reset-form')


def test_reset_bad_if_not_filled_login():
    """Проверка, что нельзя восстановить аккаунт без заполнения полей. Логин + капча"""
    on_tab_login()
    pytest.driver.find_element(By.ID, 'reset').click()
    pytest.driver.find_element(By.XPATH, ".//span[contains(@class,'meta--error')]")
    pytest.driver.find_element(By.CLASS_NAME, 'reset-form')


def test_reset_bad_if_not_filled_personal_account():
    """Проверка, что нельзя восстановить аккаунт без заполнения полей. Лицевой счет + капча"""
    on_tab_personal_acc()
    pytest.driver.find_element(By.ID, 'reset').click()
    pytest.driver.find_element(By.XPATH, ".//span[contains(@class,'meta--error')]")
    pytest.driver.find_element(By.CLASS_NAME, 'reset-form')

