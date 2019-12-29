from flask_apscheduler import APScheduler  # 主要插件
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from time import time
from be.model.db_conn import orderlist
from .buyer import buyer_action


# 初始化数据库连接
engine = create_engine('postgresql://caoyunyun:postgres@127.0.0.1:5432/test',echo = True)
#engine = create_engine('postgresql://postgres:123456@127.0.0.1:5432/final_db', echo=True)
# 创建DBSession
DBSession = sessionmaker(bind=engine)
# 创建对象基类
Base = declarative_base()

scheduler = APScheduler()


def job_func():
    with scheduler.app.app_context():
        print("hello")
        message = "no order to cancel !"
        session = DBSession()
        b = buyer_action()
        # 距离当前时间的五分钟之前
        right_time = time() - 300
        # 查询超过下单时间五分钟仍未付款的订单
        overdue_orders = session.query(orderlist)\
            .filter((right_time-orderlist.order_time)>0)\
            .filter(orderlist.order_status==0).all()
            
        # 设定订单状态为-1，即自动取消订单
        for one_order in overdue_orders:
            message = "auto cancel ok !"
            one_order.order_status = -1
            session.add(one_order)
            session.commit()
            print("auto_cancel_ok！")

        session.close()
        return 200, message
