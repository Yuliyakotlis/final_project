import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from support.app_config import BASE_URL
from support.full_reg_info import FullRegInfo
from support.generator import *


def on_tab_register():
    pytest.driver.find_element(By.ID, 'kc-register').click()
    WebDriverWait(pytest.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'register-form')))


def ui_fill_reg_info(reg_info: FullRegInfo):
    pytest.driver.find_element(By.NAME, 'firstName').send_keys(reg_info.first_name)
    pytest.driver.find_element(By.NAME, 'lastName').send_keys(reg_info.last_name)
    pytest.driver.find_element(By.ID,   'address').send_keys(reg_info.address)
    pytest.driver.find_element(By.ID,   'password').send_keys(reg_info.password)
    pytest.driver.find_element(By.ID,   'password-confirm').send_keys(reg_info.password_confirm)


def ui_exp_reg_confirm():
    WebDriverWait(pytest.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'register-confirm-form')))


def ui_exp_reg_error():
    pytest.driver.find_element(By.XPATH, ".//span[contains(@class,'meta--error')]")
    pytest.driver.find_element(By.CLASS_NAME, 'register-form')


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome()
    pytest.driver.implicitly_wait(10)
    # Переходим на страницу авторизации
    pytest.driver.get(BASE_URL)
    on_tab_register()
    yield
    pytest.driver.quit()


def test_register_complete():
    """Базовая проверка возможности зарегистрироваться"""
    full_info = FullRegInfo()
    ui_fill_reg_info(full_info)
    pytest.driver.find_element(By.NAME, 'register').click()
    WebDriverWait(pytest.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'register-confirm-form')))


def test_register_cant_if_fields_not_filled():
    """Нельзя зарегистрироваться без заполнения полей"""
    pytest.driver.find_element(By.NAME, 'register').click()
    ui_exp_reg_error()


def test_register_default_region():
    """Регион по умолчанию - Москва"""
    default_region = pytest.driver.find_element(By.XPATH, ".//div[contains(@class,'rt-select__input')]//span[@class='rt-input__mask-start']").get_attribute('textContent')
    assert default_region == 'Москва г'


def test_register_select_some_region():
    """Выбираем регион, отличный от региона по-умолчанию"""
    pytest.driver.find_element(By.XPATH, ".//div[contains(@class,'register-form__dropdown')]//div[@class='rt-input__action']").click()
    pytest.driver.find_element(By.XPATH, "//div[@class='rt-select__list-item' and text()[contains(.,'Санкт-Петербург')]]").click()
    default_region = pytest.driver.find_element(By.XPATH, ".//div[contains(@class,'rt-select__input')]//span[@class='rt-input__mask-start']").get_attribute('textContent')
    assert default_region == 'Санкт-Петербург г'


@pytest.mark.parametrize("positive", [2, 3, 30])
def test_register_name_size_good(positive):
    """Граничные значения. Позитив. Имя"""
    full_info = FullRegInfo()
    full_info.first_name = generate_letters_ru(positive)
    ui_fill_reg_info(full_info)
    pytest.driver.find_element(By.NAME, 'register').click()
    ui_exp_reg_confirm()


@pytest.mark.parametrize("negative", [0, 1, 32])
def test_register_name_size_bad(negative):
    """Граничные значения. Негатив. Имя"""
    full_info = FullRegInfo()
    full_info.first_name = generate_letters_ru(negative)
    ui_fill_reg_info(full_info)
    pytest.driver.find_element(By.NAME, 'register').click()
    ui_exp_reg_error()


@pytest.mark.parametrize("positive", [2, 3, 30])
def test_register_last_name_size_good(positive):
    """Граничные значения. Позитив. Фамилия"""
    full_info = FullRegInfo()
    full_info.last_name = generate_letters_ru(positive)
    ui_fill_reg_info(full_info)
    pytest.driver.find_element(By.NAME, 'register').click()
    ui_exp_reg_confirm()


