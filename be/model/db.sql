create table myuser(
    user_id TEXT primary key not null,
    user_money INT,
    user_address TEXT, --？？？要不要啊
    user_tel INT, --？？？要不要啊
    terminal TEXT,
    user_password TEXT,
    seller_or_not boolean,  
    login_at FLOAT);

create table store( -- 卖家拥有书店表
    store_id TEXT primary key not null,
    owner_id TEXT,
    foreign key(owner_id) REFERENCES myuser(user_id));

create table store_bookstorage( --书店库存表 (数字)
    store_id TEXT,
    book_id TEXT,
    price INT,
    storage INT,
    -- book_info TEXT, -- 原来所有的文字信息
    primary key (store_id, book_id), 
    foreign key(store_id) references store(store_id),
    foreign key(book_id) references book(id));

create table store_booklist( --书店书单表（文字）
    store_id TEXT,
    book_id TEXT,
    title TEXT,
    author TEXT,
    publisher TEXT,
    original_title TEXT,
    translator TEXT,
    pub_year TEXT,
    pages INTEGER,
    -- price INTEGER, 
    currency_unit TEXT,
    binding TEXT,
    isbn TEXT,
    author_intro TEXT,
    book_intro text,
    content TEXT,
    tags TEXT,
    primary key (store_id,book_id), 
    foreign key(store_id) references store(store_id),
    foreign key(book_id) references book(id));

create table orderlist(  -- 订单表
    order_id TEXT ,
    user_id TEXT,
    store_id TEXT,
    owner_id TEXT,
    book_id TEXT,
    book_num INT,
    order_money INT,
    order_status INT, --0:下单 1:付款  2:发货  3:收货  -1:取消
    order_time FLOAT, 
    primary key(order_id,book_id),  foreign key(user_id) references myuser(user_id),
    foreign key(store_id) references store(store_id),
    foreign key(book_id) references book(id));


-- create table book   -- 最原始数据表
--     (
--         id TEXT primary key not null,
--         title TEXT,
--         author TEXT,
--         publisher TEXT,
--         original_title TEXT,
--         translator TEXT,
--         pub_year TEXT,
--         pages INTEGER,
--         price INTEGER,
--         currency_unit TEXT,
--         binding TEXT,
--         isbn TEXT,
--         author_intro TEXT,
--         book_intro text,
--         content TEXT,
--         tags TEXT
--     );
