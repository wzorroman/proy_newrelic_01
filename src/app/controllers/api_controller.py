from flask import Blueprint, request, jsonify
import time
import newrelic.agent
from app.services.api_service import ApiService
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "service": "flask-newrelic-demo"
    })

@api_bp.route('/api/data', methods=['GET'])
@newrelic.agent.background_task()
def get_data():
    """Get processed data from external API"""
    try:
        # Record custom metric
        newrelic.agent.record_custom_metric('Custom/DataRequest', 1)

        # Get external data
        external_data = ApiService.get_external_data()

        # Process data
        processed_data = ApiService.process_data(external_data)

        logger.info("Data processed successfully")

        return jsonify({
            "success": True,
            "data": processed_data,
            "metadata": {
                "processed_at": time.time(),
                "source": "external_api"
            }
        })

    except Exception as e:
        logger.error(f"Error in get_data: {e}")
        newrelic.agent.record_exception()
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500

@api_bp.route('/api/users', methods=['POST'])
@newrelic.agent.background_task()
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()

        if not data or 'username' not in data or 'email' not in data:
            return jsonify({
                "success": False,
                "error": "Username and email are required"
            }), 400

        user_data = ApiService.create_user_data(
            data['username'],
            data['email']
        )

        # Record custom event
        newrelic.agent.record_custom_event('UserCreated', {
            'username': data['username'],
            'email': data['email']
        })

        logger.info(f"User created: {data['username']}")

        return jsonify({
            "success": True,
            "user": user_data,
            "message": "User created successfully"
        }), 201

    except Exception as e:
        logger.error(f"Error creating user: {e}")
        newrelic.agent.record_exception()
        return jsonify({
            "success": False,
            "error": "Failed to create user"
        }), 500

@api_bp.route('/api/slow-operation', methods=['GET'])
@newrelic.agent.background_task()
def slow_operation():
    """Simulate a slow operation for monitoring"""
    start_time = time.time()

    # Simulate heavy processing
    time.sleep(2)

    processing_time = time.time() - start_time

    # Record custom metric with processing time
    newrelic.agent.record_custom_metric('Custom/SlowOperationTime', processing_time)

    return jsonify({
        "success": True,
        "message": "Slow operation completed",
        "processing_time": processing_time
    })
