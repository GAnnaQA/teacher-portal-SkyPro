from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from helper_class.data import data_test
import allure
from selenium.webdriver.support.ui import Select
import requests


@allure.epic('UI_кабинет преподавателя')
@allure.story('Authorization')
class authorization:
    @allure.step('Открытие браузера')
    def __init__(self, browser: str):
        self._driver = browser
        self._driver.maximize_window()
        self._driver.implicitly_wait(4)

    @allure.step('Открытие страницы авторизации')
    def open_auto_page(self):
        self._driver.get(data_test.url_auto_SkyEng)
        try:
            button = WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "link--primary") and text()="Войти с помощью пароля"]'))
                )
            button.click()
        except StaleElementReferenceException:
            print("Старый элемент, попытка повторного получения...")
            button = WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "link--primary") and text()="Войти с помощью пароля"]'))
                )
            button.click()

    @allure.step('Ввод {userName} в поле ввода "Телефон, почта или логин"')    
    def enter_the_user_name(self, userName=data_test.user_name_teacher):
        user_name = self._driver.find_element(
            By.CSS_SELECTOR, 'input[name="username"]'
            )
        user_name.send_keys(userName)

    @allure.step('Ввод {password} в поле ввода "Пароль"') 
    def enter_the_password(self, password=data_test.user_password_teacher):
        password_input = self._driver.find_element(
            By.CSS_SELECTOR, 'input[name="password"]'
            )
        password_input.send_keys(password)

    @allure.step('Нажатие кнопки "Войти"')
    def click_login_button(self):
        login_button = self._driver.find_element(
            By.CSS_SELECTOR, 'button.button.button--primary'
            )
        login_button.click()

    @allure.step('Пулучение токена из куки')
    def get_token_global_from_cookies(self) -> str|None:
        WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, 'a[data-qa-id="left-menu-item:Расписание"]'
                ))
            )          
        cookies = self._driver.get_cookies()
        for c in cookies: 
            if c.get('name') == 'token_global':
                return f"{c.get('name')}={c.get('value')}"
        return None


