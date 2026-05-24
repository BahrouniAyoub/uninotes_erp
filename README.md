# UniNotes ERP — Django Academic Management System

UniNotes ERP is a Django-based academic management platform designed to simulate a simplified university ERP (Enterprise Resource Planning) system.

The project allows:
- Students to select academic modules,
- Tutors to supervise assigned students,
- Tutors to enter and update grades,
- Students to consult dashboards and academic evolution,
- Administrators to manage the entire system through Django Admin.

This project was developed as a complete educational Django project and demonstrates:
- Authentication & authorization,
- Database modeling,
- Business rules,
- Dashboard systems,
- Grade management,
- ORM calculations,
- Role-based permissions,
- Chart.js integration,
- Responsive frontend design.

---

# Features

## Authentication System
- User registration
- Login/logout
- Session management
- Role-based accounts:
  - Student
  - Tutor

## Academic Management
- Module catalog
- Evaluation categories
- Student enrollment basket
- 60-point academic rule
- Enrollment locking system

## Tutor System
- Tutor/student assignment
- Tutor dashboard
- Read-only student monitoring
- Tutor-only note management

## Dashboard System
- Student dashboard
- Tutor student dashboard
- Weighted averages
- Evolution chart
- Academic statistics

## Frontend
- Responsive UI
- Custom CSS design system
- Dashboard cards
- Statistics widgets
- Tables and forms
- Mobile-friendly layout

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend language |
| Django | Web framework |
| SQLite | Development database |
| HTML5 | Frontend structure |
| CSS3 | Styling |
| Chart.js | Data visualization |
| Django ORM | Database abstraction |
| Django Templates | Server-side rendering |

---

# Project Structure

```text
uninotes_erp_bahrouni_ayoub/
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── signals.py
│   ├── urls.py
│   └── admin.py
│
├── academics/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── services.py
│   ├── urls.py
│   └── admin.py
│
├── dashboard/
│   ├── views.py
│   ├── urls.py
│   └── templates/
│
├── templates/
│   ├── base.html
│   ├── accounts/
│   ├── academics/
│   └── dashboard/
│
├── static/
│   └── css/style.css
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── db.sqlite3
├── manage.py
└── README.md