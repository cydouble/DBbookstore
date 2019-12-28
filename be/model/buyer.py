from sqlalchemy import Column,String,Integer,Boolean,Time,ForeignKey,Text
from sqlalchemy import create_engine,PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash,check_password_hash    # 转换密码用到的库
import random
from time import time
# from be.model import error
# from be.model.db_conn import myuser,store
from model import error
from model.db_conn import myuser,store,orderlist,store_booklist,store_bookstorage,extra_func

engine = create_engine('postgresql://caoyunyun:postgres@127.0.0.1:5432/test',echo = True)
DBSession = sessionmaker(bind=engine)

func = extra_func()
session = DBSession()

# 搜索图书 
# 用户可以通过关键字搜索，参数化的搜索方式；
# 如搜索范围包括，题目，标签，目录，内容；全站搜索或是当前店铺搜索。
# 如果显示结果较大，需要分页
# (使用全文索引优化查找)

class search_bookstation_action:
    def search_book_title(self,book_title): # 标题搜索（考虑original title）
        book_onsale = session.query(
            store_booklist.title,
            store_booklist.original_title,
            store_booklist.author,
            store_booklist.tags,
            store_bookstorage.price, # store_booklist
            store_booklist.store_id,
            store_bookstorage.storage,
            store_booklist.book_intro,
            store_booklist.content
        ).join(
            store_bookstorage, 
            store_bookstorage.book_id == store_booklist.book_id).filter(
                store_booklist.title.like('%' + book_title + '%')).all()
        if book_onsale == []:
            return error.error_and_message_code(526)
        return 200, book_onsale
        
    def search_book_tag(self,book_tag): # 标签搜索
        book_onsale = session.query(
            store_booklist.title,
            store_booklist.original_title,
            store_booklist.author,
            store_booklist.tags,
            store_bookstorage.price, # store_booklist
            store_booklist.store_id,
            store_bookstorage.storage,
            store_booklist.book_intro,
            store_booklist.content
        ).join(
            store_bookstorage, 
            store_bookstorage.book_id == store_booklist.book_id).filter(
                store_booklist.tags.like('%' + book_tag + '%')).all()
        if book_onsale == []:
            return error.error_and_message_code(526)
        return 200, book_onsale

    def search_book_author(self,book_author):   # 作家搜索(精确搜索)
        book_onsale = session.query(
            store_booklist.title,
            store_booklist.original_title,
            store_booklist.author,
            store_booklist.tags,
            store_bookstorage.price, # store_booklist
            store_booklist.store_id,
            store_bookstorage.storage,
            store_booklist.book_intro,
            store_booklist.content
        ).join(
            store_bookstorage, 
            store_bookstorage.book_id == store_booklist.book_id).filter(
                store_booklist.author.like('%' + book_author + '%')).all()
        if book_onsale == []:
            return error.error_and_message_code(526)
        return 200, book_onsale

    def search_book_content(self,book_content): # 目录搜索
        book_onsale = session.query(
            store_booklist.title,
            store_booklist.original_title,
            store_booklist.author,
            store_booklist.tags,
            store_bookstorage.price, # store_booklist
            store_booklist.store_id,
            store_bookstorage.storage,
            store_booklist.book_intro,
            store_booklist.content
        ).join(
            store_bookstorage, 
            store_bookstorage.book_id == store_booklist.book_id).filter(
                store_booklist.content.like('%' + book_content + '%')).all()
        if book_onsale == []:
            return error.error_and_message_code(526)
        return 200, book_onsale

    def search_book_intro(self,book_intro): # 内容搜索
        book_onsale = session.query(
            store_booklist.title,
            store_booklist.original_title,
            store_booklist.author,
            store_booklist.tags,
            store_bookstorage.price, # store_booklist
            store_booklist.store_id,
            store_bookstorage.storage,
            store_booklist.book_intro,
            store_booklist.content
        ).join(
            store_bookstorage,
            store_bookstorage.book_id == store_booklist.book_id).filter(
                store_booklist.book_intro.like('%' + book_intro + '%')).all()
        if book_onsale == []:
            return error.error_and_message_code(526)
        return 200, book_onsale
    
