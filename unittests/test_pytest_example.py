import logging
import pytest

from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class TestPytestExample:

    def setup_method(self):
        """
        Pytest setup method
        """
        LOGGER.warning("Setup method")

    @classmethod
    def setup_class(cls):
        """
        Pytest setup class
        """
        LOGGER.warning("Setup Class")

    def teardown_method(self):
        """
        Pytest teardown method
        """
        LOGGER.warning("Teardown method")

    @classmethod
    def teardown_class(cls):
        """
        Pytest teardown class
        """
        LOGGER.warning("Teardown class")


    def test_one(self):
        """
        test one
        """
        LOGGER.warning("Test one")

    @pytest.mark.acceptance
    def test_two(self):
        """
        test two
        """
        LOGGER.warning("Test two")
