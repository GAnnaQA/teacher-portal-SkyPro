from selenium import webdriver
import allure
from helper_class.data import data_test
from helper_class.calendar_page import authorization, calendar


@allure.id("Positive1")
@allure.feature('Add')
@allure.severity(allure.severity_level.CRITICAL)
@allure.title('Позитивный тест на добавление личного события с валидным названием')
def test_add_task_valid_name():
    browser = webdriver.Chrome()
    auth = authorization(browser)
    auth.open_auto_page()
    auth.enter_the_user_name()
    auth.enter_the_password()
    auth.click_login_button()
    my_calendar = calendar(browser)
    my_calendar.click_plus()
    my_calendar.click_personal_events()
    data = data_test()
    eventName = data.EventName()
    my_calendar.enter_event_name(eventName)
    my_calendar.click_save()
    result = my_calendar.search_event(eventName)
    with allure.step('Проверка, что событие отображается в календаре'):
        assert result == True
    my_calendar.open_event(eventName)
    my_calendar.delete_event()
    browser.quit()

@allure.id("Negative1")
@allure.feature('Add')
@allure.severity(allure.severity_level.CRITICAL)
@allure.title('Негативный тест на добавление личного события с пустым названием')
def test_add_task_empty_name():
    browser = webdriver.Chrome()
    auth = authorization(browser)
    auth.open_auto_page()
    auth.enter_the_user_name()
    auth.enter_the_password()
    auth.click_login_button()
    my_calendar = calendar(browser)
    my_calendar.click_plus()
    my_calendar.click_personal_events()
    result = my_calendar.try_active_save_button()
    with allure.step('Проверка, что кнопка "Сохранить" серого цвета'):
        assert result == "#93999f"
    with allure.step("Закрыть браузер"):
        browser.quit()

@allure.id("Positive2")
@allure.feature('Delete')
@allure.severity(allure.severity_level.CRITICAL)
@allure.title('Позитивный тест на удаление личного события')
def test_delete_task():
    browser = webdriver.Chrome()
    auth = authorization(browser)
    auth.open_auto_page()
    auth.enter_the_user_name()
    auth.enter_the_password()
    auth.click_login_button()
    my_calendar = calendar(browser)
    my_calendar.click_plus()
    my_calendar.click_personal_events()
    data = data_test()
    eventName = data.EventName()
    my_calendar.enter_event_name(eventName)
    my_calendar.click_save()
    my_calendar.open_event(eventName)
    my_calendar.delete_event()
    result = my_calendar.check_event_deleted(eventName)
    with allure.step('Проверка, что событие удалено из календаря'):
        assert result == True
    with allure.step("Закрыть браузер"):
        browser.quit()

@allure.id("Positive3")
@allure.feature('Edit')
@allure.severity(allure.severity_level.CRITICAL)
@allure.title('Позитивный тест на редактирование названия личного события')
def test_edit_task_name():
    browser = webdriver.Chrome()
    auth = authorization(browser)
    auth.open_auto_page()
    auth.enter_the_user_name()
    auth.enter_the_password()
    auth.click_login_button()
    my_calendar = calendar(browser)
    my_calendar.click_plus()
    my_calendar.click_personal_events()
    data = data_test()
    eventName = data.EventName()
    my_calendar.enter_event_name(eventName)
    my_calendar.click_save()
    my_calendar.open_event(eventName)
    my_calendar.edit_event()
    my_calendar.clear_event_name()
    eventNameForEdit = data.EventName()
    my_calendar.enter_event_name(eventNameForEdit)
    my_calendar.click_save()
    result = my_calendar.search_event(eventNameForEdit)
    with allure.step('Проверка, что событие отображается в календаре'):
        assert result == True
    my_calendar.open_event(eventNameForEdit)
    my_calendar.delete_event()
    with allure.step("Закрыть браузер"):
        browser.quit()

@allure.id("Positive4")
@allure.feature('Add')
@allure.severity(allure.severity_level.CRITICAL)
@allure.title('Позитивный тест на добавление личного события с датой в будущем')
def test_add_task_future_date():
    browser = webdriver.Chrome()
    auth = authorization(browser)
    auth.open_auto_page()
    auth.enter_the_user_name()
    auth.enter_the_password()
    auth.click_login_button()
    my_calendar = calendar(browser)
    my_calendar.click_plus()
    my_calendar.click_personal_events()
    data = data_test()
    eventName = data.EventName()
    my_calendar.enter_event_name(eventName)
    eventDate = data.tomorow_date()
    my_calendar.enter_event_date(eventDate)
    my_calendar.click_save()
    result = my_calendar.search_event(eventName)
    with allure.step('Проверка, что событие отображается в календаре'):
        assert result == True
    my_calendar.open_event(eventName)
    my_calendar.delete_event()
    with allure.step("Закрыть браузер"):
        browser.quit()