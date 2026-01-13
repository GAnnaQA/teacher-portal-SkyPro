from selenium import webdriver
import allure
from helper_class.data import data_test
from helper_class.calendar_page import authorization, API_events, calendar


@allure.id("PositiveAPI1")
@allure.feature('Add')
@allure.severity(allure.severity_level.CRITICAL)
@allure.title('Позитивный тест на добавление личного события с текущей датой через API')
def test_add_task_today_API():
    browser = webdriver.Chrome()
    auth = authorization(browser)
    auth.open_auto_page()
    auth.enter_the_user_name()
    auth.enter_the_password()
    auth.click_login_button() 
    token = auth.get_token_global_from_cookies()
    data = data_test()
    eventName = data.EventName()
    eventDescr = data.random_description()
    startTime = data.EventDateToday()
    endTime = data.add_minutes_to_event_date(startTime, 30)
    my_headers = {}
    my_headers['Cookie'] = token
    my_API = API_events(data_test.base_url)
    add_result = my_API.add_event_via_API(eventName, eventDescr, startTime, endTime, my_headers)
    with allure.step("Проверка получения статус-кода 200"):
        assert add_result.status_code == 200
    with allure.step("Получение Json ответа"):
        json = add_result.json()
    with allure.step("Получение значение ключа id из Json"):
        eventID = json.get("data", {}).get("payload", {}).get("id")
    with allure.step("Получение значение ключа startAt из Json"):
        start_at = json.get("data", {}).get("startAt")
    with allure.step("Проверка, что значение ключа startAt из Json равняется {startTime}"):
        assert start_at == startTime
    with allure.step("Получение значение ключа type из Json"):
        event_type = json.get("data", {}).get("type")
    with allure.step("Проверка, что значение ключа type из Json - personal"):
        assert event_type == "personal"
    with allure.step("Получение значение ключа title из Json"):
        eventTitle = json.get("data", {}).get("payload", {}).get("payload", {}).get("title")
    with allure.step("Проверка, что значение ключа title из Json равняется {eventName}"):
        assert eventTitle == eventName
    with allure.step("Получение значение ключа description из Json"):
        eventDescrip = json.get("data", {}).get("payload", {}).get("payload", {}).get("description")
    with allure.step("Проверка, что значение ключа description из Json равняется {eventDescr}"):
        assert eventDescrip == eventDescr
    my_calendar = calendar(browser)
    search = my_calendar.search_event(eventName)
    with allure.step('Проверка, что событие отображается в календаре'):
        assert search == True
    with allure.step("Закрытие браузера"):
        browser.quit()
    delete_result = my_API.delete_event_via_API(eventID, startTime, my_headers)
    with allure.step("Проверка получения статус-кода 200"):
         assert delete_result.status_code == 200
    with allure.step('Получение Json ответа'):
        delete_json = delete_result.json()
    with allure.step('Получение значения ключа data'):
        key_data = delete_json.get("data")
    with allure.step("Проверка, что data = true"):
        key_data == True
    

