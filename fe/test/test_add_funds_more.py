import pytest
import uuid
from fe.access.new_buyer import register_new_buyer


class TestAddFunds:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.user_id = "test_add_funds_{}".format(str(uuid.uuid1()))
        self.password = self.user_id
        self.buyer = register_new_buyer(self.user_id, self.password)
        yield

    def test_invalid_add_values(self):
        code = self.buyer.add_funds(1000)
        assert code == 200

        code = self.buyer.add_funds(-1001)
        assert code != 200