# Shop Application

## Overview

This is a **modular, containerized e-commerce platform** built with Flask. It features secure user authentication, role-based access control, and advanced analytics integration via a Hadoop cluster. The app is divided into two main parts:

- **Authentication:** Handles registration, login, and account management for multiple user roles.
- **Shop:** Supports Owners, Customers, and Couriers, each with distinct functionalities.

All services, including MySQL databases, and Hadoop analytics cluster, are containerized and orchestrated using Docker Compose for easy deployment and consistent development environments.

---

## Features

- **User Roles:** Customer, Courier, and Owner, each with tailored permissions.
- **Authentication:** JWT-based secure login and access control using Flask-JWT-Extended.
- **Database:** MySQL managed via Flask-SQLAlchemy ORM and Flask-Migrate for schema migrations.
- **Adminer:** Web interface for managing MySQL databases.
- **Analytics:** Hadoop cluster (master + workers) for advanced product and category statistics.
- **Frontend:** Server-rendered HTML templates using Jinja2, with robust error handling.
- **Deployment:** Docker Compose orchestration for all containers including Flask apps, MySQL, Adminer, and Hadoop.

---

## Technologies Used

- **Backend:** Flask, Flask-JWT-Extended, Flask-SQLAlchemy, Flask-Migrate  
- **Database:** MySQL, Adminer  
- **Big Data Analytics:** Hadoop (Docker images `bde2020/hadoop`)  
- **Containerization:** Docker, Docker Compose  
- **Frontend:** Jinja2 templating engine  

---

## API Routes Overview

### Authentication

| Methods  | Route                 | Description                                 |
|----------|-----------------------|---------------------------------------------|
| GET/POST | `/register_customer`  | Show registration form / Register customer  |
| GET/POST | `/register_courier`   | Show registration form / Register courier   |
| GET/POST | `/login`              | Show login form / Authenticate user         |
| GET/POST | `/delete`             | Show delete confirmation / Delete account   |

### Owner

| Methods  | Route                   | Description                                  |
|----------|-------------------------|----------------------------------------------|
| GET/POST | `/update`               | Upload/update files (e.g., product data)     |
| GET      | `/product_statistics`   | View product sales and performance stats     |
| GET      | `/category_statistics`  | View category-based sales statistics          |

### Courier

| Methods  | Route                | Description                                   |
|----------|----------------------|-----------------------------------------------|
| GET/POST | `/pick_up_order`     | Show pick-up form / Confirm order pick-up     |
| GET      | `/orders_to_deliver` | List orders assigned for delivery              |

### Customer

| Methods  | Route       | Description                                    |
|----------|-------------|------------------------------------------------|
| GET       | `/search`   | Search products                               |
| GET/POST  | `/order`    | Show order form / Place a new order            |
| GET/POST  | `/delivered`| Show deliveries to confirm / Confirm delivery |
| GET       | `/status`   | Check status of orders                         |

---

## Setup and Deployment

```bash
To run:
  .\run_all_services.ps1
To stop:
   .\down_services.ps1
