from fe import conf
from fe.access import buyer_search, auth


def register_new_buyer(user_id, password):
    a = auth.Auth(conf.URL)
    code = a.register(user_id, password)
    assert code == 200
    s = buyer_search.Buyer(conf.URL, user_id, password)
    return s
