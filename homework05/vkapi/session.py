import time
import typing as tp

import requests
from requests.exceptions import RequestException


GET = "get"
POST = "post"


class Session:
    """
    Сессия.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    __slots__ = ('base_url', 'timeout', 'max_retries', 'backoff_factor')

    def __init__(
            self,
            base_url: str,
            timeout: float = 5.0,
            max_retries: int = 3,
            backoff_factor: float = 0.3,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        return request(method=GET, url=self.base_url + url, timeout=self.timeout, max_retries=self.max_retries,
                       backoff_factor=self.backoff_factor, *args, **kwargs)

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        return request(method=POST, url=self.base_url + url, timeout=self.timeout, max_retries=self.max_retries,
                       backoff_factor=self.backoff_factor, *args, **kwargs)


def request(method, url, params=None, timeout=5.0, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param method: метод запроса: GET, POST, etc
    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки


    Returns:
        requests.Response: Объект Response в случае успешного запроса.
        None: В случае, если все запросы завершились ошибкой.
    """

    if params is None:
        params = dict()

    retries = 0
    while retries < max_retries:
        try:
            response = requests.request(method=method, url=url, params=params, timeout=timeout)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response
        except RequestException as e:
            retries += 1
            if retries == max_retries:
                print(f"Максимальное количество попыток ({max_retries}) исчерпано. Ошибка: {e}")
                return None

            delay = (backoff_factor * (2 ** (retries - 1)))
            print(f"Ошибка запроса: {e}. Повторная попытка через {delay:.2f} секунд...")
            time.sleep(delay)
    return None
