from rest_framework.test import APITestCase


class GameAPITestCase(APITestCase):
    """Base test case for game API tests.
    
    This class sets up the necessary environment for testing game-related API endpoints.
    It can be extended by other test cases to inherit common setup and utility methods.
    """
    
    def setUp(self):
        """Set up the test environment."""
        # Initialize any common data or state needed for tests here
        pass

    def tearDown(self):
        """Clean up after tests."""
        # Perform any necessary cleanup after tests here
        pass