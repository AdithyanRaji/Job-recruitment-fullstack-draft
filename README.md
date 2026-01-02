🧑‍💼 AJYNT Job Recruitment Platform

A **full-stack Job Recruitment Web Application** built using **Flask**, **SQLite**, **HTML/CSS**, and **Bootstrap**, designed to simulate a real-world hiring workflow with **User** and **Admin** roles.

## 🚀 Features

### 👤 User Features

* User registration & login
* Browse available job listings
* Apply for jobs with resume upload (PDF/DOC)
* View application status (Pending / Selected / Rejected)
* Personal user dashboard with:

  * Application summary
  * Recent applications
* My Applications page
* Secure logout

---

### 🛠️ Admin Features

* Admin registration & login
* Admin dashboard with platform statistics
* Add / update job listings
* View all job postings
* View all applicants
* Download/view resumes
* Select or reject candidates
* View selected applicants with timestamps
* Remove selected candidates

---

## 🧱 Tech Stack

| Layer          | Technology             |
| -------------- | ---------------------- |
| Backend        | Flask (Python)         |
| Database       | SQLite + SQLAlchemy    |
| Frontend       | HTML, CSS, Bootstrap   |
| Authentication | Flask Sessions         |
| File Uploads   | Werkzeug               |
| Styling        | Bootstrap + Custom CSS |

---

## 📂 Project Structure

```
Job-Recruitment-Platform/
│
├── app.py
├── site.db
├── static/
│   ├── css/
│   │   └── style.css
│   └── images/
│
├── templates/
│   ├── admin_func/
│   ├── user_func/
│   ├── nav.html
│   ├── footer.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   └── index.html
│
├── uploads/
│   └── resumes/
│
└── README.md
```

---

## 🔐 Roles & Access Control

* **Users**

  * Can only apply and view their own applications
* **Admins**

  * Can manage jobs and applicants
  * Can view resumes
  * Can select or reject candidates

Access control is enforced using **Flask sessions**.

---

## 📄 Resume Handling

* Resumes are uploaded securely
* Stored in a protected folder (`uploads/resumes`)
* Accessible **only to admins**
* Supported formats: `.pdf`, `.doc`, `.docx`

---

## 🖼️ UI Enhancements

* Card-based layouts for jobs and applications
* Hover effects and transitions
* Responsive grid system
* Status badges (Pending / Selected / Rejected)
* Clean dashboards for both users and admins

---

## 🧪 How to Run the Project

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/job-recruitment-platform.git
cd job-recruitment-platform
```

### 2️⃣ Install Dependencies

```bash
pip install flask flask_sqlalchemy werkzeug
```

### 3️⃣ Run the Application

```bash
python app.py
```

### 4️⃣ Open in Browser

```
https://job-recruitment-fullstack-draft.onrender.com
```

---

## 📈 Future Enhancements

* Pagination & search for job listings
* Email notifications on selection
* Resume parsing
* Admin analytics dashboard
* Role-based permissions
* Deployment on Render / Railway / AWS

---

## 🎯 Learning Outcomes

* Flask routing & templating (Jinja2)
* Role-based authentication
* SQLAlchemy ORM
* File uploads & security
* Frontend UI structuring with Bootstrap
* Full-stack project structuring

---

## 👨‍💻 Author
**Adithyan R**

Project built for learning full-stack web development.

---

## ⭐ Final Note

This project demonstrates a **real-world recruitment workflow**, combining backend logic, database design, and frontend UI — suitable for **portfolio, interviews, and academic submissions**.


