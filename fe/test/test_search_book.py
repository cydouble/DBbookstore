import pytest
from be.model.db_conn import extra_func
from fe.access.new_seller_search import register_new_seller
from fe.access import book
import uuid


class TestSearchBook:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        # do before test
        self.seller_id = "test_books_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_books_store_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        self.seller = register_new_seller(self.seller_id, self.password)
        code = self.seller.create_store(self.store_id)
        assert code == 200
        book_db = book.BookDB()
        self.b = book_db.get_book_info(0,1)[0]
        self.b2 = book_db.get_book_info(3,4)[0]
        self.books = self.b.__dict__
        self.list_by = ['title','tags','author','bookintro','content']
        self.list_by_what = [self.books.get('title'),self.books.get('tags')[0],'西尔维娅','数学天才','东晋']
        self.fun = extra_func()
        yield
        # do after test
    
    def test_search_title_station(self):
        # code = self.seller.remove_book(self.store_id, self.b)
        code = self.seller.search_book_instation(self.list_by_what[0]+'_x', self.list_by[0])
        assert code == 526
        code = self.seller.add_book(self.store_id, 2, self.b)
        assert code == 200
        code = self.seller.search_book_instation(self.list_by_what[0], self.list_by[0])
        assert code == 200

    def test_search_tags_station(self):
        # code = self.seller.remove_book(self.store_id, self.b)
        code = self.seller.search_book_instation(self.list_by_what[1]+'_x', self.list_by[1])
        assert code == 526
        code = self.seller.add_book(self.store_id, 2, self.b)
        assert code == 200
        code = self.seller.search_book_instation(self.list_by_what[1], self.list_by[1])
        assert code == 200

    def test_search_author_station(self):
        # code = self.seller.remove_book(self.store_id, self.b)
        code = self.seller.search_book_instation(self.list_by_what[2]+'_x', self.list_by[2])
        assert code == 526
        code = self.seller.add_book(self.store_id, 2, self.b)
        assert code == 200
        code = self.seller.search_book_instation(self.list_by_what[2], self.list_by[2])
        assert code == 200

    def test_search_bookintro_station(self):
        # code = self.seller.remove_book(self.store_id, self.b)
        code = self.seller.search_book_instation(self.list_by_what[3]+'_x', self.list_by[3])
        assert code == 526
        code = self.seller.add_book(self.store_id, 2, self.b)
        assert code == 200
        code = self.seller.search_book_instation(self.list_by_what[3], self.list_by[3])
        assert code == 200

    def test_search_content_station(self):
        # code = self.seller.remove_book(self.store_id, self.b2)
        code = self.seller.search_book_instation(self.list_by_what[4]+'_x', self.list_by[4])
        assert code == 526
        code = self.seller.add_book(self.store_id, 2, self.b2)
        assert code == 200
        code = self.seller.search_book_instation(self.list_by_what[4], self.list_by[4])
        assert code == 200

    def test_search_title(self):
        code = self.seller.search_book_instore(self.store_id, self.list_by_what[0], self.list_by[0])
        assert code == 526
        code = self.seller.add_book(self.store_id, 2, self.b)
        assert code == 200
        code = self.seller.search_book_instore(self.store_id, self.list_by_what[0], self.list_by[0])
        assert code == 200
    
    def test_search_tags(self):
        code = self.seller.search_book_instore(self.store_id, self.list_by_what[1], self.list_by[1])
        assert code == 526
        code = self.seller.add_book(self.store_id, 2, self.b)
        assert code == 200
        code = self.seller.search_book_instore(self.store_id, self.list_by_what[1], self.list_by[1])
        assert code == 200

    def test_search_author(self):
        code = self.seller.search_book_instore(self.store_id, self.list_by_what[2], self.list_by[2])
        assert code == 526
        code = self.seller.add_book(self.store_id, 2, self.b)
        assert code == 200
        code = self.seller.search_book_instore(self.store_id, self.list_by_what[2], self.list_by[2])
        assert code == 200

    def test_search_bookintro(self):
        code = self.seller.search_book_instore(self.store_id, self.list_by_what[3], self.list_by[3])
        assert code == 526
        code = self.seller.add_book(self.store_id, 2, self.b)
        assert code == 200
        code = self.seller.search_book_instore(self.store_id, self.list_by_what[3], self.list_by[3])
        assert code == 200

    def test_search_content(self):
        code = self.seller.search_book_instore(self.store_id, self.list_by_what[4], self.list_by[4])
        assert code == 526
        code = self.seller.add_book(self.store_id, 2, self.b2)
        assert code == 200
        code = self.seller.search_book_instore(self.store_id, self.list_by_what[4], self.list_by[4])
        assert code == 200