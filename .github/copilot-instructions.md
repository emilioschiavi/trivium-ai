# Trivium AI - GitHub Copilot Development Instructions

## Project Context

**Project Name**: Trivium AI  
**Type**: REST API Development  
**Tech Stack**: Python, FastAPI, Django  
**Testing**: pytest

## Current Project: Swiss Weather Sport Planner

This workspace currently contains a Django web application for weather-based outdoor sport recommendations in Reinach BL, Switzerland. This is a personal learning project for a user with good Python experience but no Django experience.

**Product Requirements**: All detailed requirements are documented in `PRD.md` in the root directory. Always reference this document when providing suggestions or answering questions about project features, technical architecture, or user requirements.

**Project Roadmap**: The complete development timeline, milestones, and implementation phases are documented in `ROADMAP.md`. Reference this for understanding the project structure, implementation order, and current development phase.

**Architecture Documentation**: System architecture, component designs, and technical diagrams are documented in `ARCHITECTURE.md`. Reference this for understanding system design and data flows.

### Progress Tracking
- **Automatic Checkbox Updates**: When executing tasks from `ROADMAP.md`, automatically update checkboxes (`- [ ]` to `- [x]`) as tasks are completed, milestones achieved, deliverables verified, and features pass testing.
- Update the roadmap in real-time to provide a live progress tracker througut development.

### Key Project Details
- **Backend**: Django (Python)
- **Frontend**: HTML, JavaScript, Pure CSS (no frameworks)
- **API**: OpenWeatherMap API
- **Storage**: Local storage (browser-based)
- **Hosting**: Local development server
- **Target User**: Non-tech-savvy adults planning cycling and running activities
- **Location**: Reinach BL, Switzerland only

## Project Overview

Trivium AI is a REST API-focused project utilizing modern Python frameworks. The system provides RESTful endpoints for various services and follows best practices for API development.

## Architecture Summary

### System Architecture
- **API Layer**: RESTful endpoints built with FastAPI and Django
- **Business Logic**: Python services following PEP8 standards
- **Testing Layer**: Comprehensive test coverage using pytest
- **Data Layer**: Database integration with ORM support

### Key Technologies
- **Backend**: Python 3.x, FastAPI, Django
- **Testing**: pytest
- **Code Style**: PEP8 (120 character line length)

## Coding Standards

### Python Style
- **Style Guide**: PEP 8 (strictly followed)
- **Line Length**: 120 characters maximum
- **String Formatting**: Use `.format()` method (not f-strings or %)
- **Frameworks**: FastAPI for async APIs, Django for traditional web applications
- **Code Quality**: Clean, readable code with appropriate spacing

#### String Formatting Examples
```python
# Correct - Use .format()
result = "Value: {}, Another: {}".format(param1, param2)
message = "User {} logged in at {}".format(username, timestamp)

# Incorrect - Don't use f-strings
result = f"Value: {param1}, Another: {param2}"  # ❌ Avoid

# Incorrect - Don't use % formatting
result = "Value: %s, Another: %s" % (param1, param2)  # ❌ Avoid
```

### Testing Standards
- **Testing Framework**: pytest
- **Test Coverage**: Focus on both unit and integration tests
- **Test Naming**: `test_<functionality>` format with descriptive names
- **Test Documentation**: Include docstrings for test functions
- **Test Location**: tests/ directory mirroring source structure

### Git Workflow
### Git Workflow
- **Development Approach**: Feature-driven development
- **Branch Naming**: `[type]/[issue-number]-[description]`
  - Types: `feature`, `fix`, `docs`, `refactor`, `test`, `chore`
