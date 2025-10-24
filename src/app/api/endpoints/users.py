from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import User, get_db
from app.models.schemas import UserCreate, UserResponse, UserOperationResponse
from app.utils.logger import setup_logger
from app.utils.newrelic_monitor import NewRelicMonitor
from app.dependencies.dependencies import get_common_parameters

logger = setup_logger(__name__)
router = APIRouter()

@router.post(
    "/users",
    response_model=UserOperationResponse,
    summary="Create User",
    description="Crear un nuevo usuario en el sistema",
    tags=["users"],
    status_code=201
)
async def create_user(
    user: UserCreate,
    common_params: dict = Depends(get_common_parameters)
):
    """Create a new user"""
    try:
        NewRelicMonitor.set_transaction_name("UserCreation")
        NewRelicMonitor.add_custom_attribute('endpoint', 'create_user')
        NewRelicMonitor.add_custom_attribute('username', user.username)

        db = common_params["db"]

        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.username == user.username) | (User.email == user.email)
        ).first()

        if existing_user:
            error_msg = "Username or email already exists"
            logger.warning(f"User creation failed: {error_msg}")

            NewRelicMonitor.record_custom_metric('Custom/UserCreationFailed', 1)
            NewRelicMonitor.add_custom_attribute('creation_status', 'failed_duplicate')

            raise HTTPException(status_code=400, detail=error_msg)

        # Create new user
        db_user = User(username=user.username, email=user.email)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Record custom event y métricas
        NewRelicMonitor.record_custom_event('UserCreated', {
            'username': user.username,
            'email': user.email,
            'user_id': db_user.id
        })
        NewRelicMonitor.record_custom_metric('Custom/UserCreated', 1)
        NewRelicMonitor.add_custom_attribute('user_id', str(db_user.id))
        NewRelicMonitor.add_custom_attribute('creation_status', 'success')

        logger.info(f"User created successfully: {user.username} (ID: {db_user.id})")

        return UserOperationResponse(
            success=True,
            user=db_user,
            message="User created successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating user: {e}")

        # Registrar error en NewRelic
        NewRelicMonitor.notice_error(e, {
            'endpoint': 'create_user',
            'operation': 'user_creation',
            'username': user.username,
            'error_type': 'database_error'
        })
        NewRelicMonitor.record_custom_metric('Custom/UserCreationError', 1)
        NewRelicMonitor.add_custom_attribute('creation_status', 'failed_error')

        raise HTTPException(status_code=500, detail="Failed to create user")

@router.get(
    "/users",
    response_model=list[UserResponse],
    summary="Get Users",
    description="Obtener lista de todos los usuarios",
    tags=["users"]
)
async def get_users(common_params: dict = Depends(get_common_parameters)):
    """Get all users"""
    try:
        NewRelicMonitor.add_custom_attribute('endpoint', 'get_users')

        db = common_params["db"]
        users = db.query(User).all()

        # Record metric
        user_count = len(users)
        NewRelicMonitor.record_custom_metric('Custom/UsersListed', user_count)
        NewRelicMonitor.add_custom_attribute('user_count', str(user_count))

        logger.info(f"Retrieved {user_count} users from database")

        return users

    except Exception as e:
        logger.error(f"Error getting users: {e}")

        NewRelicMonitor.notice_error(e, {
            'endpoint': 'get_users',
            'operation': 'list_users',
            'error_type': 'database_query_error'
        })

        raise HTTPException(status_code=500, detail="Failed to get users")