@allure.id("PositiveAPI2")
@allure.feature('Add')
@allure.severity(allure.severity_level.CRITICAL)
@allure.title('Позитивный тест на добавление личного события с датой в будущем через API')
def test_add_task_date_in_future_API():
    browser = webdriver.Chrome()
    auth = authorization(browser)
    auth.open_auto_page()
    auth.enter_the_user_name()
    auth.enter_the_password()
    auth.click_login_button() 
    token = auth.get_token_global_from_cookies()
    data = data_test()
    eventName = data.EventName()
    eventDescr = data.random_description()
    startTime = data.add_days_to_event_date(1)
    endTime = data.add_minutes_to_event_date(startTime, 30)
    my_headers = {}
    my_headers['Cookie'] = token
    my_API = API_events(data_test.base_url)
    add_result = my_API.add_event_via_API(eventName, eventDescr, startTime, endTime, my_headers)
    with allure.step("Проверка получения статус-кода 200"):
        assert add_result.status_code == 200
    with allure.step("Получение Json ответа"):
        json = add_result.json()
    with allure.step("Получение значение ключа id из Json"):
        eventID = json.get("data", {}).get("payload", {}).get("id")
    with allure.step("Получение значение ключа startAt из Json"):
        start_at = json.get("data", {}).get("startAt")
    with allure.step("Проверка, что значение ключа startAt из Json равняется {startTime}"):
        assert start_at == startTime
    with allure.step("Получение значение ключа type из Json"):
        event_type = json.get("data", {}).get("type")
    with allure.step("Проверка, что значение ключа type из Json - personal"):
        assert event_type == "personal"
    with allure.step("Получение значение ключа title из Json"):
        eventTitle = json.get("data", {}).get("payload", {}).get("payload", {}).get("title")
    with allure.step("Проверка, что значение ключа title из Json равняется {eventName}"):
        assert eventTitle == eventName
    with allure.step("Получение значение ключа description из Json"):
        eventDescrip = json.get("data", {}).get("payload", {}).get("payload", {}).get("description")
    with allure.step("Проверка, что значение ключа description из Json равняется {eventDescr}"):
        assert eventDescrip == eventDescr
    my_calendar = calendar(browser)
    search = my_calendar.search_event(eventName)
    with allure.step('Проверка, что событие отображается в календаре'):
        assert search == True
    with allure.step("Закрытие браузера"):
        browser.quit()
    my_API.delete_event_via_API(eventID, startTime, my_headers)

@allure.id("PositiveAPI3")
@allure.feature('Delete')
@allure.severity(allure.severity_level.CRITICAL)
@allure.title('Позитивный тест на удаление личного события через API')
def test_delete_task_API():
    browser = webdriver.Chrome()
    auth = authorization(browser)
    auth.open_auto_page()
    auth.enter_the_user_name()
    auth.enter_the_password()
    auth.click_login_button() 
    token = auth.get_token_global_from_cookies()
    data = data_test()
    eventName = data.EventName()
    evantDescr = data.random_description()
    startTime = data.EventDateToday()
    endTime = data.add_minutes_to_event_date(startTime, 30)
    my_headers = {}
    my_headers['Cookie'] = token
    my_API = API_events(data_test.base_url)
    add_result = my_API.add_event_via_API(eventName, evantDescr, startTime, endTime, my_headers)
    json = add_result.json()
    eventID = json.get("data", {}).get("payload", {}).get("id")
    delete_result = my_API.delete_event_via_API(eventID, startTime, my_headers)
    with allure.step("Проверка получения статус-кода 200"):
         assert delete_result.status_code == 200
    with allure.step('Получение Json ответа'):
        delete_json = delete_result.json()
    with allure.step('Получение значения ключа data'):
        key_data = delete_json.get("data")
    with allure.step("Проверка, что data = true"):
        key_data == True
    my_calendar = calendar(browser)
    search = my_calendar.check_event_deleted(eventName)
    with allure.step('Проверка, что событие не отображается в календаре'):
        assert search == True
    with allure.step("Закрытие браузера"):
        browser.quit()