- **Commit Format**: [Conventional Commits](https://www.conventionalcommits.org/)
  - Format: `type(scope): description`
  - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- **Merge Strategy**: Squash and merge
- **Issue Linking**: Reference issues with `Closes #123` or `Fixes #123`

## Development Workflow

### Feature Development Process
1. Create GitHub issue for the feature/fix
2. Create feature branch from `main` branch
3. Implement feature incrementally
4. Write tests alongside implementation
5. Update documentation during development
6. Create PR with completed checklist
7. Code review and address feedback
8. Merge after approval

### Key Principles
- Build features incrementally and test continuously
- Keep features small and focused
- All configuration via .env files (never hardcode)
- Follow PEP8 strictly with 120 character line limit
- Use `.format()` for all string formatting

### Project-Specific Rules
- Always follow PEP8 coding standards
- API responses must be well-structured and consistent
- All database queries must use ORM (avoid raw SQL)
- User inputs must be validated (use Pydantic for FastAPI)
- Include proper error handling in all endpoints

## Copilot Usage Guidelines

### For Python Code

When writing Python code:

1. **Follow PEP8 with 120 character line length**:
```python
def calculate_user_statistics(user_id, start_date, end_date, include_details=False):
    """
    Calculate statistics for a user within a date range.
    
    Args:
        user_id: The ID of the user
        start_date: Start of date range
        end_date: End of date range
        include_details: Whether to include detailed breakdown
    
    Returns:
        Dictionary containing user statistics
    """
    query = "SELECT * FROM stats WHERE user_id = {} AND date BETWEEN {} and {}".format(
        user_id, start_date, end_date
    )
    return execute_query(query)
```

2. **Include comprehensive docstrings**:
```python
def process_payment(amount, currency, payment_method):
    """
    Process a payment transaction.
    
    Args:
        amount (Decimal): The payment amount
        currency (str): Three-letter currency code (e.g., 'USD')
        payment_method (str): Payment method identifier
    
    Returns:
        dict: Payment result with transaction ID and status
        
    Raises:
        ValueError: If amount is negative or currency is invalid
        PaymentError: If payment processing fails
    """
    if amount <= 0:
        raise ValueError("Amount must be positive")
    # Processing logic here
    return {"transaction_id": "123", "status": "success"}
```

3. **Use Pydantic for data validation (FastAPI)**:
```python
from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    age: Optional[int] = Field(None, ge=0, le=150)
    
    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "age": 30
            }
        }
```

4. **Structured error handling**:
```python
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def fetch_user_data(user_id: int) -> Optional[dict]:
    """
    Fetch user data from the database.
    
    Args:
        user_id: The user's ID
        
    Returns:
        User data dictionary or None if not found
    """
    try:
        user = User.objects.get(id=user_id)
        return user.to_dict()
    except User.DoesNotExist:
        logger.warning("User with id {} not found".format(user_id))
        return None
    except DatabaseError as e:
        logger.error("Database error fetching user {}: {}".format(user_id, str(e)))
        raise
    except Exception as e:
        logger.error("Unexpected error fetching user {}: {}".format(user_id, str(e)))
        raise
```

### For FastAPI Endpoints

When creating FastAPI endpoints:

1. **Use async/await with proper type hints**:
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List

router = APIRouter()

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a user by ID.
    
    Args:
        user_id: The ID of the user to retrieve
        db: Database session dependency
        
    Returns:
        UserResponse: User data
        
    Raises:
        HTTPException: 404 if user not found
    """
    user = await db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User with id {} not found".format(user_id))
    return user
```

2. **Proper error handling**:
```python
from fastapi import HTTPException, status

@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    try:
        db_user = User(**user.dict())
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
```

### For Django Views

When creating Django views:

1. **Use class-based or function-based views appropriately**:
```python
from django.views import View
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

class UserDetailView(View):
    """
    Handle user detail operations.
    """
    
    def get(self, request, user_id):
        """
        Retrieve user details.
        """
        try:
            user = User.objects.get(id=user_id)
            return JsonResponse({
                "id": user.id,
                "username": user.username,
                "email": user.email
            })
        except User.DoesNotExist:
            return JsonResponse(
                {"error": "User not found"},
                status=404
            )
```

### For Database Models

When creating database models:

1. **Django ORM models**:
```python
from django.db import models

class User(models.Model):
    """
    User model for storing user information.
    """
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "users"
        ordering = ["-created_at"]
    
    def __str__(self):
        return "User: {}".format(self.username)
```

2. **Generate and apply migrations**:
```bash
# Django migrations
python manage.py makemigrations
python manage.py migrate
```

### API Design

When creating REST API endpoints:

1. **Follow RESTful conventions**:
```python
# FastAPI example
from fastapi import APIRouter, status

router = APIRouter(prefix="/api/v1")

# GET - Retrieve resource(s)
@router.get("/users", response_model=List[UserResponse])
async def list_users():
    """List all users."""
    pass

# GET - Retrieve single resource
@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Get user by ID."""
    pass

# POST - Create resource
@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Create a new user."""
    pass

# PUT - Update resource
@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserUpdate):
    """Update user by ID."""
    pass

# DELETE - Delete resource
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    """Delete user by ID."""
    pass
```

2. **Use consistent response format**:
```python
# Success response
{
    "data": {...},
    "message": "Operation successful",
    "status": "success"
}

# Error response
{
    "error": {
        "code": "USER_NOT_FOUND",
        "message": "User with id 123 not found",
        "details": {}
    },
    "status": "error"
}
```

3. **Always include validation and error handling**:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

@router.post("/protected-resource")
async def protected_endpoint(
    data: RequestModel,
    token: str = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Protected endpoint with authentication and validation.
    """
    # Validate token
    user = await validate_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Process request
    try:
        result = await process_data(data, db)
        return {"data": result, "status": "success"}
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Validation error: {}".format(str(e))
        )
