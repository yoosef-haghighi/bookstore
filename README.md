# 📚 Bookstore

An online bookstore web application built with Django.

## 🚀 Features
- User authentication (register/login/logout)
- Book management (add/edit/display)
- Responsive UI with HTML/CSS templates
- Modular structure (accounts, books, pages apps)

## 🛠️ Tech Stack
- Python 3.x
- Django
- HTML, CSS, JavaScript

## ⚡ Quick Start
```bash
git clone https://github.com/yoosef-haghighi/bookstore.git
cd bookstore
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Acces at : http://127.0.0.1:8000/

## 📁 Project Structure
bookstore/
├── config/          # Project settings
├── accounts/        # User management
├── books/           # Book CRUD operations
├── pages/           # Static pages (about, etc.)
├── templates/       # HTML templates
└── static/          # CSS, JS, images

توجه: این پروژه در حال توسعه است و هر روز تغییراتی در آن ایجاد می‌شود. 
