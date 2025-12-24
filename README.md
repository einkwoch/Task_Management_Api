# 🗂️ Task Management Application (Django)

A full-featured **Task Management web application** built with **Django**, designed to help users create, manage, filter, and track tasks efficiently.  
The application includes **authentication, task ownership, filtering, sorting, and automated notifications for upcoming deadlines**.

---

## 🚀 Features

### 🔐 User Authentication
- User registration and login
- Secure session-based authentication
- Tasks are **user-specific** (each user only sees their own tasks)

---

### ✅ Task Management
Users can:
- Create new tasks
- View task details
- Update existing tasks
- Delete tasks

Each task includes:
- Title
- Description
- Status (Pending / Completed)
- Priority (High / Medium / Low)
- Due date
- Created-by user

---

### 🔍 Filtering & Sorting
Tasks can be filtered by:
- Status (Pending / Completed)
- Priority (High / Medium / Low)
- Due date

Tasks can be sorted by:
- Due date
- Priority

---

### 🔔 Notifications System

#### In-App Notifications
- Users receive **in-app warnings** when they have tasks due within the next 24 hours.
- Notifications appear automatically on the task list page.

#### Email Notifications
- Automated email reminders are sent for tasks due within 24 hours.
- Implemented using a **custom Django management command**.
- Can be scheduled using cron or a task scheduler.

---

## 🛠️ Tech Stack

- **Backend:** Django
- **Frontend:** Django Templates (HTML/CSS)
- **Database:** SQLite (default)
- **Authentication:** Django Auth System
- **Email:** Gmail SMTP (Production) / Console Backend (Development)
- **Hosting:** PythonAnywhere (optional)

---

## 📂 Project Structure

```
Task_Management_Api/
├── tasks/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   │   └── tasks/
│   └── management/
│       └── commands/
│           └── send_due_task_notifications.py
├── static/
├── manage.py
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/Task_Management_Api.git
cd Task_Management_Api
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate     # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Apply Migrations
```bash
python manage.py migrate
```

### 5️⃣ Create a Superuser
```bash
python manage.py createsuperuser
```

### 6️⃣ Run the Server
```bash
python manage.py runserver
```

---

## 📧 Email Setup (Gmail SMTP)

### 🔐 Enable Gmail App Password
- Enable 2-Step Verification
- Generate App Password for Mail
- Use the generated password in Django settings

### ⚙️ Django Email Configuration

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'yourgmail@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

---

## ⏰ Automated Email Reminders

```bash
python manage.py send_due_task_notifications
```

---

## ☁️ Deployment on PythonAnywhere

### Environment Variables
Set on PythonAnywhere dashboard:

```
EMAIL_HOST_USER=yourgmail@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

Update settings.py:

```python
import os
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
```

### Schedule Task
```bash
python /home/yourusername/Task_Management_Api/manage.py send_due_task_notifications
```

---

## 🔒 Security
- Authentication required for all task actions
- Users can only access their own tasks
- Secure password hashing via Django
- Environment variables for sensitive data

---

## 👨‍💻 Author

**Emmanuel Izuchukwu Nkwocha**  
Senior Controls Engineer | Software Engineer  

---

## 📄 License

MIT License
