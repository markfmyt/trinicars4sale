# TriniCars4Sale

TriniCars4Sale is a modern e-commerce platform specifically designed for buying and selling vehicles in Trinidad and Tobago. The application provides a user-friendly interface for car dealers and private sellers to list their vehicles, while offering potential buyers an easy way to browse and purchase cars.

![image](https://github.com/user-attachments/assets/3494bbc2-4208-4428-91a7-1fd074ec75d4)

## Features

### For Buyers
- Browse car listings with detailed information
- Search and filter cars by various criteria (make, model, year, price range)
- Direct messaging system to communicate with sellers
- View seller profiles and their listings
- View detailed car information including images and specifications

### For Sellers
- Create and manage car listings
- Upload multiple images per listing
- Set pricing and vehicle details
- Receive and respond to buyer inquiries
- Track listing views and messages
- Manage multiple listings from a dashboard

### General Features
- User authentication and authorization
- Responsive design for mobile and desktop
- Real-time messaging system
- Image upload and management
- Category-based organization
- Search functionality
- User profiles with activity history

## Technology Stack

- **Backend**: Python/Flask
- **Database**: SQLite (SQLAlchemy ORM)
- **Frontend**: Jinja, HTML5, CSS3, JavaScript
- **UI Framework**: Bootstrap 5
- **Authentication**: Flask-Login
- **File Upload**: Flask-Upload
- **Forms**: Flask-WTF
- **API**: Flask-JWT-Extended

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/markfmyt/TriniCars4Sale.git
cd TriniCars4Sale
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
FLASK_APP=wsgi.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
UPLOAD_FOLDER=uploads
```

5. Initialize the database and sample data:
```bash
# First, reset the database to ensure a clean state
flask init-db

# Initialize the required categories for car listings
flask init-categories

# Initialize sample data including:
# - Demo user account (mark@mail.com)
# - Sample car listings (Lamborghini, Tesla, Mitsubishi, Mercedes)
flask init-sample-data
```

6. Run the application:
```bash
flask run
```

The application will be available at `http://localhost:8080`

The application comes with pre-loaded sample data for demonstration purposes:

### Demo User Account
- **Email**: mark@mail.com
- **Password**: 1
- **Phone**: +1-868-123-4567

## Database Structure

The application uses the following main models:

- **User**: Stores user information and authentication details
- **Product**: Contains car listing information
- **Message**: Manages communication between users
- **Order**: Tracks purchase transactions
- **Category**: Organizes car listings by type

## Additional Images
![listings](https://github.com/user-attachments/assets/949d3fb0-fe4b-4a55-8534-64125e5df417)
![lambo listing](https://github.com/user-attachments/assets/e4568240-b601-4b1e-b97d-42213750aafe)


