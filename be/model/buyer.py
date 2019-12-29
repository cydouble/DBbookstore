from sqlalchemy import Column,String,Integer,Boolean,Time,ForeignKey,Text,func
from sqlalchemy import create_engine,PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash,check_password_hash    # 转换密码用到的库
import uuid
import random
from time import time
# pytest
from be.model import error
from be.model.db_conn import myuser,store,orderlist,store_booklist,store_bookstorage,extra_func
# from model import error
# from model.db_conn import myuser,store,orderlist,store_booklist,store_bookstorage,extra_func

engine = create_engine('postgresql://wrl:12345@localhost:5432/bookstore',echo = True)
DBSession = sessionmaker(bind=engine)

func1 = extra_func()
#session = DBSession()


# 订单状态
#  0:下单  1:付款  2:发货  3:收货  -1:取消
class buyer_action:
    def new_order(self, user_id, store_id, buy_book_list):  # 这里model里和test里面传入的参数不同
        """"
        @:param: user_id：买家id (str)
                 store_id：商铺id (str)
                 buy_book_list：下单图书列表 (book_id, count)
        @:return: order_id
        """
        
        new_order_id = ""
        # 创建session对象
        # session.begin()
        session = DBSession()
        find_user = session.query(myuser).filter(myuser.user_id == user_id).first()
        find_store = session.query(store).filter(store.store_id == store_id).first()
        if find_user is None:
            session.close()
            return error.error_non_exist_user_id(user_id),new_order_id  # 买家用户ID不存在  # 511

        if find_store is None:
            session.close()
            return error.error_non_exist_store_id(store_id),new_order_id  # 商铺ID不存在  # 513

        if find_user is not None and find_store is not None:
            now_user = session.query(myuser).filter(myuser.user_id == user_id).one()
            now_store = session.query(store).filter(store.store_id == store_id).one()
            new_order_id = uuid.uuid1()
            for book_id, count in buy_book_list:
                find_book = session.query(store_bookstorage).filter(store_bookstorage.book_id == book_id).first()
                # 在该商铺中判断是否有该图书
                if find_book is None:
                    session.rollback()
                    session.close()
                    return error.error_non_exist_book_id(book_id),new_order_id  # 该图书不存在  # 515
                else:
                    now_book = session.query(store_bookstorage).filter(store_bookstorage.book_id == book_id,store_bookstorage.store_id== store_id).one()
                    stock_number = now_book.storage
                    if stock_number < count:
                        session.rollback()
                        session.close()
                        return error.error_stock_level_low(book_id),new_order_id  # 商品库存不足  # 517
                    else:
                        # 减库存
                        now_book.storage = stock_number - 1
                        # 添加新的订单信息
                        new_order = orderlist(
                            order_id = new_order_id,
                            user_id = now_user.user_id,
                            store_id = now_store.store_id,
                            owner_id = now_store.owner_id,
                            book_id = book_id,
                            book_num = count,
                            order_money = count * now_book.price,
                            order_status = 0,
                            order_time = time())
                        session.add(new_order)
                        session.commit()

            session.close()
            result = (200,"ok")
            return result, new_order_id


    def payment(self, user_id, pwd, order_id):
        """"
        @:param: user_id：买家id (str)
                 pwd：买家密码 (str)
                 order_id：订单id (str)
        @:return: status code：交易状态的识别码
        """

        # session.begin()
        session = DBSession()
        find_user = session.query(myuser).filter(myuser.user_id == user_id).first()
        if find_user is None:
            session.close()
            return error.error_non_exist_user_id(user_id)  # 买家用户ID不存在  # 511
        else:
            now_user = session.query(myuser).filter(myuser.user_id == user_id).one()
            right_pwd = now_user.check_password(pwd)
            if not right_pwd:
                session.close()
                return error.error_authorization_fail()  # 密码不正确，授权失败 # 401
            else:
                # # 解析order_id字符串
                # get_order_id = order_id.split(',')
                # for one_order_id in get_order_id:
                find_order = session.query(orderlist).filter(orderlist.order_id == order_id).first()
                if (find_order is None) or (find_order.order_status != 0):
                    session.close()
                    return error.error_invalid_order_id(order_id)  # 无效订单 # 518
                else:
                    now_order = session.query(orderlist).filter(orderlist.order_id == order_id).all()
                    now_order_money = session.query(func.sum(orderlist.order_money)).filter(orderlist.order_id == order_id).scalar()
                    now_user_money = now_user.user_money
                    if now_user_money < now_order_money:
                        session.close()
                        return error.error_not_sufficient_funds(order_id)  # 余额不足 # 519
                    else:
                        now_owner = session.query(myuser).filter(myuser.user_id == find_order.owner_id).one()
                        now_owner_money = now_owner.user_money
                        # 修改订单状态
                        for one_order in now_order:
                            one_order.order_status = 1;  # 0 -> 1
                            session.add(one_order)
                        # 修改用户账户金额
                        now_user.user_money = now_user_money - now_order_money
                        session.add(now_user)
                        now_owner.user_money = now_owner_money + now_order_money
                        session.add(now_owner)
                        session.commit()
                        session.close()
                        return 200, "ok"

    def add_funds(self, user_id, pwd, add_value):
        """"
        @:param: user_id：买家id (str)
                 pwd：买家密码 (str)
                 add_value：充值金额 (int)
        @:return: status code：交易状态的识别码
        """

        # session.begin()
        session = DBSession()
        find_user = session.query(myuser).filter(myuser.user_id == user_id).first()
        if find_user is None:
            session.close()
            return error.error_non_exist_user_id(user_id)  # 买家用户ID不存在  # 511
        else:
            now_user = session.query(myuser).filter(myuser.user_id == user_id).one()
            right_pwd = now_user.check_password(pwd)
            if not right_pwd:
                session.close()
                return error.error_authorization_fail()  # 密码不正确，授权失败 # 401
            else:
                now_user.user_money = now_user.user_money + add_value
                if  now_user.user_money < 0:
                    session.close()
                    return error.error_invalid_add_value(add_value)
                else:
                    # 修改用户账户金额
                    session.add(now_user)
                    session.commit()
                    session.close()
                    return 200, "ok"

    def cancel_order(self, user_id, pwd, order_id):
        """"
        @:param: user_id：买家id (str)
                 pwd：买家密码 (str)
                 order_id：订单id (str)
        @:return: status code：交易状态的识别码
        """
        session = DBSession()
        find_user = session.query(myuser).filter(myuser.user_id == user_id).first()
        if find_user is None:
            session.close()
            return error.error_non_exist_user_id(user_id)  # 买家用户ID不存在  # 511
        else:
            now_user = session.query(myuser).filter(myuser.user_id == user_id).one()
            right_pwd = now_user.check_password(pwd)
            if not right_pwd:
                session.close()
                return error.error_authorization_fail()  # 密码不正确，授权失败 # 401
            else:
                find_order = session.query(orderlist).filter(orderlist.order_id == order_id).first()
                if find_order is None:
                    session.close()
                    return error.error_invalid_order_id(order_id)  # 无效订单 # 518
                elif find_order.order_status != 0:
                    session.close()
                    return error.error_invalid_cancel_order(order_id)  # 不可取消该订单 # 518
                else:
                    now_order = session.query(orderlist).filter(orderlist.order_id == order_id).all()
                    for one_order in now_order:
                        one_order.order_status = -1
                        session.add(one_order)
                        now_book = session.query(store_bookstorage).filter(store_bookstorage.book_id == one_order.book_id).first()
                        now_book.storage += 1
                        session.add(now_book)

                    session.commit()
                    session.close()
                    return 200, "ok"



