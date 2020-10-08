from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandsTestCase(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""

        with patch('django.db.utils.ConnectionHandler.__getitem__') as item:
            item.return_value = True
            call_command('wait_for_db')
            # Check that the getitem called once
            self.assertEqual(item.call_count, 1)

    @patch('time.sleep', return_value=True)
    # Same as line #13 and pass item object as parameter, in the function
    # Parameter name: "ts"
    def test_wait_for_db(self, ts):
        """Test waiting for db"""

        with patch('django.db.utils.ConnectionHandler.__getitem__') as item:
            # 5 times it will raise the OperationalError,
            # 6th time won't raise an Error and will return.
            item.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(item.call_count, 6)
