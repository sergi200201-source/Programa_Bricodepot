# Programa Brico Dépôt Web Application

## Overview
This project is a web application version of the "Programa Brico Dépôt" built using Flask. It provides a user interface for users to log in and access various functionalities related to the Brico Dépôt program.

## Project Structure
```
programa-brico-depot-web
├── app.py                # Main application file
├── requirements.txt      # Project dependencies
├── templates             # HTML templates
│   ├── index.html       # Main page template
│   ├── login.html       # Login page template
│   └── unauthorized.html # Unauthorized access page
├── static                # Static files
│   └── style.css        # CSS styles
└── README.md            # Project documentation
```

## Setup Instructions
1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd programa-brico-depot-web
   ```

2. **Install dependencies**:
   It is recommended to use a virtual environment. You can create one using:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
   Then install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. **Run the application**:
   Execute the following command to start the Flask application:
   ```
   python app.py
   ```
   The application will be accessible at `http://127.0.0.1:5000`.

## Usage
- Navigate to the login page to enter your name.
- If the name entered is "sergi", you will be granted access to the main application.
- Unauthorized users will be redirected to an unauthorized access page.

## License
This project is licensed under the MIT License. See the LICENSE file for details.