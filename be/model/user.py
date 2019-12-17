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
from model.db_conn import myuser,store

engine = create_engine('postgresql://caoyunyun:postgres@127.0.0.1:5432/test',echo = True)
DBSession = sessionmaker(bind=engine)

def get_user(user_id):
    session = DBSession()
    find_user = session.query(myuser).filter(myuser.user_id == user_id).first()
    session.close()
    return find_user

class loginout_action:
    def login(self,user_id,pwd,ter):
        session = DBSession()
        # 只需要修改登陆时间即可
        find_user = session.query(myuser).filter(myuser.user_id == user_id).first()
        if find_user == None: 
            session.close()
            return error.error_non_exist_user_id(user_id)  # 用户名错误 #511
        else:
            now_user = session.query(myuser).filter(myuser.user_id == user_id).one()
            pwd_tag = now_user.check_password(pwd)
            if pwd_tag == False:
                session.close()
                return error.error_authorization_fail()  # 密码错误
            else:
                print("@@@@@@@@@@@@@@@@@",user_id)                 
                session.query(myuser).filter(myuser.user_id == user_id).update({'login_at':time(),'terminal':ter})
                session.commit()
                session.close()
                return 200,"ok"
    
    def logout(self,user_id):
        session = DBSession()
        find_user = session.query(myuser).filter(myuser.user_id == user_id).first()
        if find_user != None:
            session.close()
            return 200,"ok"
        else:
            session.close()
            return error.error_non_exist_user_id(user_id) # 用户名错误 # 511

    def change_password(self,user_id,oldpwd,newpwd):
        session = DBSession()
        find_user = session.query(myuser).filter(myuser.user_id == user_id).first()
        if find_user == None:
            session.close()
            return error.error_authorization_fail() # 更改密码失败
        else:
            now_user = session.query(myuser).filter(myuser.user_id == user_id).one()
            pwd_tag = now_user.check_password(oldpwd)
            if pwd_tag == False:
                session.close()
                return error.error_authorization_fail() # 更改密码失败
            if oldpwd == newpwd:
                session.close()
                return error.error_and_message_code(520) # 更改密码失败
            else:
                newpwd_hash = generate_password_hash(newpwd)
                session.query(myuser).filter(myuser.user_id == user_id).update({'user_password':newpwd_hash})
                session.commit()
                session.close()
                return 200,"ok"

class register_action:
    def register(self,user_id,pwd):
        session = DBSession()
        find_user = session.query(myuser).filter(myuser.user_id == user_id).first()
        if find_user != None:
            session.close()
            return error.error_exist_user_id(user_id) # 注册失败，用户名重复
        else:
            new_user = myuser(
            user_id = user_id,
            user_money = 0,
            # user_address = 'you know',
            # user_tel = 1313,
            user_password = generate_password_hash(pwd),
            terminal = user_id,
            # seller_or_not = False, # ????要不要
            login_at = time()
            )
            print(new_user.user_password)
            session.add(new_user)
            session.commit()
            session.close()
            return 200,"ok"

    def unregister(self,user_id,pwd): ## 有一个问题是注销什么身份呢？如果
        session = DBSession()
        find_user = session.query(myuser).filter(myuser.user_id == user_id).first()
        if find_user == None:
            session.close()
            return error.error_authorization_fail() # 注销失败，用户名不存在
        else:
            now_user = session.query(myuser).filter(myuser.user_id == user_id).one()
            right_pwd = now_user.check_password(pwd)
            if right_pwd == False:
                return error.error_authorization_fail()  # 注销失败，密码不正确
            else:
                session.query(myuser).filter(myuser.user_id == user_id).delete() ## 这个是否需要删除
                session.query(store).filter(store.owner_id == user_id).delete()  # 删除商家门店信息
                session.commit()
                return 200,"ok"

