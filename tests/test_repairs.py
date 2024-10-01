# tests/test_repairs.py
import unittest
from app import create_app
from extensions import db
from models.repairs import Repair
import uuid

class RepairTestCase(unittest.TestCase):
    def setUp(self):
        test_config = {
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'WTF_CSRF_ENABLED': False
        }
        self.app = create_app(test_config)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    # def tearDown(self):
    #     with self.app.app_context():
    #         db.session.remove()
    #         db.drop_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.engine.execute('DROP TABLE IF EXISTS repair_logs CASCADE;')
            db.engine.execute('DROP TABLE IF EXISTS repairs CASCADE;')


    tearDown()

    def test_get_all_repairs(self):
        with self.app.app_context():
            order_number_1 = str(uuid.uuid4())[:8]
            order_number_2 = str(uuid.uuid4())[:8]

            repair1 = Repair(order_number=order_number_1, device_model='MacBook Pro', serial_number='SN001', reported_issue='Screen issue', status='En progreso')
            repair2 = Repair(order_number=order_number_2, device_model='MacBook Air', serial_number='SN002', reported_issue='Battery issue', status='Pausada')
            db.session.add_all([repair1, repair2])
            db.session.commit()

            response = self.client.get('/repairs')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()

            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['order_number'], order_number_1)
            self.assertEqual(data[1]['order_number'], order_number_2)

    def test_add_repair(self):
        new_order_number = str(uuid.uuid4())[:8]
        new_repair = {
            "order_number": new_order_number,
            "device_model": "MacBook Pro 2021",
            "serial_number": "SN1234567890",
            "reported_issue": "Keyboard issue",
            "status": "En progreso",
            "user_id": 1
        }

        response = self.client.post('/repairs', json=new_repair)
        self.assertEqual(response.status_code, 201)

        response = self.client.get('/repairs')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['order_number'], new_order_number)