# 搜索图书 
# 用户可以通过关键字搜索，参数化的搜索方式；
# 如搜索范围包括，题目，标签，目录，内容；全站搜索或是当前店铺搜索。
# 如果显示结果较大，需要分页
# (使用全文索引优化查找)

class search_bookstation_action:
    def search_book_title(self,book_title): # 标题搜索（考虑original title）
        session = DBSession()
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
            session.close()
            return error.error_and_message_code(526)
        session.close()
        return 200, book_onsale
        
    def search_book_tag(self,book_tag): # 标签搜索
        session = DBSession()
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
            session.close()
            return error.error_and_message_code(526)
        session.close()
        return 200, book_onsale

    def search_book_author(self,book_author):   # 作家搜索(精确搜索)
        session = DBSession()
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
            session.close()
            return error.error_and_message_code(526)
        session.close()
        return 200, book_onsale

    def search_book_content(self,book_content): # 目录搜索
        session = DBSession()
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
            session.close()
            return error.error_and_message_code(526)
        session.close()
        return 200, book_onsale

    def search_book_intro(self,book_intro): # 内容搜索
        session = DBSession()
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
            session.close()
            return error.error_and_message_code(526)
        session.close()
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
        session = DBSession()
        if func1.store_id_exist(store_id) == False:
            session.close()
            return error.error_non_exist_store_id(store_id)
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
                session.close()
                return error.error_and_message_code(526)
            session.close()
            return 200, book_onsale
        
    def search_book_tag(self, book_tag, store_id): # 标签搜索
        session = DBSession()
        if func1.store_id_exist(store_id) == False:
            session.close()
            return error.error_non_exist_store_id(store_id)
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
                session.close()
                return error.error_and_message_code(526)
            session.close()
            return 200, book_onsale

    def search_book_author(self, book_author, store_id):   # 作家搜索(精确搜索)
        session = DBSession()
        if func1.store_id_exist(store_id) == False:
            session.close()
            return error.error_non_exist_store_id(store_id)
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
                session.close()
                return error.error_and_message_code(526)

            session.close()
            return 200, book_onsale

    def search_book_content(self, book_content, store_id): # 目录搜索
        session = DBSession()
        if func1.store_id_exist(store_id) == False:
            session.close()
            return error.error_non_exist_store_id(store_id)
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
                session.close()
                return error.error_and_message_code(526)
            
            session.close()
            return 200, book_onsale

    def search_book_intro(self, book_intro, store_id): # 内容搜索
        session = DBSession()
        if func1.store_id_exist(store_id) == False:
            session.close()
            return error.error_non_exist_store_id(store_id)
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
                session.close()
                return error.error_and_message_code(526)
            
            session.close()
            return 200, book_onsale

