import random
import string
from locust import HttpUser, task, between

EXISTING_TERMS = ['fps', 'fcp', 'fid', 'tbt', 'cls']


def generate_random_term():
    """
    Генерирует случайный термин для тестирования операций создания.
    """
    random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return {
        "title": f"term_{random_id}",
        "definition": f"Test definition for term_{random_id}",
        "source_link": f"https://example.com/{random_id}"
    }


def generate_random_keyword():
    """
    Генерирует случайный ключ для нового термина.
    """
    random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"test_{random_id}"


def get_task_weights():
    """
    Рассчитывает веса задач для распределения нагрузки.
    """
    # 60% - получение, 30% - создание, 10% - обновление
    return 6, 3, 1


class GlossaryRestUser(HttpUser):
    """
    Locust пользователь для нагрузочного тестирования REST сервиса глоссария.
    """
    wait_time = between(1, 3)

    GET_WEIGHT, CREATE_WEIGHT, UPDATE_WEIGHT = get_task_weights()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.my_created_terms = []

    @task(GET_WEIGHT)
    def get_all_terms(self):
        """Получить все термины — самая частая операция"""
        with self.client.get("/", catch_response=True, name="REST Get All Terms") as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status {response.status_code}")

    @task(CREATE_WEIGHT)
    def create_term(self):
        """Создать новый термин"""
        new_term = generate_random_term()
        keyword = generate_random_keyword()

        with self.client.post(f"/term/{keyword}", json=new_term, catch_response=True, name="REST Create Term") as response:
            if response.status_code == 200:
                response.success()
                self.my_created_terms.append(keyword)
            else:
                response.failure(f"Failed with status {response.status_code}")

    @task(UPDATE_WEIGHT)
    def update_term(self):
        """Обновить термины, созданные этим пользователем"""
        if not self.my_created_terms:
            return

        term_to_update = random.choice(self.my_created_terms)
        update_data = {
            "definition": f"Updated definition for {term_to_update}",
            "source_link": f"https://updated.com/{term_to_update}"
        }

        with self.client.put(f"/term/{term_to_update}", json=update_data, catch_response=True, name="REST Update Term") as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                # Термин уже удалён — считаем это успехом и убираем его из списка
                response.success()
                self.my_created_terms.remove(term_to_update)
            else:
                response.failure(f"Failed with status {response.status_code}")
