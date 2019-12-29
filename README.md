# DBbookstore

### 基于Flask+Postgresql的书店购物网站的实现



#### 实验环境

-----------

- 后端框架：Flask-1.0.2
- 数据库：Postgresql
- 版本控制：git
- 覆盖率测试：pytest
- 定时功能插件：flask-apscheduler（使用pip install 安装）
- 前端测试端口号：http://127.0.0.1:5000



#### 功能描述

---------

实现一个提供网上购书功能的网站后端，网站支持书商在网站平台上开商店，购买者也可以通过网站购买，买家和卖家都可以注册自己的账号。一个买家可以开一个或多个网上商店，买家可以为自己的账户充值在任意商店购买图书，支持 `”下单->付款->发货->收货“` 流程。

- **基本功能**

  - 用户权限：**注册**（register）、**注销**（unregister）、**登录**(login)、**登出**(logout)

  - 买家功能：**下单**(new_order)、**充值**(add_funds)、 **付款**(payment)

  - 卖家功能：**创建商铺**(create_store)、**上架图书**（add_book）、**添加库存**(add_storage)

    

- **其他功能**

  - **发货、收货功能**；
  - 用户能够**查询个人的历史订单**；
  - 用户能够**查询订单状态**；
  - 用户可以在下单之后**主动取消订单**；
  - 若下单5分钟之后订单仍未付款，系统会**自动取消该订单**；
  - 图书**检索功能**（搜索方式包括：书名检索、标签检索、作者检索、目录检索、内容检索）



#### 项目目录结构

---------

```shell
DBbookstore
  |-- be                            mock backend
        |-- model                   函数功能实现
        |-- templates               前端页面实现
        |-- view                    
  |-- doc                           API specification
  |-- fe                            frontend
        |-- access
        |-- bench                   性能测试
        |-- data                    测试数据库(book.db)
        |-- test                    测试文件
  |-- script                        测试文件脚本
```