@allure.epic('UI_кабинет преподавателя')
@allure.story('Calendar')
class calendar:
    @allure.step('Открытие страницы расписания')
    def __init__(self, browser: str):
        self._driver = browser
        schedule_button = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, 'a[data-qa-id="left-menu-item:Расписание"]'
                ))
            )
        schedule_button.click()

    @allure.step('Нажатие кнопки + для добавления события')
    def click_plus(self):
        plus_button = WebDriverWait(self._driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'use'))
        )
        plus_button.click()

    @allure.step('Нажатие кнопки "Личныое событие"')
    def click_personal_events(self):
        personal_events_button = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, "//div[contains(@class, '-size-m') and .//span[text()=' Личное событие ']]"
                ))
            )
        personal_events_button.click()

    @allure.step('Ввод {EventName} в поле "Название события"')
    def enter_event_name(self, EventName: str):
        event_name_input = self._driver.find_element(
            By.CSS_SELECTOR, 'input[placeholder="Например: посмотреть вебинар"]'
            )
        event_name_input.send_keys(EventName)

    @allure.step('Ввод даты в поле "День и время"')
    def enter_event_date(self, EventDate: str):
        event_date_input = self._driver.find_element(
            By.CSS_SELECTOR, 'select.class-date'
            )
        select = Select(event_date_input)
        select.select_by_value(EventDate)

    @allure.step('Очищение поля "Название события"')
    def clear_event_name(self):
        event_name_input = self._driver.find_element(
            By.CSS_SELECTOR, 'input[placeholder="Например: посмотреть вебинар"]'
            )
        event_name_input.clear()

    @allure.step('Проверка активности кнопки "Сохранить"')
    def try_active_save_button(self) -> str:
        save_button = WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, "//button[contains(@class, '-type-primary') and contains(@class, '-size-m') and .//div[contains(@class, 'text-container') and text()=' Cохранить ']]"
                ))
            )
        background_color = save_button.value_of_css_property('background-color')
        rgb = background_color[5:-1].split(',')
        hex_color = "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
        return hex_color

    @allure.step('Нажатие кнопки "Сохранить"')
    def click_save(self):
        save_button = WebDriverWait(self._driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, "//button[contains(@class, '-type-primary') and contains(@class, '-size-m') and .//div[contains(@class, 'text-container') and text()=' Cохранить ']]"
                ))
            )
        save_button.click()

    @allure.step('Поиск события с названием {EventName} в календаре')
    def search_event(self, EventName: str) -> bool:
        search_result = False
        try:
            event = WebDriverWait(self._driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH, f"//div[contains(@class, 'long-view') and .//div[contains(@class, 'long-view__title') and text()='{EventName}']]"
            ))
            )
            search_result = event.is_displayed()
        except TimeoutException:
            right_button = self._driver.find_element(By.CSS_SELECTOR, "div.right-button")
            right_button.click()
            event = WebDriverWait(self._driver, 10).until(
                    EC.visibility_of_element_located((
                        By.XPATH, f"//div[contains(@class, 'long-view') and .//div[contains(@class, 'long-view__title') and text()='{EventName}']]"
                    ))
                )
            search_result = event.is_displayed()
        return search_result

    @allure.step('Проверка отсутствия события с названием {EventName}')
    def check_event_deleted(self, EventName: str) -> bool:
        search_result = True
        try:
            event = WebDriverWait(self._driver, 10).until(
            EC.invisibility_of_element_located((
                By.XPATH, f"//div[contains(@class, 'long-view') and .//div[contains(@class, 'long-view__title') and text()='{EventName}']]"
            ))
            )
            search_result = True
        except TimeoutException:
            print(f"Событие '{EventName}' все еще отображается.")
            search_result = False

        return search_result

    @allure.step('Открытие карточки события с названием {EventName}')
    def open_event(self, EventName: str):
        event = WebDriverWait(self._driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH, f"//div[contains(@class, 'long-view') and .//div[contains(@class, 'long-view__title') and text()='{EventName}']]"
            ))
            )
        event.click()

    @allure.step('Редактирование открытого события')
    def edit_event(self):
        edit_button = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, "//button[contains(@class, '-type-primary') and contains(@class, '-size-m') and .//div[contains(@class, 'text-container') and text()=' Редактировать ']]"
                ))
                )
        edit_button.click()

    @allure.step('Удаление открытого события')
    def delete_event(self):
        delete_button = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, "//button[contains(@class, '-type-secondary') and contains(@class, '-size-m') and .//div[contains(@class, 'text-container') and text()=' Удалить ']]"
                ))
                )
        delete_button.click()

@allure.epic('API_кабинет преподавателя')
@allure.story('PersonalEvents')
class API_events:

    def __init__(self, url: str):
        self.url = url

    @allure.step('Добавление нового события через API')
    def add_event_via_API(self, EventName: str, EventDescr: str, TimeStart: str, TimeEnd: str, Headers: dict)-> object:
        body = {
            "backgroundColor":data_test.backgroundColor,
            "color":data_test.color,
            "description":EventDescr,
            "endAt":TimeEnd,
            "startAt":TimeStart,
            "title":EventName
            }
        resp = requests.post(self.url + '/createPersonal', json=body, headers=Headers)
        return resp
    
    @allure.step('Удаление события через API')
    def delete_event_via_API(self, id: int, StartAt: str, Headers: dict)-> object:
        body = {
            "id": id,
            "startAt": StartAt
            }
        resp = requests.post(self.url + '/removePersonal', json=body, headers=Headers)
        return resp
    
    @allure.step('Редактирование события через API')
    def edit_event_via_API(self, ID: int, EventName: str, EventDescr: str, TimeStart: str, NewTimeStart: str, NewTimeEnd: str, Headers: dict)-> object:
        body = {
            "backgroundColor": data_test.backgroundColor,
            "color": data_test.color,
            "description": EventDescr,
            "endAt": NewTimeEnd,
            "id": ID,
            "oldStartAt": TimeStart,
            "startAt": NewTimeStart,
            "title": EventName
            }
        resp = requests.post(self.url + '/updatePersonal', json=body, headers=Headers)
        return resp