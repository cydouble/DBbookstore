import pytest
from fe.access.new_seller import register_new_seller
from fe.access.unregister_seller import unregister_new_seller
import uuid


class TestUnregisterSeller:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.user_id = "test_seller_user_{}".format(str(uuid.uuid1()))
        self.store_id = "test_seller_store_{}".format(str(uuid.uuid1()))
        self.password = self.user_id
        yield

        
    def test_error_unregister_seller(self):
        self.seller = register_new_seller(self.user_id, self.password)
        code = self.seller.create_store(self.store_id)
        assert code == 200
        code = unregister_new_seller(self.user_id,self.password)
        assert code == 524
