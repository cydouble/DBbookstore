import requests
import simplejson
from urllib.parse import urljoin
from fe.access.auth import Auth


class Buyer:
    def __init__(self, url_prefix, user_id, password):
        self.url_prefix_seller = urljoin(url_prefix, "seller/")
        self.url_prefix = urljoin(url_prefix, "buyer/")
        self.user_id = user_id
        self.password = password
        self.token = ""
        self.terminal = "my terminal"
        self.auth = Auth(url_prefix)
        code, self.token = self.auth.login(self.user_id, self.password, self.terminal)
        assert code == 200

    def new_order(self, store_id: str, book_id_and_count: [(str, int)]) -> (int, str):
        books = []
        for id_count_pair in book_id_and_count:
            books.append({"id": id_count_pair[0], "count": id_count_pair[1]})
        json = {"user_id": self.user_id, "store_id": store_id, "books": books}
        url = urljoin(self.url_prefix, "new_order")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json=json)
        response_json = r.json()
        return r.status_code, response_json.get("order_id")

    def user_order_status(self, user_id, order_id: str) -> int:
        json = {"user_id": self.user_id, "order_id": order_id}
        url = urljoin(self.url_prefix, "myorder")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json=json)
        return r.status_code

    def user_order(self, user_id) -> int:
        json = {"user_id": self.user_id}
        url = urljoin(self.url_prefix, "myorder")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json=json)
        return r.status_code

    def deliver(self, order_id):
        json = {"order_id": order_id}
        url = urljoin(self.url_prefix_seller, "deliver")
        r = requests.post(url, json=json)
        return r.status_code

    def payment(self,  order_id: str):
        json = {"user_id": self.user_id, "password": self.password, "order_id": order_id}
        url = urljoin(self.url_prefix, "payment")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json=json)
        return r.status_code

    def add_funds(self, add_value: str) -> int:
        json = {"user_id": self.user_id, "password": self.password, "add_value": add_value}
        url = urljoin(self.url_prefix, "add_funds")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json=json)
        return r.status_code

    def recieve(self, order_id):
        json = {"order_id": order_id}
        url = urljoin(self.url_prefix_seller, "recieve")
        r = requests.post(url, json=json)
        return r.status_code

    # add more
    def cancel_order(self, order_id: str) :
        json = {"user_id": self.user_id, "password": self.password, "order_id": order_id}
        url = urljoin(self.url_prefix, "cancel_order")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json=json)
        return r.status_code

    

    