class search_bookstore_action:
    # def search_book_instore(self,store_id): # 店内搜索
    #     if func.store_id_exist == False:
    #         return error.error_exist_store_id
    #     else:
    #         book_onsale = session.query(
    #             store_booklist.title,
    #             store_booklist.store_id,
    #             store_booklist.author,
    #             store_booklist.price
    #         ).join(
    #             store_bookstorage).filter(
    #                 store_bookstorage.book_id == store_booklist.book_id,
    #                 store_booklist.store_id == store_id,
    #                 store_bookstorage.storage != 0).all()
    #         if book_onsale == []:
    #             return error.error_and_message_code(526)
    #         return 200, book_onsale
    def search_book_title(self, book_title, store_id): # 标题搜索（考虑original title）
        if func.store_id_exist == False:
            return error.error_exist_store_id
        else:
            book_onsale = session.query(
                store_booklist.title,
                store_booklist.original_title,
                store_booklist.author,
                store_booklist.tags,
                store_bookstorage.price, # store_booklist
                store_booklist.store_id,
                store_bookstorage.storage,
                store_booklist.book_intro,
                store_booklist.content
            ).join(
                store_bookstorage,
                store_bookstorage.book_id == store_booklist.book_id).filter(
                    store_booklist.store_id == store_id,
                    store_booklist.title.like('%' + book_title + '%')).all()
            if book_onsale == []:
                return error.error_and_message_code(526)
            return 200, book_onsale
        
    def search_book_tag(self, book_tag, store_id): # 标签搜索
        if func.store_id_exist == False:
            return error.error_exist_store_id
        else:
            book_onsale = session.query(
                store_booklist.title,
                store_booklist.original_title,
                store_booklist.author,
                store_booklist.tags,
                store_bookstorage.price, # store_booklist
                store_booklist.store_id,
                store_bookstorage.storage,
                store_booklist.book_intro,
                store_booklist.content
            ).join(
                store_bookstorage,
                store_bookstorage.book_id == store_booklist.book_id).filter(
                    store_booklist.store_id == store_id,
                    store_booklist.tags.like('%' + book_tag + '%')).all()
            if book_onsale == []:
                return error.error_and_message_code(526)
            return 200, book_onsale

    def search_book_author(self, book_author, store_id):   # 作家搜索(精确搜索)
        if func.store_id_exist == False:
            return error.error_exist_store_id
        else:
            book_onsale = session.query(
                store_booklist.title,
                store_booklist.original_title,
                store_booklist.author,
                store_booklist.tags,
                store_bookstorage.price, # store_booklist
                store_booklist.store_id,
                store_bookstorage.storage,
                store_booklist.book_intro,
                store_booklist.content
            ).join(
                store_bookstorage,
                store_bookstorage.book_id == store_booklist.book_id).filter(
                    store_booklist.store_id == store_id,
                    store_booklist.author.like('%' + book_author + '%')).all()
            if book_onsale == []:
                return error.error_and_message_code(526)
            return 200, book_onsale

    def search_book_content(self, book_content, store_id): # 目录搜索
        if func.store_id_exist == False:
            return error.error_exist_store_id
        else:
            book_onsale = session.query(
                store_booklist.title,
                store_booklist.original_title,
                store_booklist.author,
                store_booklist.tags,
                store_bookstorage.price, # store_booklist
                store_booklist.store_id,
                store_bookstorage.storage,
                store_booklist.book_intro,
                store_booklist.content
            ).join(
                store_bookstorage,
                store_bookstorage.book_id == store_booklist.book_id).filter(
                    store_booklist.store_id == store_id,
                    store_booklist.content.like('%' + book_content + '%')).all()
            if book_onsale == []:
                return error.error_and_message_code(526)
            return 200, book_onsale

    def search_book_intro(self, book_intro, store_id): # 内容搜索
        if func.store_id_exist == False:
            return error.error_exist_store_id
        else:
            book_onsale = session.query(
                store_booklist.title,
                store_booklist.original_title,
                store_booklist.author,
                store_booklist.tags,
                store_bookstorage.price, # store_booklist
                store_booklist.store_id,
                store_bookstorage.storage,
                store_booklist.book_intro,
                store_booklist.content
            ).join(
                store_bookstorage,
                store_bookstorage.book_id == store_booklist.book_id).filter(
                    store_booklist.store_id == store_id,
                    store_booklist.book_intro.like('%' + book_intro + '%')).all()
            if book_onsale == []:
                return error.error_and_message_code(526)
            return 200, book_onsale

# 订单状态/订单查询
# 用户可以查自已的历史订单，查看订单状态。
class search_order_action:
    def search_order_history(self,user_id): # 历史订单是指已经完成的订单么
        if func.user_id_exist(user_id) == False:
            return error.error_exist_user_id
        else:
            order_log = session.query(orderlist).filter(orderlist.user_id == user_id).all()
            if order_log == []:
                return error.error_and_message_code(527)
            return 200, order_log

    def search_order_history_seller(self,seller_id): # 历史订单是指已经完成的订单么
        if func.user_id_exist(seller_id) == False:
            return error.error_exist_user_id
        else:
            order_log = session.query(orderlist).filter(orderlist.owner_id == seller_id).all()
            if order_log == []:
                return error.error_and_message_code(527)
            return 200, order_log

    def search_order_status(self,user_id,order_id):
        if func.user_id_exist(user_id) == False:
            return error.error_exist_user_id
        elif func.order_id_exist(order_id) == False:
            return error.error_invalid_order_id
        else:
            order_log = session.query(orderlist).filter(orderlist.user_id == user_id, orderlist.order_id == order_id).one()
            if order_log == []:
                return error.error_and_message_code(527)
            return 200, order_log

    def search_order_status_seller(self,seller_id,store_id):
        if func.user_id_exist(seller_id) == False:
            return error.error_exist_user_id
        elif func.store_id_exist(store_id) == False:
            return error.error_invalid_order_id
        else:
            order_log = session.query(orderlist).filter(orderlist.owner_id == seller_id, orderlist.store_id == store_id).one()
            if order_log == None:
                return error.error_and_message_code(527)
            return 200, order_log


