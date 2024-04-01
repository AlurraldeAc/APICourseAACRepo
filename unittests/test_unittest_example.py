import logging

import unittest

from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

class TestUnitTestExample(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Setup class
        """
        LOGGER.warning("Setup Class")

    def setUp(self):
        """
        setup method
        """
        LOGGER.warning("Setup method")

    def tearDown(self):
        """
        teardown method
        """
        LOGGER.warning("Teardown method")

    @classmethod
    def tearDownClass(cls):
        """
        Teardown class
        """
        LOGGER.warning("Teardown class")

    def test_one(self):
        """
        test ones
        """
        LOGGER.warning("Test one")

    def test_two(self):
        """
        test two
        """
        LOGGER.warning("Test two")

    def test_three(self):
        """
        test three
        """
        LOGGER.warning("Test three")
