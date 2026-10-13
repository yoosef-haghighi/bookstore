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

<img width="1370" height="726" alt="Screenshot (14)" src="https://github.com/user-attachments/assets/28cc2628-ccac-4387-a836-85dc1df16e85" />

### Book Catalog and Details

<img width="1359" height="687" alt="Screenshot (16)" src="https://github.com/user-attachments/assets/710fabe7-a723-4aa8-823e-48e5d7231bca" />


### Additional Application Views

<img width="1362" height="623" alt="Screenshot (19)" src="https://github.com/user-attachments/assets/0374e06e-fa2e-4f20-a066-c2d9ad661278" />

<img width="1366" height="685" alt="Screenshot (18)" src="https://github.com/user-attachments/assets/0d8560d0-ba46-4ff0-807d-6afb85c029c3" />


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
