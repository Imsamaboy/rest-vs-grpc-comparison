from typing import Dict

from .models import Term

data: Dict[str, Term] = {
    "fps": Term(
        title="fps",
        definition="Количество сменяемых на интерфейсе кадров за одну секунду.",
        source_link="https://developer.mozilla.org/ru/docs/Glossary/FPS",
    ),
    "fcp": Term(
        title="fcp",
        definition=(
            "Время, за которое пользователь увидит какое-то содержимое "
            "веб-страницы, например, текст или картинку."
        ),
        source_link="https://developer.mozilla.org/ru/docs/Glossary/First_contentful_paint",
    ),
    "fid": Term(
        title="fid",
        definition="Время ожидания до первого взаимодействия с контентом.",
        source_link="https://habr.com/ru/companies/timeweb/articles/714280/",
    ),
    "tbt": Term(
        title="tbt",
        definition=(
            "Общее количество времени, когда основной поток заблокирован "
            "достаточно долго, чтобы реагировать на взаимодействия пользователя."
        ),
        source_link="https://habr.com/ru/companies/domclick/articles/549098/",
    ),
    "cls": Term(
        title="cls",
        definition=(
            "Какое количество содержимого во viewport двигалось во время загрузки страницы."
        ),
        source_link="https://habr.com/ru/companies/domclick/articles/549098/",
    ),
}
