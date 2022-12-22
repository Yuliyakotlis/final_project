import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from support.app_config import BASE_URL


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
    yield
    pytest.driver.quit()


@pytest.mark.skip(reason="По номеру не зарегистрироваться, смс не приходит")
def test_auth_ok_by_phone():
    """Базовая проверка авторизации существующим пользователем с помощью номера телефона + пароля"""
    on_tab_phone()
    # Тут должен быть номер сущ. пользователя
    pytest.driver.find_element(By.ID, 'username').send_keys('+77777777777')
    pytest.driver.find_element(By.ID, 'password').send_keys('Axemaden793')
    pytest.driver.find_element(By.NAME, 'login').click()

    WebDriverWait(pytest.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'home-container')))


def test_auth_ok_by_email():
    """Базовая проверка авторизации существующим пользователем с помощью почты + пароля"""
    on_tab_email()
    pytest.driver.find_element(By.ID, 'username').send_keys('xemaden793@bitvoo.com')
    pytest.driver.find_element(By.ID, 'password').send_keys('Axemaden793')
    pytest.driver.find_element(By.NAME, 'login').click()

    WebDriverWait(pytest.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'home-container')))


def test_auth_ok_by_login():
    """Базовая проверка авторизации существующим пользователем с помощью логина + пароля"""
    on_tab_login()
    pytest.driver.find_element(By.ID, 'username').send_keys('xemaden793@bitvoo.com')
    pytest.driver.find_element(By.ID, 'password').send_keys('Axemaden793')
    pytest.driver.find_element(By.NAME, 'login').click()

    WebDriverWait(pytest.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'home-container')))


@pytest.mark.skip(reason="Нет лицевого счета для проверки")
def test_auth_ok_by_personal_account():
    """Базовая проверка авторизации существующим пользователем с помощью лицевого счета + пароля"""
    on_tab_personal_acc()
    # Тут должен быть лицевой счет сущ. пользователя
    pytest.driver.find_element(By.ID, 'username').send_keys('123456789000')
    pytest.driver.find_element(By.ID, 'password').send_keys('Axemaden793')
    pytest.driver.find_element(By.NAME, 'login').click()

    WebDriverWait(pytest.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'home-container')))


def test_auth_can_switch_login_types():
    """Можно переключать тип поля для авторизации"""
    on_tab_phone()
    on_tab_email()
    on_tab_login()
    on_tab_personal_acc()


def test_auth_social_providers_exist():
    """Проверка, что есть кнопки входа через соц. сети"""
    pytest.driver.find_element(By.ID, 'oidc_vk')
    pytest.driver.find_element(By.ID, 'oidc_ok')
    pytest.driver.find_element(By.ID, 'oidc_mail')
    pytest.driver.find_element(By.ID, 'oidc_google')
    pytest.driver.find_element(By.ID, 'oidc_ya')


def test_auth_support_widget_works():
    """Проверка, что виджет чата с тех подержкой доступен"""
    pytest.driver.find_element(By.ID, 'widget_bar').click()
    pytest.driver.find_element(By.ID, 'full-name').send_keys("Тест")
    pytest.driver.find_element(By.ID, 'phone').send_keys("77777777777")
    pytest.driver.find_element(By.ID, 'widget_sendPrechat').click()
    chat_into_text = pytest.driver.find_element(By.XPATH, ".//div[contains(@class,'title-from-skill-group')]").text
    assert chat_into_text == "Здравствуйте! Мы с удовольствием ответим на интересующие Вас вопросы"


def test_auth_support_phone_number_exist():
    """Проверка, что на странице указан верный номер тех поддержки"""
    sup_phone = pytest.driver.find_element(By.XPATH, ".//a[contains(@class, 'support-phone')]").text
    assert sup_phone.replace(" ", "") == '88001000800'


def test_auth_user_agreement_href_not_empty():
    """Проверка, что href пользовательского соглашения не пустая"""
    agreement_href = pytest.driver.find_element(By.XPATH, ".//div[@class='auth-policy']/a").get_attribute("href")
    assert agreement_href != ""


def test_auth_by_phone_at_startup():
    """Проверка, что по умолчанию выбрана форма авторизации по телефону"""
    pytest.driver.find_element(By.XPATH, ".//input[@name='tab_type' and @value='phone']")

