from sqlalchemy import Column,String,Integer,Boolean,Time,ForeignKey,Text
from sqlalchemy import create_engine,PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash,check_password_hash    # 转换密码用到的库

Base = declarative_base()
class myuser(Base): # 存放user信息
    __tablename__ = 'myuser'
    user_id = Column(String,primary_key = True)
    user_money = Column(Integer)
    user_address = Column(Text)
    user_tel = Column(Integer)
    terminal = Column(String)
    user_password = Column(String)
    seller_or_not = Column(Boolean)
    login_at = Column(Time)
    

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
    store_id = Column(String,primary_key = True)
    owner_id = Column(String,ForeignKey('myuser.user_id'))

class store_bookstorage(Base): # 存放上架关系（书店->上架->书）
    __tablename__ = 'store_bookstorage'
    store_id = Column(String,ForeignKey('store.store_id'))
    book_id = Column(Text,ForeignKey('book.id'))
    price = Column(Integer)
    storage = Column(Integer)
    __table_args__ = (
        PrimaryKeyConstraint('store_id','book_id'),
        {},
    )
class store_booklist(Base): # 书籍信息
    __tablename__ = 'store_booklist'
    store_id = Column(String,ForeignKey('store.store_id'))
    book_id  = Column(Text,ForeignKey('book.id'))
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
    __table_args__ = (
        PrimaryKeyConstraint('store_id','book_id'),
        {},
    )

class orderlist(Base): # 订单信息
    __tablename__ = 'orderlist'
    order_id = Column(Integer, primary_key = True)
    user_id = Column(String,ForeignKey('myuser.user_id'))
    store_id = Column(String,ForeignKey('store.store_id'))
    owner_id = Column(String)
    book_id = Column(Text,ForeignKey('book.id'))
    book_num = Column(Integer)
    order_money = Column(Integer)
    order_status = Column(Integer)  # 0:下单 1:付款  2:发货  3:收货  -1:取消
    order_time = Column(Time)
    

class book(Base): # 书籍信息
    __tablename__ = 'book'
    id  = Column(Text, primary_key = True)
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

engine = create_engine('postgresql://caoyunyun:postgres@127.0.0.1:5432/test',echo = True)
DBSession = sessionmaker(bind=engine)  
session = DBSession() 

class extra_func:
    def user_id_exist(self,user_id):
        find_user = session.query(myuser).filter(myuser.user_id == user_id).first()
        if find_user == None:
            return False
        else:
            return True

    def book_id_exist(self, store_id, book_id):
        find_book = session.query(store_bookstorage).filter(store_bookstorage.store_id == store_id, store_bookstorage.book_id == book_id).first()
        if find_book == None:
            return False
        else:
            return True

    def store_id_exist(self, store_id):
        find_store = session.query(store).filter(store.store_id == store_id).one()
        if find_store == None:
            return False
        else:
            return True

    def book_onsale_or_not(self, store_id,book_id):
        find_book = session.query(store_bookstorage).filter(store_bookstorage.book_id == book_id, store_bookstorage.store_id == store_id).first()
        if find_book == None:
            return False
        else:
            return True

    def user_have_order_or_not(self,user_id):
        order_info = session.query(orderlist).filter(orderlist.user_id == user_id).first()
        if order_info == None:
            return False
        else:
            return True
    
    # 注意：使用一下函数之前首先要判断一下查询的对象是否存在
    def get_user(self, user_id):
        find_user = session.query(myuser).filter(myuser.user_id == user_id).one()
        return find_user

    def get_store_bookstorage(self, store_id, book_id):
        find_book_storage = session.query(store_bookstorage).filter(store_bookstorage.store_id == store_id, store_bookstorage.book_id == book_id).one()
        return find_book_storage
    
    def get_store_booktext(self, store_id, book_id):
        store_book_text = session.query(store_booklist).filter(store_booklist.book_id == book_id, store_booklist.store_id == store_id).one()
        return store_book_text

    def get_order_info(self, user_id): # 比如说用户可能没有订单，则直接调用此函数回报错
        order_info = session.query(orderlist).filter(orderlist.user_id == user_id).one()
        return order_info

session.close()