```

## Project Structure

```
[PROJECT_ROOT]/
├── [directory]/
│   ├── [subdirectory]/
│   │   └── [file patterns]
│   └── [purpose]
├── [directory]/
│   ├── [subdirectory]/
│   └── [purpose]
├── [directory]/
│   └── [purpose]
├── [config files]
└── [documentation]
```

### File Organization Rules
- [Rule 1: e.g., "Each module should have a single responsibility"]
- [Rule 2: e.g., "Test files mirror source file structure"]
- [Rule 3: e.g., "Shared utilities go in /shared or /common"]
- [Rule 4: e.g., "Feature folders contain all related files (component, styles, tests)"]

## Environment & Configuration

### Environment Variables
All configuration managed through `.env` files:
- `.env.example` - Template (committed to repo)
- `.env` - Local configuration (never committed, in .gitignore)

### Required Variables
```bash
# [Service/Component Name]
[VAR_NAME]=[description]
[VAR_NAME]=[description]

# [Another Service]
[VAR_NAME]=[description]
[VAR_NAME]=[description]
```

### Development Commands

```bash
# Setup
make setup              # Initial environment setup

# Development
make build             # Build containers/compile code
make up                # Start services
make down              # Stop services
make restart           # Restart services

# Testing
make test              # Run all tests
make test-[component]  # Run specific test suite
make coverage          # Generate coverage report

# Code Quality
make lint              # Run linters
make format            # Format code
make typecheck         # Run type checker

# Utilities
make logs              # View logs
make clean             # Clean build artifacts
make migrate           # Run database migrations
```

## Common Patterns

### [Pattern 1 Name]
```[language]
[Code example with explanation]
```

### [Pattern 2 Name]
```[language]
[Code example with explanation]
```

### [Pattern 3 Name]
```[language]
[Code example with explanation]
```

## Anti-Patterns to Avoid

### ❌ [Anti-pattern 1]
```[language]
# Don't do this:
[Bad example]
```

```[language]
# Do this instead:
[Good example]
```

### ❌ [Anti-pattern 2]
```[language]
# Don't do this:
[Bad example]
```

```[language]
# Do this instead:
[Good example]
```

## Debugging & Troubleshooting

### Common Issues

**Issue**: [Common problem description]
```bash
# Diagnostic command
[command to identify issue]

# Solution
[command to fix issue]
```

**Issue**: [Another common problem]
```bash
# Diagnostic command
[command to identify issue]

# Solution
[command to fix issue]
```

## Performance Considerations

- [Performance guideline 1]
- [Performance guideline 2]
- [Performance guideline 3]

## Security Guidelines

- [Security practice 1]
- [Security practice 2]
- [Security practice 3]
- [Security practice 4]

## Communication Preferences

- **Explanation Detail Level**: Moderate
  - Provide context and reasoning for decisions
  - Don't be overly verbose
  - Include practical examples when helpful
  - Balance thoroughness with brevity

## Key Reminders

### Always Follow:
- ✅ PEP8 coding standards strictly
- ✅ 120 character line length maximum
- ✅ Use `.format()` for string formatting
- ✅ Write tests using pytest
- ✅ Include comprehensive docstrings
- ✅ Proper error handling in all code
- ✅ REST API best practices

### Never Do:
- ❌ Don't use f-strings (use `.format()` instead)
- ❌ Don't exceed 120 character line length
- ❌ Don't use % string formatting
- ❌ Don't hardcode configuration values
- ❌ Don't skip error handling
- ❌ Don't write code without tests

## Questions or Clarifications

For questions about these guidelines or project-specific decisions:
1. Check project documentation in `/docs`
2. Review closed issues and PRs for precedent
3. Refer to this copilot-instructions.md file
4. Ensure all code follows PEP8 with 120 character limit

---

**Last Updated**: 3 December 2025  
**Maintained By**: Trivium AI Team