@allure.id("PositiveAPI4")
@allure.feature('Add')
@allure.severity(allure.severity_level.NORMAL)
@allure.title('Позитивный тест на добавление личного события с пустым description через API')
def test_add_task_with_empty_description_API():
    browser = webdriver.Chrome()
    auth = authorization(browser)
    auth.open_auto_page()
    auth.enter_the_user_name()
    auth.enter_the_password()
    auth.click_login_button() 
    token = auth.get_token_global_from_cookies()
    data = data_test()
    eventName = data.EventName()
    eventDescr = ""
    startTime = data.EventDateToday()
    endTime = data.add_minutes_to_event_date(startTime, 30)
    my_headers = {}
    my_headers['Cookie'] = token
    my_API = API_events(data_test.base_url)
    add_result = my_API.add_event_via_API(eventName, eventDescr, startTime, endTime, my_headers)
    with allure.step("Проверка получения статус-кода 200"):
        assert add_result.status_code == 200
    with allure.step("Получение Json ответа"):
        json = add_result.json()
    with allure.step("Получение значение ключа id из Json"):
        eventID = json.get("data", {}).get("payload", {}).get("id")
    with allure.step("Получение значение ключа startAt из Json"):
        start_at = json.get("data", {}).get("startAt")
    with allure.step("Проверка, что значение ключа startAt из Json равняется {startTime}"):
        assert start_at == startTime
    with allure.step("Получение значение ключа type из Json"):
        event_type = json.get("data", {}).get("type")
    with allure.step("Проверка, что значение ключа type из Json - personal"):
        assert event_type == "personal"
    with allure.step("Получение значение ключа title из Json"):
        eventTitle = json.get("data", {}).get("payload", {}).get("payload", {}).get("title")
    with allure.step("Проверка, что значение ключа title из Json равняется {eventName}"):
        assert eventTitle == eventName
    with allure.step("Получение значение ключа description из Json"):
        eventDescrip = json.get("data", {}).get("payload", {}).get("payload", {}).get("description")
    with allure.step("Проверка, что значение ключа description из Json равняется {eventDescr}"):
        assert eventDescrip == eventDescr
    my_calendar = calendar(browser)
    search = my_calendar.search_event(eventName)
    with allure.step('Проверка, что событие отображается в календаре'):
        assert search == True
    with allure.step("Закрытие браузера"):
        browser.quit()
    my_API.delete_event_via_API(eventID, startTime, my_headers)

@allure.id("PositiveAPI5")
@allure.feature('Edit')
@allure.severity(allure.severity_level.NORMAL)
@allure.title('Позитивный тест на изменение даты личного события через API')
def test_edit_task_date_API():
    browser = webdriver.Chrome()
    auth = authorization(browser)
    auth.open_auto_page()
    auth.enter_the_user_name()
    auth.enter_the_password()
    auth.click_login_button() 
    token = auth.get_token_global_from_cookies()
    data = data_test()
    eventName = data.EventName()
    eventDescr = data.random_description()
    startTime = data.EventDateToday()
    endTime = data.add_minutes_to_event_date(startTime, 30)
    my_headers = {}
    my_headers['Cookie'] = token
    my_API = API_events(data_test.base_url)
    add_result = my_API.add_event_via_API(
        eventName, eventDescr, startTime, endTime, my_headers
        )
    with allure.step("Получение Json ответа"):
        json = add_result.json()
    with allure.step("Получение значение ключа id из Json"):
        eventID = json.get("data", {}).get("payload", {}).get("id")
    newStartTime = data.add_days_to_event_date(1)
    newEndTime = data.add_minutes_to_event_date(newStartTime, 60)
    edit_result = my_API.edit_event_via_API(
        eventID, eventName, eventDescr, startTime, newStartTime, newEndTime, my_headers
        )
    with allure.step("Получение Json ответа"):
        json = edit_result.json()
    with allure.step("Получение значение ключа id из Json"):
        newEventID = json.get("data", {}).get("payload", {}).get("id")
    with allure.step("Получение значение ключа startAt из Json"):
        start_at = json.get("data", {}).get("startAt")
    with allure.step("Проверка, что значение ключа startAt из Json равняется {newStartTime}"):
        assert start_at == newStartTime
    with allure.step("Получение значение ключа type из Json"):
        event_type = json.get("data", {}).get("type")
    with allure.step("Проверка, что значение ключа type из Json - personal"):
        assert event_type == "personal"
    with allure.step("Получение значение ключа title из Json"):
        eventTitle = json.get("data", {}).get("payload", {}).get("payload", {}).get("title")
    with allure.step("Проверка, что значение ключа title из Json равняется {eventName}"):
        assert eventTitle == eventName
    with allure.step("Получение значение ключа description из Json"):
        eventDescrip = json.get("data", {}).get("payload", {}).get("payload", {}).get("description")
    with allure.step("Проверка, что значение ключа description из Json равняется {eventDescr}"):
        assert eventDescrip == eventDescr
    my_calendar = calendar(browser)
    search = my_calendar.search_event(eventName)
    with allure.step('Проверка, что событие отображается в календаре'):
        assert search == True
    with allure.step("Закрытие браузера"):
        browser.quit()
    my_API.delete_event_via_API(newEventID, startTime, my_headers)
