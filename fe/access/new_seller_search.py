from fe import conf
from fe.access import seller_search, auth


def register_new_seller(user_id, password):
    a = auth.Auth(conf.URL)
    code = a.register(user_id, password)
    assert code == 200
    s = seller_search.Seller(conf.URL, user_id, password)
    return s
