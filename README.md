# Code Checker: AI-Powered Programming Assessment Platform

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-4.1-green.svg)](https://www.djangoproject.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-lightgrey)](https://openai.com/)

Code Checker is an advanced programming assessment platform powered by OpenAI's GPT models to generate, evaluate, and provide feedback on programming challenges across multiple languages and difficulty levels.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Setup & Installation](#setup--installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Development](#development)
- [Production Deployment](#production-deployment)
- [Testing](#testing)
- [Troubleshooting & Common Issues](#troubleshooting--common-issues)
- [Contributing](#contributing)
- [License](#license)

## 🔍 Overview

Code Checker is a Django-based web application that leverages OpenAI's GPT models to provide a comprehensive programming assessment platform. The system can generate unique coding questions, theory questions, and multiple-choice questions (MCQs) across various programming languages and difficulty levels. It evaluates submitted code, provides feedback, and tracks user progress.

The platform uses vector embeddings for semantic similarity checks to prevent duplicate questions and features a robust leaderboard system to encourage friendly competition among users.

## ✨ Features

- **User Authentication & Management**
  - Email-based signup with verification
  - Password reset and change functionality
  - Google OAuth integration
  - User profile management

- **Question Generation**
  - AI-generated coding challenges (with automatic test case creation)
  - Theory questions for conceptual understanding
  - Multiple-choice questions for quick assessments
  - Support for multiple programming languages
  - Three difficulty levels: Easy, Medium, Hard
  - Semantic duplicate detection using OpenAI embeddings

- **Quiz System**
  - Create customized quizzes based on language and difficulty
  - Track quiz progress and completion
  - Automatic or manual quiz completion
  - View detailed quiz history

- **Code Evaluation**
  - Syntax validation for submitted code
  - Secure code execution in controlled environments
  - Testing against predefined test cases
  - AI-powered feedback for incorrect submissions

- **Progress Tracking & Leaderboards**
  - Individual progress tracking
  - Global leaderboards based on accuracy
  - Quiz-specific leaderboards
  - User submission history and review
  - Friend comparison feature

## 🏗️ System Architecture

The system follows a standard Django architecture with the following key components:

### Core Components

1. **Authentication Module** (built on django-rest-authemail and social-auth)
   - Handles user signup, verification, and login
   - Supports OAuth integration for Google login

2. **Question Generation System** 
   - Uses OpenAI GPT-4 to generate programming questions
   - Implements semantic similarity checks using embeddings
   - Supports multiple question types (coding, theory, MCQ)

3. **Quiz Management System**
   - Creates and manages quizzes
   - Tracks quiz progress and completion
   - Handles question sequencing and scoring

4. **Code Execution & Evaluation System**
   - Validates code syntax
   - Runs code against test cases
   - Provides feedback on submissions

5. **Progress & Leaderboard System**
   - Tracks individual and comparative progress
   - Generates leaderboards based on various metrics

### Database Models

- `MyUser`: Extended user model for authentication
- `ProgrammingLanguage`: Supported programming languages
- `ExpertiseLevel`: Difficulty levels for questions
- `QuizQuestion`, `TheoryQuestion`, `MCQQuestion`: Different question types
- `TestCase`: Input/output test cases for coding questions
- `QuestionEmbedding`: Vector embeddings for semantic similarity checks
- `Quiz` and `QuizQuestionResponse`: Quiz management and tracking
- `UserProgress` and `UserSubmission`: User performance tracking

## 🛠️ Setup & Installation

### Prerequisites

- Python 3.8+
- PostgreSQL with pgvector extension (recommended for production)
- OpenAI API key

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/code-checker.git
   cd code-checker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
    source venv/bin/activate
```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a .env file based on env-sample**
   ```bash
   cp env-sample .env
   ```

6. **Update the .env file with your configuration**
   - Add your OpenAI API key
   - Configure database settings
   - Set up email settings for verification
   - Add Google OAuth credentials (if using)

7. **Apply migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

8. **Run the server**
   ```bash
   python manage.py runserver
   ```

## ⚙️ Configuration

### Environment Variables

Edit the `.env` file with the following configurations:

```
# Django Settings
SECRET_KEY=your_secret_key

# Database Settings
DB_ENGINE=django.db.backends.postgresql
DB_NAME=code_checker_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432


# OpenAI Settings
open_ai_key=your_openai_api_key
```

## 🗃️ Database Setup

The application can work with SQLite (default for development) or PostgreSQL (recommended for production).

### PostgreSQL Setup with pgvector (Recommended)

1. **Install PostgreSQL and pgvector extension**

2. **Create a database**
   ```sql
   CREATE DATABASE code_checker_db;
   ```

3. **Enable pgvector extension**
   ```sql
   \c code_checker_db
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

4. **Update .env file with PostgreSQL settings**
   ```
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=code_checker_db
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

### Initial Data

To create initial programming languages and expertise levels:

```bash
python manage.py shell
```

```python
from interface.models import ProgrammingLanguage, ExpertiseLevel

# Add programming languages
languages = ["Python", "JavaScript", "Java", "C++", "C#"]
for lang in languages:
    ProgrammingLanguage.objects.get_or_create(name=lang)

# Add expertise levels
levels = ["Easy", "Medium", "Hard"]
for level in levels:
    ExpertiseLevel.objects.get_or_create(level=level)
```

## 🚀 Usage

### Starting the Server

```bash
python manage.py runserver
```

### Generating Embeddings for Questions

To enable semantic similarity checks, generate embeddings for existing questions:

```bash
python manage.py generate_embeddings --types all
```

Options:
- `--types`: Question types to process (coding,theory,mcq,all)
- `--batch-size`: Number of questions per batch (default: 50)
- `--sleep-time`: Wait time between batches in seconds (default: 10.0)
- `--force`: Regenerate embeddings for all questions

## 🔌 API Endpoints

> **Authentication Note**: Most endpoints require a JWT authentication token. Include the token in the request header as:
> ```
> Authorization: Bearer <your_jwt_token>
> ```
> 
> To obtain this token, use the `/api/token/` endpoint.

### Authentication

- `POST /api/token/`
  - **Description**: Obtain a JWT token for authentication
  - **Request Body**:
    ```json
    {
      "email": "user@example.com",
      "password": "your_password"
    }
    ```
  - **Response**:
    ```json
    {
      "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
    ```
  - **Authentication**: None required

- `POST /api/token/refresh/`
  - **Description**: Refresh an expired JWT token
  - **Request Body**:
    ```json
    {
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
    ```
  - **Response**:
    ```json
    {
      "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
    ```
  - **Authentication**: None required

- `POST /api/signup/`
  - **Description**: Register a new user
  - **Request Body**:
    ```json
    {
      "email": "user@example.com",
      "password": "secure_password",
      "first_name": "John",
      "last_name": "Doe"
    }
    ```
  - **Response**:
    ```json
    {
      "detail": "Verification email sent."
    }
    ```
  - **Authentication**: None required

- `POST /api/signup/verify/`
  - **Description**: Verify email after registration
  - **Request Body**:
    ```json
    {
      "code": "verification_code_from_email"
    }
    ```
  - **Response**:
    ```json
    {
      "detail": "Email verified successfully."
    }
    ```
  - **Authentication**: None required

- `POST /api/password/reset/`
  - **Description**: Request password reset
  - **Request Body**:
    ```json
    {
      "email": "user@example.com"
    }
    ```
  - **Response**:
    ```json
    {
      "detail": "Password reset email sent."
    }
    ```
  - **Authentication**: None required

- `POST /api/password/reset/verified/`
  - **Description**: Confirm password reset
  - **Request Body**:
    ```json
    {
      "code": "reset_code_from_email",
      "password": "new_secure_password"
    }
    ```
  - **Response**:
    ```json
    {
      "detail": "Password reset successfully."
    }
    ```
  - **Authentication**: None required

- `POST /api/password/change/`
  - **Description**: Change password (for authenticated users)
  - **Request Body**:
    ```json
    {
      "password": "current_password",
      "new_password": "new_secure_password"
    }
    ```
  - **Response**:
    ```json
    {
      "detail": "Password changed successfully."
    }
    ```
  - **Authentication**: JWT token required

- `GET /api/google-login/`
  - **Description**: Start Google OAuth flow
  - **Response**: Redirects to Google login page
  - **Authentication**: None required

- `GET /api/google-callback/`
  - **Description**: Google OAuth callback
  - **Response**: Returns JWT tokens after successful Google authentication
  - **Authentication**: None required (handled by OAuth flow)

### Question Generation

- `POST /api/generate-quiz-question/`
  - **Description**: Generate a coding question
  - **Request Body**:
    ```json
    {
      "language": 1,
      "level": 2
    }
    ```
  - **Response**:
    ```json
    {
      "id": 123,
      "question_text": "Write a function to find the longest palindromic substring...",
      "programming_language": {
        "id": 1,
        "name": "Python"
      },
      "expertise_level": {
        "id": 2,
        "level": "Medium"
      },
      "test_cases": [
        {
          "input_data": "babad",
          "expected_output": "bab"
        }
      ]
    }
    ```
  - **Authentication**: JWT token required

- `POST /api/generate-mcq-question/`
  - **Description**: Generate a multiple-choice question
  - **Request Body**:
    ```json
    {
      "language": 2,
      "level": 1
    }
    ```
  - **Response**:
    ```json
    {
      "id": 456,
      "question_text": "Which of the following is NOT a JavaScript data type?",
      "option_a": "String",
      "option_b": "Boolean",
      "option_c": "Float",
      "option_d": "Number",
      "programming_language": {
        "id": 2,
        "name": "JavaScript"
      },
      "expertise_level": {
        "id": 1,
        "level": "Easy"
      }
    }
    ```
  - **Authentication**: JWT token required

- `POST /api/generate-theory-question/`
  - **Description**: Generate a theory question
  - **Request Body**:
    ```json
    {
      "language": 3,
      "level": 3
    }
    ```
  - **Response**:
    ```json
    {
      "id": 789,
      "question_text": "Explain the differences between interface and abstract class in Java...",
      "model_answer": "An interface in Java is a blueprint of a class that contains...",
      "programming_language": {
        "id": 3,
        "name": "Java"
      },
      "expertise_level": {
        "id": 3,
        "level": "Hard"
      }
    }
    ```
  - **Authentication**: JWT token required

### Quiz Management

- `POST /api/create-quiz/`
  - **Description**: Create a new quiz
  - **Request Body**:
    ```json
    {
      "language": 1,
      "level": 2,
      "total_questions": 5,
      "mcq_percentage": 20,
      "theory_percentage": 20,
      "coding_percentage": 60
    }
    ```
  - **Response**:
    ```json
    {
      "id": 123,
      "language": {
        "id": 1,
        "name": "Python"
      },
      "level": {
        "id": 2,
        "level": "Medium"
      },
      "total_questions": 5,
      "mcq_percentage": 20,
      "theory_percentage": 20,
      "coding_percentage": 60,
      "created_at": "2023-04-15T14:30:00Z",
      "status": "in_progress"
    }
    ```
  - **Authentication**: JWT token required

- `GET /api/quiz/<quiz_id>/next-question/`
  - **Description**: Get the next question in a quiz
  - **Path Parameters**: `quiz_id` - ID of the quiz
  - **Response**:
    ```json
    {
      "id": 456,
      "question_type": "coding",
      "question_text": "Write a function to find the longest palindromic substring...",
      "programming_language": {
        "id": 1,
        "name": "Python"
      },
      "expertise_level": {
        "id": 2,
        "level": "Medium"
      },
      "test_cases": [
        {
          "input_data": "babad",
          "expected_output": "bab"
        }
      ],
      "question_number": 2,
      "total_questions": 5
    }
    ```
  - **Authentication**: JWT token required

- `POST /api/quiz/<quiz_id>/submit-answer/`
  - **Description**: Submit an answer for a quiz question
  - **Path Parameters**: `quiz_id` - ID of the quiz
  - **Request Body** (for coding question):
    ```json
    {
      "question_id": 456,
      "answer": "def longest_palindrome(s):\n    # Solution code here",
      "question_type": "coding",
      "start_time": "2023-04-15T14:35:00Z"
    }
    ```
  - **Request Body** (for MCQ question):
    ```json
    {
      "question_id": 457,
      "answer": "C",
      "question_type": "mcq",
      "start_time": "2023-04-15T14:40:00Z"
    }
    ```
  - **Request Body** (for theory question):
    ```json
    {
      "question_id": 458,
      "answer": "An interface in Java is a blueprint of a class...",
      "question_type": "theory",
      "start_time": "2023-04-15T14:45:00Z"
    }
    ```
  - **Response**:
    ```json
    {
      "correct": true,
      "feedback": "Your solution is correct and efficient!",
      "time_taken": 300,
      "is_last_question": false,
      "next_question_id": 459
    }
    ```
  - **Authentication**: JWT token required

- `POST /api/quiz/<quiz_id>/complete/`
  - **Description**: Complete a quiz
  - **Path Parameters**: `quiz_id` - ID of the quiz
  - **Response**:
    ```json
    {
      "quiz_id": 123,
      "score": 80,
      "total_questions": 5,
      "correct_answers": 4,
      "completion_time": 1500,
      "completed_at": "2023-04-15T15:00:00Z"
    }
    ```
  - **Authentication**: JWT token required

- `GET /api/quiz/<quiz_id>/details/`
  - **Description**: Get quiz details
  - **Path Parameters**: `quiz_id` - ID of the quiz
  - **Response**:
    ```json
    {
      "id": 123,
      "language": {
        "id": 1,
        "name": "Python"
      },
      "level": {
        "id": 2,
        "level": "Medium"
      },
      "total_questions": 5,
      "mcq_percentage": 20,
      "theory_percentage": 20,
      "coding_percentage": 60,
      "created_at": "2023-04-15T14:30:00Z",
      "completed_at": "2023-04-15T15:00:00Z",
      "status": "completed",
      "score": 80,
      "responses": [
        {
          "question_id": 456,
          "question_type": "coding",
          "correct": true,
          "time_taken": 300
        },
        // More responses...
      ]
    }
    ```
  - **Authentication**: JWT token required

- `GET /api/quiz-history/`
  - **Description**: Get user's quiz history
  - **Query Parameters**:
    - `page` (optional): Page number for pagination
    - `page_size` (optional): Number of results per page
  - **Response**:
    ```json
    {
      "count": 10,
      "next": "/api/quiz-history/?page=2",
      "previous": null,
      "results": [
        {
          "id": 123,
          "language": {
            "id": 1,
            "name": "Python"
          },
          "level": {
            "id": 2,
            "level": "Medium"
          },
          "total_questions": 5,
          "score": 80,
          "created_at": "2023-04-15T14:30:00Z",
          "completed_at": "2023-04-15T15:00:00Z",
          "status": "completed"
        },
        // More quizzes...
      ]
    }
    ```
  - **Authentication**: JWT token required

### Leaderboards & Progress

- `GET /api/leaderboard/`
  - **Description**: Get global leaderboard
  - **Query Parameters**:
    - `type` (optional): Metric type (accuracy, quiz_score), default is accuracy
    - `period` (optional): Time period (all, month, week), default is all
  - **Response**:
    ```json
    {
      "leaderboard": [
        {
          "user_id": 1,
          "username": "john_doe",
          "avatar": "https://example.com/avatar.jpg",
          "accuracy": 0.95,
          "total_attempts": 100,
          "correct_attempts": 95
        },
        // More users...
      ]
    }
    ```
  - **Authentication**: JWT token required

- `GET /api/quiz-leaderboard/`
  - **Description**: Get quiz-specific leaderboard
  - **Query Parameters**:
    - `language` (optional): Filter by programming language ID (e.g., 1 for Python)
    - `level` (optional): Filter by expertise level ID (e.g., 2 for Medium)
  - **Response**:
    ```json
    {
      "leaderboard": [
        {
          "user_id": 1,
          "username": "john_doe",
          "avatar": "https://example.com/avatar.jpg",
          "average_score": 92.5,
          "quizzes_completed": 8,
          "best_quiz_score": 100
        },
        // More users...
      ]
    }
    ```
  - **Authentication**: JWT token required

- `GET /api/user-submissions/`
  - **Description**: Get current user's submissions
  - **Query Parameters**:
    - `question_type` (optional): Filter by question type (coding, theory, mcq)
    - `language` (optional): Filter by programming language ID (e.g., 1 for Python)
    - `level` (optional): Filter by expertise level ID (e.g., 2 for Medium)
    - `page` (optional): Page number for pagination
  - **Response**:
    ```json
    {
      "count": 50,
      "next": "/api/user-submissions/?page=2",
      "previous": null,
      "results": [
        {
          "id": 123,
          "question_id": 456,
          "question_type": "coding",
          "question_text": "Write a function to find the longest palindromic substring...",
          "language": {
            "id": 1,
            "name": "Python"
          },
          "level": {
            "id": 2,
            "level": "Medium"
          },
          "submitted_at": "2023-04-15T14:55:00Z",
          "correct": true,
          "time_taken": 300
        },
        // More submissions...
      ]
    }
    ```
  - **Authentication**: JWT token required

- `GET /api/user-submissions/<user_id>/`
  - **Description**: Get specific user's submissions
  - **Path Parameters**: `user_id` - ID of the user to view
  - **Query Parameters**: Same as `/api/user-submissions/`
  - **Response**: Same format as `/api/user-submissions/`
  - **Authentication**: JWT token required

- `GET /api/compare/<friend_id>/`
  - **Description**: Compare progress with another user
  - **Path Parameters**: `friend_id` - ID of the user to compare with
  - **Response**:
    ```json
    {
      "current_user": {
        "id": 1,
        "username": "john_doe",
        "accuracy": 0.95,
        "total_attempts": 100,
        "quizzes_completed": 8,
        "average_quiz_score": 92.5
      },
      "friend": {
        "id": 2,
        "username": "jane_smith",
        "accuracy": 0.92,
        "total_attempts": 120,
        "quizzes_completed": 10,
        "average_quiz_score": 88.0
      },
      "comparison": {
        "accuracy_difference": 0.03,
        "attempts_difference": -20,
        "quizzes_difference": -2,
        "score_difference": 4.5
      },
      "languages": [
        {
          "language": {
            "id": 1,
            "name": "Python"
          },
          "current_user_accuracy": 0.97,
          "friend_accuracy": 0.90
        },
        // More languages...
      ]
    }
    ```
  - **Authentication**: JWT token required

### Answers Submission (Outside of Quiz)

- `POST /api/submit-answer/`
  - **Description**: Submit an answer for a coding question (outside of a quiz)
  - **Request Body**:
    ```json
    {
      "question_id": 456,
      "code": "def longest_palindrome(s):\n    # Solution code here"
    }
    ```
  - **Response**:
    ```json
    {
      "correct": true,
      "feedback": "Your solution is correct and efficient!",
      "time_taken": 300,
      "test_results": [
        {
          "input": "babad",
          "expected": "bab",
          "actual": "bab",
          "passed": true
        }
      ]
    }
    ```
  - **Authentication**: JWT token required

- `POST /api/submit-theory-answer/`
  - **Description**: Submit an answer for a theory question (outside of a quiz)
  - **Request Body**:
    ```json
    {
      "question_id": 789,
      "answer": "An interface in Java is a blueprint of a class..."
    }
    ```
  - **Response**:
    ```json
    {
      "correct": true,
      "feedback": "Your explanation covers all the key differences between interfaces and abstract classes.",
      "score": 0.95,
      "model_answer": "An interface in Java is a blueprint of a class that contains..."
    }
    ```
  - **Authentication**: JWT token required

## 💻 Development

### Running in Debug Mode

Set `DEBUG=1` in your `.env` file and run:

```bash
python manage.py runserver
```

### Code Structure

- `interface/`: Main application
  - `models.py`: Database models
  - `views.py`: API view functions
  - `urls.py`: URL routing
  - `generation_utils.py`: Question generation utilities
  - `embeddings.py`: Vector embedding utilities
  - `management/commands/`: Custom management commands

- `project/`: Django project configuration
  - `settings.py`: Global settings
  - `urls.py`: Root URL configuration

## 🌐 Production Deployment

### Using Gunicorn

```bash
gunicorn project.wsgi -b 0.0.0.0:8000
```

### Docker Deployment

1. **Copy deployment files**
   ```bash
cp deploy/dev/* .
```

2. **Start containers with database**
   ```bash
docker-compose -f docker-compose-sql.yml up -d
```
   
   Or without database if configured externally:
   ```bash
docker-compose -f docker-compose.yml up -d
```

3. **Stop containers**
   ```bash
docker-compose down
```

## 🧪 Testing

The project uses pytest for testing:

```bash
pytest
```

Test configuration is in `pytest.ini`. Environment variables for testing can be set in `.test.env`.

## 🔧 Troubleshooting & Common Issues

### OpenAI API Errors

If you encounter errors with OpenAI embeddings, check:
1. Your API key is valid and has sufficient credits
2. You're using the correct OpenAI library version
   - For v1.0.0+: Update `embeddings.py` to use the client-based approach
   - For older versions: Downgrade to v0.28 with `pip install openai==0.28`

### pgvector Format Issues

If you see errors like "invalid input syntax for type vector", ensure:
1. The embedding format uses square brackets `[...]` instead of curly braces `{...}`
2. The pgvector extension is properly installed in PostgreSQL

### Quiz Generation Issues

If quiz creation fails, check:
1. Sufficient questions exist for the selected language/level
2. The OpenAI API is responding correctly
3. Database connections are working

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Open a pull request

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🔗 Useful Links

- [Django Documentation](https://www.djangoproject.com/)
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [JWT Authentication](https://django-rest-framework-simplejwt.readthedocs.io/)
