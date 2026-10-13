# 📚 Django Bookstore

A web-based bookstore application built with **Python and Django**, featuring book browsing, user accounts, a shopping cart, and order management.

## ✨ Features

- **User Authentication:** User registration, login, and logout.
- **Book Catalog:** Browse books and view individual book details.
- **Book Management:** Create, update, and delete book listings.
- **Wishlist:** Save favorite books for later.
- **Shopping Cart:** Add books to the cart and manage cart items.
- **Order Management:** Checkout, view orders, and track order status.
- **Responsive Interface:** HTML and CSS templates designed for a user-friendly experience.

> Note: Available features and workflows should be verified against the current implementation.

## 🛠️ Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **Forms:** Django Forms, django-crispy-forms
- **Image Processing:** Pillow
- **Database:** Django-supported database configuration

## 📸 Screenshots

Explore the application's interface below.

### Homepage

![Bookstore Homepage](https://github.com/user-attachments/assets/4379d75c-173c-41da-84ca-f1e66f10d6c2)

### Book Catalog and Details

![Bookstore Screenshot](https://github.com/user-attachments/assets/b0ee6869-8ed1-42a9-8c4e-c8e40aaa4cac)

### Additional Application Views

![Bookstore Screenshot](https://github.com/user-attachments/assets/521acf6d-c7e9-42cd-85c1-d196af2f7129)

## 🚀 Getting Started

Follow these steps to run the project locally.

### Prerequisites

- Python 3.x compatible with the project's Django version
- Git
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/yoosef-haghigi/bookstore.git
cd bookstore
```

### 2. Create a Virtual Environment

**Windows (Command Prompt):**

```bat
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

### 5. Start the Development Server

```bash
python manage.py runserver
```

Open your browser and visit:

**http://127.0.0.1:8000/**

## 📁 Project Structure

```text
bookstore/
├── accounts/       # User authentication and account management
├── books/          # Book catalog and book-related functionality
├── orders/         # Shopping cart and order management
├── pages/          # General website pages
├── config/         # Django settings and URL configuration
├── templates/      # Shared HTML templates
├── static/         # CSS, fonts, icons, and other static assets
├── media/          # Uploaded or stored media files
├── requirements.txt
├── manage.py
└── README.md
```

## 🔧 Development Notes

This project is actively under development. Features, design, and functionality may change as development progresses.

For local development, use Django's development server. Before deploying to production, review security settings, environment variables, static and media file handling, database configuration, and the order/payment workflow.

## 👨‍💻 Author

**Yoosef Haghighi**

- GitHub: [yoosef-haghighi](https://github.com/yoosef-haghighi)
- Project Repository: [Django Bookstore](https://github.com/yoosef-haghighi/bookstore)

---

*Built with Python and Django.*
