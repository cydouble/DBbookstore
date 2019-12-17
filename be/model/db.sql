create table myuser(
    user_id CHAR(20) primary key not null,
    user_money INT,
    -- user_address CHAR,
    -- user_tel INT,
    terminal CHAR(30),
    user_password CHAR(93),
    -- seller_or_not boolean,  --？？？要不要啊
    login_at FLOAT);

create table store(
    store_id CHAR(20) primary key not null,
    owner_id CHAR(20),
    foreign key(owner_id) REFERENCES myuser(user_id));

-- create table store_booklist(
--     store_id CHAR(20),
--     book_id text,
--     primary key (store_id, book_id), 
--     foreign key(store_id) references store(store_id),
--     foreign key(book_id) references book(id));


-- create table orderlist(
--     order_id INT primary key not null,
--     user_id CHAR(20),
--     store_id CHAR(20),
--     book_id TEXT,
--     book_num INT,
--     order_money INT,
--     order_status INT,
--     order_time FLOAT,
--     foreign key(user_id) references people(user_id),
--     foreign key(store_id) references store(store_id),
--     foreign key(book_id) references book(id));

-- create table book
--     (
--         id TEXT primary key,
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
--         tags TEXT,
--         picture BLOB
--     );
