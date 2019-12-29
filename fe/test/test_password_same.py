import uuid

import pytest

from fe.access import auth
from fe import conf


class TestPassword:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.auth = auth.Auth(conf.URL)
        # register a user
        self.user_id = "test_password_{}".format(str(uuid.uuid1()))
        self.old_password = "old_password_" + self.user_id
        self.new_password = "new_password_" + self.user_id
        self.terminal = "terminal_" + self.user_id

        assert self.auth.register(self.user_id, self.old_password) == 200
        yield

    def test_error_samepwd(self):
        code = self.auth.password(self.user_id, self.old_password, self.old_password)
        assert code == 520
