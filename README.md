# URL Shortener

## Overview

The **URL Shortener** is a modern, responsive web application that allows users to shorten long URLs for easier sharing and tracking. Built using **Flask** and **SQLAlchemy**, this app features the ability to shorten URLs, track the number of clicks on each shortened link, and provide a sleek, user-friendly design.

The application is designed to be easily extendable and offers a clean user interface, allowing users to quickly generate short URLs and view their usage statistics. With a well-structured database and modern design principles, this URL shortener is both powerful and easy to use.

![d0761df0-9d81-40c2-b009-2d2b7b7a9885](https://github.com/user-attachments/assets/c0e1d7bb-51b8-445b-878f-0375b30fa170)

## Key Features

- **Shorten URLs**: Easily convert long URLs into short, shareable links.
- **Click Tracking**: Keep track of the number of times each shortened URL has been clicked, providing insight into its usage.
- **Responsive Design**: The app is built with a mobile-first approach, ensuring it is fully responsive across all devices.
- **Clipboard Copy**: A simple "Copy to Clipboard" button to quickly copy shortened URLs for easy sharing.
- **Recent URLs**: View a history of recently shortened URLs for quick access.
- **SEO Friendly**: The generated short URLs can be indexed by search engines for better visibility.

## Technology Stack

- **Flask**: A lightweight web framework for Python that allows easy routing and request handling.
- **SQLAlchemy**: A powerful Object-Relational Mapping (ORM) library for Python to manage the app's database.
- **SQLite**: The default database for local development, which can be replaced with other databases like PostgreSQL for production.
- **HTML/CSS/JavaScript**: Used for the frontend interface, providing a modern, user-friendly experience.

## Project Structure

```
url-shortener/
│
├── static/                   # Contains static files like CSS, JS, images, etc.
│   ├── css/
│   │   └── style.css         # Main CSS file for styling the app
│   ├── js/
│   │   └── main.js           # JavaScript file for handling frontend functionality
│
├── templates/                # Contains HTML files that form the structure of the web pages
│   ├── base.html             # Base template with common layout (header, footer)
│   ├── index.html            # Main page where users can shorten URLs
│   └── stats.html            # Page to display statistics for shortened URLs
│
├── .gitignore                # Specifies files and directories that should be ignored by Git
├── README.md                 # Project documentation (you're reading this file)
├── app.py                    # The main Flask application file
├── config.py                 # Configuration settings for the Flask app (e.g., database URI)
├── requirements.txt          # List of Python dependencies required for the project
```

### Folder and File Descriptions

1. **`static/`**  
   This folder holds static resources, such as stylesheets (CSS), JavaScript files, and any images used in the frontend of the application.
   - **`css/style.css`**: Contains all the styles for the web pages.
   - **`js/main.js`**: Handles all JavaScript functionality, including the logic for copying URLs to the clipboard, AJAX requests, and any other interactivity.

2. **`templates/`**  
   Contains HTML files that are rendered by Flask to generate the content of the web pages.
   - **`base.html`**: A base HTML template that includes shared elements (header, footer) and is extended by other templates.
   - **`index.html`**: The homepage where users can input a long URL and generate a shortened version.
   - **`stats.html`**: Displays statistics (such as the number of clicks) for each shortened URL.

3. **`app.py`**  
   The core of the Flask application that contains route handlers and the logic for shortening URLs, rendering pages, and interacting with the database.

4. **`config.py`**  
   A configuration file that contains settings for the application, such as the database URI, secret keys, etc. This file helps manage the app's environment (development, production, etc.).

5. **`requirements.txt`**  
   Lists all the required Python dependencies for the project. Use this file to install the necessary libraries with `pip`.

6. **`.gitignore`**  
   Specifies files and directories that should not be tracked by Git, such as local development files and the virtual environment directory.

---

## Installation

### Prerequisites

- Python 3.x
- Flask
- SQLAlchemy
- SQLite (or another database for production)

### Steps to Install

Follow these steps to set up the project on your local machine:

1. **Clone the Repository**

   Clone the repository to your local machine:
   ```bash
   git clone https://github.com/harryongit/url-shortener.git
   cd url-shortener
   ```

2. **Create a Virtual Environment**

   Create and activate a virtual environment to manage the dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   Install the required dependencies listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database**

   Initialize the database and create the necessary tables:
   ```bash
   python
   >>> from app import app, db
   >>> with app.app_context():
   >>>     db.create_all()
   >>> exit()
   ```

5. **Run the Application**

   Start the Flask development server:
   ```bash
   python app.py
   ```

   Your application will be running at `http://localhost:5000`.

---

## Usage

Once the app is running, you can access it in your web browser at `http://localhost:5000`. Here’s how the app works:

1. **Shorten a URL**: On the homepage (`index.html`), paste a long URL into the input field and click the "Shorten URL" button. The app will generate a shortened version of the URL and display it on the page.
2. **Copy to Clipboard**: You can easily copy the shortened URL to your clipboard with the "Copy to Clipboard" button.
3. **View Statistics**: Go to the "Statistics" page to view how many times each URL has been clicked and other relevant data.

---

## Technology Details

### Flask
- **Flask** is a lightweight WSGI web framework that is easy to use and very flexible. It helps you build web applications quickly and with minimal overhead.

### SQLAlchemy
- **SQLAlchemy** is an ORM (Object Relational Mapper) for Python. It allows you to interact with databases in a Pythonic way by mapping tables to Python classes.

### SQLite
- By default, the app uses **SQLite** for local development, which stores data in a local file. For production environments, you can switch to a more robust database like **PostgreSQL** or **MySQL**.

---

## Contributing

We welcome contributions to the project! If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Write tests and ensure all existing tests pass.
4. Submit a pull request with a detailed description of your changes.

Please ensure your code follows the project’s existing style and passes all linting checks before submitting a pull request.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

## Acknowledgements

- **Flask** for the web framework.
- **SQLAlchemy** for database handling.
- **Bootstrap** (used in the frontend) for responsive design and UI components.
