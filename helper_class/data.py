from datetime import datetime, timedelta, timezone
import random


class data_test:
    url_auto_SkyEng = "https://id.skyeng.ru/login?redirect=https%3A%2F%2Fteacher.skyeng.ru%2F"
    user_name_teacher = "test.tst345@skyeng.ru"
    user_password_teacher = "2DbhAAPG6q"
    user_name_student = "skypro1@skypro.ru"
    user_password_student = "123zav123"
    url_schedule = "https://teachers.skyeng.ru/schedule"
    event_name_for_edit = "Отредактированное тестовое событие"
    event_date = "Понедельник, 11 ноября"
    base_url = "https://api-teachers.skyeng.ru/v2/schedule"
    backgroundColor = "#F4F5F6"
    color = "#81888D"

    def random_description(self, max_length=500)-> str:
        words = [
        "Великое", "Событие", "Техно", "Достижение", "Успех", 
        "Фестиваль", "Конференция", "Выставка", "Забава", 
        "Концерт", "Семинар", "Заседание", "Гала", "Турнир",
        "Приключение", "Встреча", "Соревнование", "Летний", 
        "Зимний", "Презентация", "Дебаты", "Урок", "Консультация",
        "Экзамен", "Встреча", "Тестирование", "Тест"
        ]
        num_words = random.randint(1, 7)
        event_descr = ' '.join(random.choices(words, k=num_words))
        if len(event_descr) > max_length:
            event_descr = event_descr[:max_length - 3] + '...'
        return event_descr

    def add_minutes_to_event_date(self, event_date_str: str, minutes: int)-> str:
        event_date = event_date_str[:-6]
        event_datetime = datetime.strptime(event_date, "%Y-%m-%dT%H:%M:%S")
        new_datetime = event_datetime + timedelta(minutes=minutes)
        formatted_new_date = new_datetime.strftime("%Y-%m-%dT%H:%M:%S") + "+00:00"
        return formatted_new_date
    
    def add_days_to_event_date(self, Days: int)-> str:
        current_time = datetime.now(timezone.utc)
        new_time = current_time + timedelta(days=Days)
        formatted_date = new_time.strftime("%Y-%m-%dT%H:%M:%S") + "+00:00"
        return formatted_date

    def EventDateToday(self)-> str:
        dateNow = datetime.now(timezone.utc)
        formatted_date = dateNow.strftime("%Y-%m-%dT%H:%M:%S") + "+00:00"
        return formatted_date

    def EventName(self, max_length=40)-> str:
        words = [
        "Великое", "Событие", "Техно", "Достижение", "Успех", 
        "Фестиваль", "Конференция", "Выставка", "Забава", 
        "Концерт", "Семинар", "Заседание", "Гала", "Турнир",
        "Приключение", "Встреча", "Соревнование", "Летний", 
        "Зимний", "Презентация", "Дебаты", "Урок", "Консультация",
        "Экзамен", "Встреча", "Тестирование", "Тест"
        ]
        num_words = random.randint(1, 5)
        event_name = ' '.join(random.choices(words, k=num_words))
        if len(event_name) > max_length:
            event_name = event_name[:max_length - 3] + '...'
        return event_name


    def tomorow_date(self)-> str:
        current_date = datetime.now(timezone.utc)
        next_day = current_date + timedelta(days=1)
        formatted_date = next_day.strftime("%Y-%m-%d") + "T20:00:00.000Z"
        return formatted_date
