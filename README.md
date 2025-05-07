🛒 Shop project using Flask

🔐 Authentication
This part of the system is built using two Docker images:
  - MySQL Database image
  - Adminer for database ispection
  - A Flask application image

💻 Frontend
  - Provided simple forms using render_template in Flask for basic interaction

Database tables are created and managed using Flask-SQLAlchemy, with schema changes tracked using Flask-Migrate.
  
   -  Migrations run automatically every time a new image is built
   -  Alternatively, migrations can be executed manually while the containers are running

JWT access tokens are used for access control and are stored as cookies for secure session management

📡 API
/login - for logging into a system
/register_customer - for registering a new customer
/register_courier - for registering a new courier
/delete - for deleting account(Currently logged user so access token is required)

⚠️ Error Handling
  - Errors are handled in JSON format with provided messages and error status code.

🐳 Docker

This project can be simply runned using command:

docker compose up --build










