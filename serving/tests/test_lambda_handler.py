import json
import unittest
from app import lambda_handler


class BasicTests(unittest.TestCase):
    def test_basic_path(self):
        lambda_handler({"body": json.dumps({"text": "example input"})}, None)

    def test_crash(self):
        self.assertRaises(BaseException, lambda_handler, {"body": json.dumps({"not_the_right_one": "example input"})}, None)


if __name__ == '__main__':
    unittest.main()
