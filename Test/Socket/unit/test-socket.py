from time import time
from unittest import TestCase
from app import socketio, app

class TestSocket(TestCase):
    def setUp(self):
        self.client = socketio.test_client(app)

    def tearDown(self):
        self.client.disconnect()

    def test_ping_server(self):
        # Ask server ping
        self.client.emit('ping_server')

        # Waiting for response
        response = self.client.get_received()

        # Si le timestamps est un float c'est bon
        self.assertIsInstance(response[0]['args'][0]['timestamp'], float, "Error: 'timestamp' must be a float!")

    def test_hearbeat(self):
        # define HeartBeat Data
        data_to_send = {"date": time(), "module_name": "test-olympe", "module_key": "546ee675-4011-41ba-84ab-56340f2ab815"}

        # Empty responses
        self.client.emit("heartbeat", data_to_send)

        response = self.client.get_received()
