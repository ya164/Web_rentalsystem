# RentalSystem

**RentalSystem** is a full-stack web application for managing vehicle rentals (cars, e-scooters, bicycles).
It allows users to rent vehicles and track expenses, while administrators manage the fleet and monitor system activity.

**Project Type:** Full-Stack Web Application (Pet Project)

**Architecture:** Client–Server (REST API)

---

## 🛠 Technology Stack

| Component    | Technologies                                     |
| ------------ | ------------------------------------------------ |
| **Backend**  | Python, Flask, Flask-RESTful, Flask-JWT-Extended |
| **Frontend** | Vue.js 3, Vue Router, Vuex                       |
| **Database** | PostgreSQL / MySQL (SQLAlchemy ORM)              |
| **Security** | JWT Authentication, Werkzeug Security            |
| **Styling**  | Custom CSS (CSS variables, Grid/Flexbox)         |

---

## 🚀 Key Features

### 👤 User Features

* **Authentication**: Secure registration and login using JWT
* **Asset Catalog**: Browse available vehicles with filtering
* **Rental Management**: Create rentals with automatic cost calculation *(Price × Days)*
* **Dashboard**: View active rentals, rental history, and financial summaries

### 🛡️ Admin Features

* **Fleet Management**: Full CRUD for all vehicles
* **Status Control**: Toggle availability (Available ↔ Under Maintenance)
* **Global Monitoring**: View all rentals in the system
* **Intervention Tools**: Force-cancel any active rental

---

## 🗄 Database Model (Overview)

* **User**: Credentials (hashed), admin flag
* **Asset**: Vehicle type, pricing, status
* **Rental**: Connects User ↔ Asset with dates and total cost
* **StatusHistory**: Logs all status changes for assets and rentals

The system uses a relational database with strict data integrity via SQLAlchemy ORM.

---

## 🔧 Installation & Setup

### 1. Backend Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/rentalsystem.git
cd rentalsystem/backend

# Create virtual environment
python -m venv venv
# Activate (Windows):
venv\Scripts\activate
# Activate (Linux/Mac):
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend
flask run
```

---

### 2. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Run development server
npm run serve
```

**Backend:** [http://localhost:5000](http://localhost:5000)
**Frontend:** [http://localhost:8080](http://localhost:8080)

---

## 🔐 Security Measures

* **Password Hashing** using `werkzeug.security`
* **JWT-based Authentication** (stateless sessions)
* **Role-Based Access Control (RBAC)** — `@admin_required` decorators
* **CORS** configured for secure frontend ↔ backend communication

---

## 📌 Notes

This project was developed as a personal full-stack training project to practice

* backend architecture with Flask
* REST API design
* authentication flows
* relational database modeling
* SPA development with Vue.js
* separation of backend and frontend services
