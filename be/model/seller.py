from sqlalchemy import Column, String, Integer, Boolean, create_engine, Time
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json
from model import error
from model.db_conn import myuser,store,orderlist,store_bookstorage,store_booklist,extra_func



# 创建对象的基类:
Base = declarative_base()

# 初始化数据库连接:
engine = create_engine('postgresql://wrl:12345@localhost:5432/bookstore')
DBSession = sessionmaker(bind=engine)
session = DBSession()
Base.metadata.create_all(engine)

class seller_action:
    def create_store(self, user_id, store_id):
        u = session.query(myuser).filter(myuser.user_id == user_id).all()
        s = session.query(store).filter(store.store_id == store_id).all()
        if (len(u) == 0):
            return error.error_non_exist_user_id(user_id)  # 用户名错误
        if (len(s) != 0):
            return error.error_exist_store_id(store_id)  # 店铺名错误
        new_store = store(store_id = store_id, owner_id = user_id)
        u[0].seller_or_not = 1
        session.add(new_store)
        session.commit()
        return 200, 'ok'


    def add_book(self, seller_id, store_id, book_info, storage):
        u = session.query(myuser).filter(myuser.user_id == seller_id).all()
        s = session.query(store).filter(store.store_id == store_id).all()
        if (len(u) == 0):
            # print(seller_id)
            return error.error_non_exist_user_id(seller_id)  # 卖家用户ID不存在
        if (len(s) == 0):
            return error.error_non_exist_store_id(store_id)  # 商铺ID不存在
        book_info_json = json.loads(book_info)
        print(book_info_json)
        book_id = book_info_json.get('id')
        price = book_info_json.get('price')
        b = session.query(store_bookstorage).filter(store_bookstorage.book_id == book_id, store_bookstorage.store_id == store_id).all()
        print(book_id)
        print(store_id)
        print(len(b))
        if(len(b) != 0):
            return error.error_exist_book_id(book_id)   # 图书ID已存在
        
        new_book = store_bookstorage(store_id = store_id, book_id = book_info_json.get('id'), price = book_info_json.get('price'), storage = storage)
        new_book_info = store_booklist(store_id = store_id, book_id = book_info_json.get('id'), title = book_info_json.get('title'), \
            author = book_info_json.get('author'), publisher = book_info_json.get('publisher'), original_title = book_info_json.get('original_title'), \
                translator = book_info_json.get('translator'), pub_year = book_info_json.get('pub_year'), pages = book_info_json.get('pages'), \
                    currency_unit = '???', binding = book_info_json.get('binding'), isbn = book_info_json.get('isbn'), author_intro = book_info_json.get('author_intro'), \
                        book_intro = book_info_json.get('book_intro'), content = book_info_json.get('content'), tags = book_info_json.get('tags'))
        session.add(new_book)
        session.add(new_book_info)
        session.commit()
        return 200, 'ok'


    def add_stock_level(self, user_id, store_id, book_id, add_stock_level):
        s = session.query(store).filter(store.store_id == store_id).all()
        if (len(s) == 0):
            return error.error_non_exist_store_id(store_id)  # 商铺ID不存在
        b = session.query(store_bookstorage).filter(store_bookstorage.book_id == book_id, store_bookstorage.store_id == store_id).all()
        if(len(b) == 0):
            return error.error_non_exist_book_id(book_id)   # 图书ID不存在
        b[0].storage = b[0].storage + int(add_stock_level)
        session.commit()
        return 200, 'ok'


    def deliver(self, order_id):
        o = session.query(orderlist).filter(orderlist.order_id == order_id).all()
        if (len(o) == 0):
            return error.error_non_exist_store_id(order_id)  # ORDER_ID不存在
        for i in range(0, len(o)):
            if (o[i].order_status == 1):
                o[i].order_status = 2
            else:
                return error.error_exist_book_id(orderlist)  # status != 1
        session.commit()
        return 200, 'ok'
            

    def recieve(self, order_id):
        o = session.query(orderlist).filter(orderlist.order_id == order_id).all()
        if (len(o) == 0):
            return error.error_non_exist_store_id(order_id)  # ORDER_ID不存在
        for i in range(0, len(o)):
            if (o[i].order_status == 2):
                o[i].order_status = 3
            else:
                return error.error_exist_book_id(orderlist)  # status != 1
        session.commit()
        return 200, 'ok'

    # store_id = Column(String,ForeignKey('store.store_id'))
    # book_id  = Column(Text,ForeignKey('book.id'))
    # title = Column(Text)
    # author = Column(Text)
    # publisher = Column(Text)
    # original_title = Column(Text)
    # translator = Column(Text)
    # pub_year = Column(Text)
    # pages = Column(Integer)
    # price = Column(Integer)
    # currency_unit = Column(Text)
    # binding = Column(Text)
    # isbn = Column(Text)
    # author_intro = Column(Text)
    # book_intro = Column(Text)
    # content = Column(Text)
    # tags = Column(Text)