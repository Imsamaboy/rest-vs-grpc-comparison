import grpc
import sys
import os
import random
import string
import time
from locust import User, task, between, events

# Добавляем путь к gRPC сгенерированным файлам
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'grpc'))
import glossary_pb2
import glossary_pb2_grpc

EXISTING_TERMS = ['fps', 'fcp', 'fid', 'tbt', 'cls']


def generate_random_term_data():
    """Генерация случайного термина"""
    random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return {
        "title": f"term_{random_id}",
        "definition": f"Test definition for term_{random_id}",
        "source_link": f"https://example.com/{random_id}"
    }


def generate_random_keyword():
    """Генерация случайного ключа для термина"""
    return f"test_{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}"


def build_grpc_term(term_data):
    """Создание gRPC объекта Term из словаря"""
    return glossary_pb2.Term(
        title=term_data["title"],
        definition=term_data["definition"],
        source_link=term_data["source_link"]
    )


class GlossaryGrpcUser(User):
    wait_time = between(1, 3)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.terms = EXISTING_TERMS.copy()
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = glossary_pb2_grpc.TermsServiceStub(self.channel)

    def _send_request_metrics(self, name, func, *args, **kwargs):
        """Вспомогательный метод для отправки метрик в Locust"""
        start_time = time.time()
        try:
            func(*args, **kwargs)
            elapsed_ms = max(1, int((time.time() - start_time) * 1000))
            events.request.fire(
                request_type="grpc",
                name=name,
                response_time=elapsed_ms,
                response_length=0,
                exception=None,
            )
        except Exception as exc:
            elapsed_ms = max(1, int((time.time() - start_time) * 1000))
            events.request.fire(
                request_type="grpc",
                name=name,
                response_time=elapsed_ms,
                response_length=0,
                exception=exc,
            )
            raise

    @task(6)
    def get_all_terms(self):
        """Получить все термины — самая частая операция"""
        self._send_request_metrics(
            "gRPC Get All Terms",
            self.stub.GetAllTerms,
            glossary_pb2.Empty()
        )

    @task(3)
    def create_term(self):
        """Создать новый термин"""
        new_term_data = generate_random_term_data()
        new_term = build_grpc_term(new_term_data)

        self._send_request_metrics(
            "gRPC Create Term",
            self.stub.CreateTerm,
            glossary_pb2.CreateTermRequest(
                keyword=generate_random_keyword(),
                term=new_term
            )
        )

    @task(1)
    def update_term(self):
        """Обновить существующий термин"""
        if not self.terms:
            return

        term_to_update = random.choice(self.terms)
        update_data = glossary_pb2.TermUpdate(
            definition=f"Updated definition for {term_to_update}",
            source_link=f"https://updated.com/{term_to_update}"
        )

        self._send_request_metrics(
            "gRPC Update Term",
            self.stub.UpdateTerm,
            glossary_pb2.UpdateTermRequest(
                keyword=term_to_update,
                term_update=update_data
            )
        )