@pytest.mark.parametrize("negative", [0, 1, 32])
def test_register_last_name_size_bad(negative):
    """Граничные значения. Негатив. Фамилия"""
    full_info = FullRegInfo()
    full_info.last_name = generate_letters_ru(negative)
    ui_fill_reg_info(full_info)
    pytest.driver.find_element(By.NAME, 'register').click()
    ui_exp_reg_error()


@pytest.mark.parametrize("positive", ['+79254558197', '+375254558197'])
def test_register_phone_size_good(positive):
    """Граничные значения. Позитив. Номер"""
    full_info = FullRegInfo()
    full_info.address = positive
    ui_fill_reg_info(full_info)
    pytest.driver.find_element(By.NAME, 'register').click()
    ui_exp_reg_confirm()


@pytest.mark.parametrize("negative", [('', 0), ('+7', 9), ('+7', 11), ('+375', 8), ('+375', 10)], ids="{0}".format)
def test_register_phone_size_bad(negative):
    """Граничные значения. Негатив. Номер"""
    full_info = FullRegInfo()
    full_info.address = f'{negative[0]}{generate_numbers(int(negative[1]))}'
    ui_fill_reg_info(full_info)
    pytest.driver.find_element(By.NAME, 'register').click()
    ui_exp_reg_error()


@pytest.mark.parametrize("positive", [(1, '@y.r'), (251, '@y.r')], ids="{0}".format)
def test_register_email_size_good(positive):
    """Граничные значения. Позитив. Email"""
    full_info = FullRegInfo()
    full_info.address = f'{generate_letters_en(positive[0])}{positive[1]}'
    ui_fill_reg_info(full_info)
    pytest.driver.find_element(By.NAME, 'register').click()
    ui_exp_reg_confirm()


@pytest.mark.parametrize("negative", [(0, ''), (0, '@y.r'), (252, '@y.r')], ids="{0}".format)
def test_register_email_size_bad(negative):
    """Граничные значения. Негатив. Email"""
    full_info = FullRegInfo()
    full_info.address = f'{generate_letters_en(negative[0])}{negative[1]}'
    ui_fill_reg_info(full_info)
    pytest.driver.find_element(By.NAME, 'register').click()
    ui_exp_reg_error()


@pytest.mark.parametrize("positive", [('A!', 6), ('A!', 7), ('A!', 18)], ids="{0}".format)
def test_register_password_size_good(positive):
    """Граничные значения. Позитив. Пароли"""
    password = f'{positive[0]}{generate_letters_en(int(positive[1]))}'
    full_info = FullRegInfo()
    full_info.password = password
    full_info.password_confirm = password
    ui_fill_reg_info(full_info)
    pytest.driver.find_element(By.NAME, 'register').click()
    ui_exp_reg_confirm()


@pytest.mark.parametrize("negative", [('', 0), ('A!', 5), ('A!', 19)], ids="{0}".format)
def test_register_password_size_bad(negative):
    """Граничные значения. Негатив. Пароли"""
    password = f'{negative[0]}{generate_letters_en(int(negative[1]))}'
    full_info = FullRegInfo()
    full_info.password = password
    full_info.password_confirm = password
    ui_fill_reg_info(full_info)
    pytest.driver.find_element(By.NAME, 'register').click()
    ui_exp_reg_error()


@pytest.mark.parametrize("negative", [('A!ssssss', 'ffffffB?'), ('A!ssssss', 'A!Ssssss')], ids="{0}".format)
def test_register_password_and_password_confirm_not_equals(negative):
    """Граничные значения. Негатив. Пароли"""
    full_info = FullRegInfo()
    full_info.password = f'{negative[0]}'
    full_info.password_confirm = f'{negative[1]}'
    ui_fill_reg_info(full_info)
    pytest.driver.find_element(By.NAME, 'register').click()
    ui_exp_reg_error()


@pytest.mark.parametrize("negative", ['qq', 'бq', '12', 'б1', '“[|]’~<!--@ /*$%^&#*/ ()?>,.*/\\'])
def test_register_name_equivalence(negative):
    """Классы эквивалентности. Негатив. Имя"""
    full_info = FullRegInfo()
    full_info.first_name = negative
    ui_fill_reg_info(full_info)
    pytest.driver.find_element(By.NAME, 'register').click()
    ui_exp_reg_error()