# 订单状态/订单查询
# 用户可以查自已的历史订单，查看订单状态。
class search_order_action:
    def search_order_history(self,user_id): # 历史订单是指已经完成的订单么
        session = DBSession()
        if func1.user_id_exist(user_id) == False:
            session.close()
            return error.error_non_exist_user_id(user_id)
        else:
            order_log = session.query(
                orderlist.order_id,
                orderlist.user_id,
                orderlist.store_id,
                orderlist.owner_id,
                orderlist.book_id,
                orderlist.book_num,
                orderlist.order_money,
                orderlist.order_status,
                orderlist.order_time).filter(orderlist.user_id == user_id).all()
            if order_log == []:
                session.close()
                return error.error_and_message_code(527)
            
            session.close()
            return 200, order_log

    # def search_order_history_seller(self,seller_id): # 历史订单是指已经完成的订单么
    #     if func1.user_id_exist(seller_id) == False:
    #         return error.error_exist_user_id
    #     else:
    #         order_log = session.query(
    #             orderlist.order_id,
    #             orderlist.user_id,
    #             orderlist.store_id,
    #             orderlist.owner_id,
    #             orderlist.book_id,
    #             orderlist.book_num,
    #             orderlist.order_money,
    #             orderlist.order_status,
    #             orderlist.order_time).filter(orderlist.owner_id == seller_id).all()
    #         if order_log == []:
    #             return error.error_and_message_code(527)
    #         return 200, order_log

    def search_order_status(self,user_id,order_id):
        session = DBSession()
        if func1.user_id_exist(user_id) == False:
            session.close()
            return error.error_non_exist_user_id(user_id)
        elif func1.order_id_exist(user_id,order_id) == False:
            session.close()
            return error.error_invalid_order_id(order_id)
        else:
            order_log = session.query(
                orderlist.order_id,
                orderlist.user_id,
                orderlist.store_id,
                orderlist.owner_id,
                orderlist.book_id,
                orderlist.book_num,
                orderlist.order_money,
                orderlist.order_status,
                orderlist.order_time).filter(orderlist.user_id == user_id, orderlist.order_id == order_id).all()
            if order_log == []:
                session.close()
                return error.error_and_message_code(527)
            session.close()
            return 200, order_log

    # def search_order_status_seller(self,seller_id,store_id):
    #     if func1.user_id_exist(seller_id) == False:
    #         return error.error_exist_user_id
    #     elif func1.store_id_exist(store_id) == False:
    #         return error.error_invalid_order_id
    #     else:
    #         order_log = session.query(
    #             orderlist.order_id,
    #             orderlist.user_id,
    #             orderlist.store_id,
    #             orderlist.owner_id,
    #             orderlist.book_id,
    #             orderlist.book_num,
    #             orderlist.order_money,
    #             orderlist.order_status,
    #             orderlist.order_time).filter(orderlist.owner_id == seller_id, orderlist.store_id == store_id).one()
    #         if order_log == None:
    #             return error.error_and_message_code(527)
    #         return 200, order_log


