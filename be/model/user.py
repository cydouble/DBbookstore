from sqlalchemy import Column,String,Integer,Boolean,Time,ForeignKey,Text
from sqlalchemy import create_engine,PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash,check_password_hash    # 转换密码用到的库
import random
from time import time
 # pytest
from be.model import error
from be.model.db_conn import myuser,store,orderlist,extra_func
# from model import error
# from model.db_conn import myuser,store,orderlist,extra_func

engine = create_engine('postgresql://wrl:12345@localhost:5432/bookstore',echo = True)
DBSession = sessionmaker(bind=engine)

func = extra_func()
class loginout_action:
    def login(self,user_id,pwd,ter):
        session = DBSession()
        # 只需要修改登陆时间即可
        if func.user_id_exist(user_id) == False: 
            # session.begin(subtransactions=True)
            session.close()
            return error.error_authorization_fail()  # 用户名错误 #511
        else:
            now_user = func.get_user(user_id)
            pwd_tag = now_user.check_password(pwd)
            if pwd_tag == False:
                session.close()
                return error.error_authorization_fail()  # 密码错误
            else:                 
                session.query(myuser).filter(myuser.user_id == user_id).update({'login_at' : time(), 'terminal' : ter})
                session.commit()
                session.close()
                return 200,"ok"
    
    def logout(self,user_id):
        session = DBSession()
        if func.user_id_exist(user_id) == True:
            session.close()
            return 200,"ok"
        else:
            session.close()
            return error.error_authorization_fail() # 用户名错误 # 511

    def change_password(self,user_id,oldpwd,newpwd):
        session = DBSession()
        if func.user_id_exist(user_id) == False:
            session.close()
            return error.error_authorization_fail() # 更改密码失败
        else:
            now_user = func.get_user(user_id)
            pwd_tag = now_user.check_password(oldpwd)
            if pwd_tag == False:
                session.close()
                return error.error_authorization_fail() # 输入密码错误
            if oldpwd == newpwd:
                session.close()
                return error.error_and_message_code(520) # 更改密码失败
            else:
                newpwd_hash = generate_password_hash(newpwd)
                session.query(myuser).filter(myuser.user_id == user_id).update({'user_password' : newpwd_hash})
                session.commit()
                session.close()
                return 200,"ok"

class register_action:
    def register(self,user_id,pwd):
        session = DBSession()
        # session.begin(subtransactions=True)
        if func.user_id_exist(user_id) == True:
            session.close()
            return error.error_exist_user_id(user_id) # 注册失败，用户名重复
        else:
            new_user = myuser(
            user_id = user_id,
            user_money = 0,
            user_address = 'you know',
            user_tel = 1313,
            user_password = generate_password_hash(pwd),
            terminal = user_id,
            seller_or_not = False, 
            login_at = time()
            )
            session.add(new_user)
            session.commit()
            session.close()
            return 200,"ok"

    def unregister(self,user_id,pwd): 
        session = DBSession()
        if func.user_id_exist(user_id) == False:
            session.close()
            return error.error_authorization_fail() # 注销失败，用户名不存在
        else:
            now_user = func.get_user(user_id)
            right_pwd = now_user.check_password(pwd)
            if right_pwd == False:
                return error.error_authorization_fail()  # 注销失败，密码不正确
            else:
                if now_user.seller_or_not == True:
                    return error.error_and_message_code(524)
                else:
                    # if func.user_have_order_or_not(user_id) == False:
                    session.query(myuser).filter(myuser.user_id == user_id).delete() ## 这个是否需要删除
                    session.commit()
                    return 200,"ok"
                #     else:
                #         user_order = func.get_order_info(user_id)
                #         if user_order.order_status == 3 | user_order.order_status < 0:
                #             session.query(myuser).filter(myuser.user_id == user_id).delete() ## 这个是否需要删除
                #             session.commit()
                #             return 200,"ok"
                #         else:
                #             return error.error_and_message_code(525)
        
    # def unregister_seller(self,seller_id,pwd): ## 注销一个seller
    #     session = DBSession()
    #     if func.user_id_exist(seller_id) == False:
    #         session.close()
    #         return error.error_authorization_fail() # 注销失败，用户名不存在
    #     else:
    #         now_user = func.get_user(seller_id)
    #         right_pwd = now_user.check_password(pwd)
    #         if right_pwd == False:
    #             return error.error_authorization_fail()  # 注销失败，密码不正确
    #         else:
    #             if now_user.seller_or_not == False:
    #                 return error.error_and_message_code(524)
    #             else:
    #                 user_order = func.get_order_info_seller(seller_id)
    #                 if user_order.order_status == 3 | user_order.order_status < 0:
    #                     session.query(store).filter(store.owner_id == seller_id).delete()  # 删除商家门店信息
    #                     session.query(myuser).filter(myuser.user_id == seller_id).update({'seller_or_not' : False})
    #                     session.commit()
    #                     return 200,"ok"
    #                 else:
    #                     return error.error_and_message_code(523)
                   
                
                

