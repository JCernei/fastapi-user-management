# fastapi-user-management

## Running the Project with Docker Compose

This project uses Docker Compose to simplify setup and deployment. Docker Compose will handle creating and linking the
application and database containers.

### Steps to Run the Project

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/JCernei/fastapi-user-management.git
   cd fastapi-user-management
   ```
2. **Add Environment Variables**

   To set up and run this project, the following environment variables are required. You can copy them into a `.env`
   file in the project root. These values are mock examples—replace them with actual values for production.

    ```plaintext
    # Application-specific settings
    PYTHONPATH=/usr/src/app/
    
    # Database configuration
    MYSQL_USER=example_user
    MYSQL_PASSWORD=example_password
    MYSQL_ROOT_PASSWORD=example_root_password
    MYSQL_HOST=db  # Use 'localhost' if not using Docker
    MYSQL_PORT=3306
    MYSQL_DATABASE=example_db
    
    # JWT settings
    SECRET_KEY=mock_secret_key_1234567890abcdef1234567890abcdef1234567890abcdef
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```
3. **Run the Project with Docker Compose**
   
   Make sure to have **Docker** and **Docker Compose** installed on your system. You can download them from [Docker's official website](https://www.docker.com/).
    ```
    docker compose up --build
    ```
   