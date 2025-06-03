from starter_code.models.user import UserModel
from starter_code.models.item import ItemModel
from starter_code.models.store import StoreModel
from starter_code.tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_request = client.post('/auth', 
                                            data=json.dumps({'username': 'test', 'password': '1234'}),
                                            headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = f'JWT {auth_token}'
        
    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test')
                self.assertEqual(resp.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                resp = client.get('/item/test', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 200)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                resp = client.delete('/item/test')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'Item deleted.'},
                                    json.loads(resp.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                resp = client.post('/item/test', data=json.dumps({'price': 17.99, 'store_id': 1}),
                                    headers={'Content-Type': 'application/json'})

                self.assertEqual(resp.status_code, 201)
                self.assertDictEqual({'name': 'test', 'price': 17.99},
                                    json.loads(resp.data))

    def test_create_duplicate(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()

                resp = client.post('/item/test', data=json.dumps({'price': 17.99, 'store_id': 1}),
                                    headers={'Content-Type': 'application/json'})

                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual({'message': 'An item with name \'test\' already exists.'},
                                    json.loads(resp.data))

    def test_put_item(self): # create item if the item does not exist
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.put('/item/test', data=json.dumps({'price': 17.99, 'store_id': 1}),
                                headers={'Content-Type': 'application/json'})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertDictEqual({'name': 'test', 'price': 17.99},
                                    json.loads(resp.data))

    def test_put_update_item(self): # update an existing item
         with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 5.99, 1).save_to_db()

                self.assertEqual(ItemModel.find_by_name('test').price, 5.99)

                resp = client.put('/item/test', data=json.dumps({'price': 17.99, 'store_id': 1}),
                                headers={'Content-Type': 'application/json'})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertDictEqual({'name': 'test', 'price': 17.99},
                                    json.loads(resp.data))
    
    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 5.99, 1).save_to_db()

                resp = client.get('/items')

                self.assertDictEqual({'items': [{'name': 'test', 'price': 5.99}]},
                                    json.loads(resp.data))