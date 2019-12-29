from fe import conf
from fe.access import seller, auth


def unregister_new_seller(user_id, password):
    a = auth.Auth(conf.URL)
    code = a.unregister(user_id, password)
    return code
