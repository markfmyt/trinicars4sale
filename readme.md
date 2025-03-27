# TriniCars4Sale

TriniCars4Sale is a modern e-commerce platform specifically designed for buying and selling vehicles in Trinidad and Tobago. The application provides a user-friendly interface for car dealers and private sellers to list their vehicles, while offering potential buyers an easy way to browse and purchase cars.

## Features

### For Buyers
- Browse car listings with detailed information
- Search and filter cars by various criteria (make, model, year, price range)
- Direct messaging system to communicate with sellers
- View seller profiles and their listings
- Save favorite listings
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
- **Frontend**: HTML5, CSS3, JavaScript
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

5. Initialize the database:
```bash
flask init-db
flask init-categories
```

6. Run the application:
```bash
flask run
```

The application will be available at `http://localhost:8080`

## Database Structure

The application uses the following main models:

- **User**: Stores user information and authentication details
- **Product**: Contains car listing information
- **Message**: Manages communication between users
- **Order**: Tracks purchase transactions
- **Category**: Organizes car listings by type

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Bootstrap for the UI framework
- Font Awesome for icons
- Flask community for the excellent framework and extensions

## Support

For support, please open an issue in the GitHub repository or contact the development team.
