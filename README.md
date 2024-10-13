# Employee Management System

A Flask-based web application for managing employee data.

## Features

- Employee listing: View all employees.
- Employee creation: Add new employees.
- Employee editing: Update existing employee details.
- Employee deletion: Remove employees from the system.
- Find by ID: Search for an employee by their ID.
- Database connection: PostgreSQL database interaction via `psycopg2`

## Requirements

To run this application, you need the following:

- **Flask**
- **psycopg2**
- **PostgreSQL**

## Database Schema

The application uses a PostgreSQL database with the following schema:

### Table: `emp_table`

| Column Name | Type             | Constraints               |
|-------------|------------------|---------------------------|
| id          | serial           | Primary Key               |
| name        | varchar          | Not Null                  |
| email       | varchar          | Not Null                  |
| designation | varchar          | Not Null                  |
| salary      | integer          | Not Null                  |

## Routes and Endpoints

- `GET /`: Renders the home page (index.html).
- `GET/POST /employees`: Lists all employees or adds a new employee.
- `GET /find_employees`: Finds an employee by their ID.
- `POST /update/<id>`: Updates employee details.
- `GET/DELETE /delete/<id>`: Deletes an employee.

## Templates

The following templates are included in the application:

- **index.html**: The template for the root route.
- **employees.html**: The template for listing all employees.
- **create.html**: The template for creating a new employee.
- **edit.html**: The template for editing an existing employee.
- **failure.html**: The template for displaying failure messages.
- **layout.html**: The base template for the application.
- **success.html**: The template for displaying success messages.

## Usage

To run the application, follow these steps:

1. **Install the required dependencies**:

   ```bash
   pip install Flask psycopg2
   ```

2. **Set up the database connection**:

   - Create a PostgreSQL database named `emp_management`.
   - Update the `app.py` file with the appropriate database connection details.

3. **Run the application**:

   Start the Flask development server:

   ```bash
   flask --debug run
   ```
## License

This project is licensed under the MIT License.
