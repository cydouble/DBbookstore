from sqlalchemy import Column,String,Integer,Boolean,Time,ForeignKey,Text
from sqlalchemy import create_engine,PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash,check_password_hash    # 转换密码用到的库


Base = declarative_base()
class myuser(Base): # 存放user信息
    __tablename__ = 'myuser'
    user_id = Column(String,primary_key=True)
    user_money = Column(Integer)
    # user_address = Column(String)
    # user_tel = Column(Integer)
    terminal = Column(String)
    user_password = Column(String)
    login_at = Column(Time)
    # seller_or_not = Column(Boolean)

    @property
    def password(self):
        raise AttributeError("密码不允许读取")

    # 转换密码为hash存入数据库
    @password.setter
    def password(self,raw):
        self.user_password = generate_password_hash(raw)

    # 检查密码
    def check_password(self, raw):
        return check_password_hash(self.user_password,raw)
    

class store(Base): # 存放商店信息
    __tablename__ = 'store'
    store_id = Column(String,primary_key=True)
    owner_id = Column(String,ForeignKey('myuser.user_id'))

class store_booklist(Base): # 存放上架关系（书店->上架->书）
    __tablename__ = 'store_booklist'
    store_id = Column(String,ForeignKey('store.store_id'))
    book_id = Column(Text,ForeignKey('book.id'))
    __table_args__ = (
        PrimaryKeyConstraint('store_id','book_id'),
        {},
    )
class orderlist(Base): # 订单信息
    __tablename__ = 'orderlist'
    order_id = Column(Integer,primary_key=True)
    store_id = Column(String,ForeignKey('store.store_id'))
    book_id = Column(Text,ForeignKey('book.id'))
    book_num = Column(Integer)
    order_money = Column(Integer)
    order_status = Column(Integer)
    order_time = Column(Time)
    user_id = Column(String,ForeignKey('myuser.user_id'))
    book_id = Column(String,ForeignKey('book.id'))
    store_id = Column(String,ForeignKey('store.store_id'))

class book(Base): # 书籍信息
    __tablename__ = 'book'
    id  = Column(Text, primary_key=True)
    title = Column(Text)
    author = Column(Text)
    publisher = Column(Text)
    original_title = Column(Text)
    translator = Column(Text)
    pub_year = Column(Text)
    pages = Column(Integer)
    price = Column(Integer)
    currency_unit = Column(Text)
    binding = Column(Text)
    isbn = Column(Text)
    author_intro = Column(Text)
    book_intro = Column(Text)
    content = Column(Text)
    tags = Column(Text)