@pytest.mark.parametrize("negative", ['qq', 'бq', '12', 'б1', '“[|]’~<!--@ /*$%^&#*/ ()?>,.*/\\'])
def test_register_last_name_equivalence(negative):
    """Классы эквивалентности. Негатив. Фамилия"""
    full_info = FullRegInfo()
    full_info.last_name = negative
    ui_fill_reg_info(full_info)
    pytest.driver.find_element(By.NAME, 'register').click()
    ui_exp_reg_error()


@pytest.mark.parametrize("positive",
                         [f'{generate_numbers(10)}@y.ru',
                          f'{generate_letters_en(10)}@y.ru',
                          f'{generate_letters_en(5)}{generate_numbers(5)}@y.ru'])
def test_register_email_equivalence_good(positive):
    """Классы эквивалентности. Позитив. Email"""
    full_info = FullRegInfo()
    full_info.address = positive
    ui_fill_reg_info(full_info)
    pytest.driver.find_element(By.NAME, 'register').click()
    ui_exp_reg_confirm()


@pytest.mark.parametrize("negative",
                         [f'{generate_letters_ru(10)}@y.ru',
                          '“[|]’~<!--@ /*$%^&#*/ ()?>,.*/\\@y.ru',
                          ' @y.ru',
                          's@ .ru',
                          's@y ru',
                          's@y. ru',
                          's@y.r u'])
def test_register_second_email_equivalence_bad(negative):
    """Классы эквивалентности. Негатив. Email"""
    full_info = FullRegInfo()
    full_info.address = negative
    ui_fill_reg_info(full_info)
    pytest.driver.find_element(By.NAME, 'register').click()
    ui_exp_reg_error()


#Минусы преобразуются в плюсы
@pytest.mark.parametrize("positive", [f'-7{generate_numbers(10)}', f'-375{generate_numbers(9)}'])
def test_register_phone_equivalence_good(positive):
    """Классы эквивалентности. Негатив. Телефон"""
    full_info = FullRegInfo()
    full_info.address = positive
    ui_fill_reg_info(full_info)
    pytest.driver.find_element(By.NAME, 'register').click()
    ui_exp_reg_confirm()


@pytest.mark.parametrize("negative",
                         [f'+7{generate_letters_en(10)}',
                          f'+375{generate_letters_en(9)}',
                          '+7“[|]’~<!--',
                          '+375“[|]’~<!-])
def test_register_phone_equivalence_bad(negative):
    """Классы эквивалентности. Негатив. Телефон"""
    full_info = FullRegInfo()
    full_info.address = negative
    ui_fill_reg_info(full_info)
    pytest.driver.find_element(By.NAME, 'register').click()
    ui_exp_reg_error()


@pytest.mark.parametrize("positive",
                         ['A!a“[|]’~<!--@/*$%^',
                          'A!a&#*/()?>,.*/\\',
                          f'A!a{generate_numbers(10)}',
                          f'A!a{generate_letters_en(10)}'])
def test_register_password_equivalence_good(positive):
    """Классы эквивалентности. Позитив. Пароль"""
    full_info = FullRegInfo()
    full_info.password = positive
    full_info.password_confirm = positive
    ui_fill_reg_info(full_info)
    pytest.driver.find_element(By.NAME, 'register').click()
    ui_exp_reg_confirm()


@pytest.mark.parametrize("negative",
                         [f'A!a{generate_letters_ru(10)}',
                          ' ',
                          'W!w 12345678',
                          'W!б12345678'])
def test_register_second_email_equivalence_bad(negative):
    """Классы эквивалентности. Негатив. Пароль"""
    full_info = FullRegInfo()
    full_info.address = negative
    ui_fill_reg_info(full_info)
    pytest.driver.find_element(By.NAME, 'register').click()
    ui_exp_reg_error()
