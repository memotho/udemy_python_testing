from starter_code.models.user import UserModel
from starter_code.tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel('test', 'abcd')

            self.assertIsNone(UserModel.find_by_username('test'),
                            "Found user with name 'test' before saving to the database.")
            self.assertIsNone(UserModel.find_by_id(1),
                            "Found user with id '1' before saving to the database.")

            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_username('test'),
                                "Did not find a user with name 'test' after saving to the database.")
            self.assertIsNotNone(UserModel.find_by_id(1),
                                "Did not find a user with id '1' after saving to the database.")