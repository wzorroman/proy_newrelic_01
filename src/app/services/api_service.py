import requests
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class ApiService:
    """Service layer for API operations"""

    @staticmethod
    def get_external_data():
        """Simulate external API call"""
        try:
            # Simulate API call
            response = requests.get('https://jsonplaceholder.typicode.com/posts/1', timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"External API call failed: {e}")
            return {"error": "External service unavailable"}

    @staticmethod
    def process_data(data):
        """Process data with business logic"""
        if isinstance(data, dict) and 'title' in data:
            data['processed'] = True
            data['title_upper'] = data['title'].upper()
        return data

    @staticmethod
    def create_user_data(username, email):
        """Create user data structure"""
        return {
            "username": username,
            "email": email,
            "status": "active"
        }
