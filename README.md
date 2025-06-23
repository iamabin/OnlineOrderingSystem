A QR-based smart restaurant ordering system built with Django. This app enables restaurant owners to manage digital menus and generate table-specific QR codes. Customers can scan and place orders directly from their phones—no app installation needed.

#### **Main Pages**

> **Homepage (Login / Signup)**

**Login page:**
  ![GitHub Logo](https://raw.githubusercontent.com/iamabin/OnlineOrderingSystem/main/assets/login.png)
**Signup page:**
  ![GitHub Logo](https://raw.githubusercontent.com/iamabin/OnlineOrderingSystem/main/assets/Signup.png)

> **Dashboard (Menu & Table Management)**
**Menu edition page:**
  ![GitHub Logo](https://raw.githubusercontent.com/iamabin/OnlineOrderingSystem/main/assets/EditMenu.png)

**Table management page:**
  ![GitHub Logo](https://raw.githubusercontent.com/iamabin/OnlineOrderingSystem/main/assets/manageTable.png)
**View order page:**

  ![GitHub Logo](https://raw.githubusercontent.com/iamabin/OnlineOrderingSystem/main/assets/viewOrder.png)

> **Admin Panel**

**Admin page:**
  ![GitHub Logo](https://raw.githubusercontent.com/iamabin/OnlineOrderingSystem/main/assets/admin.png)

#### Tech Stack

- Backend: Django 5.1
- Database: SQLite (default) or MySQL
- Frontend: HTML + Bootstrap 5
- Authentication: Django built-in auth system
- QR Code: `qrcode` + `base64` for image embedding

#### Getting Started

1. Clone the Repository

```bash
git clone https://github.com/iamabin/OnlineOrderingSystem.git
cd tabletapbuilder
```

2.  Create and Activate Virtual Environment

```bash
python3 -m venv env
source env/bin/activate
```

3.  Install Dependencies

```bash
pip install -r requirements.txt
```

4. Run the Development Server

```bash
python manage.py migrate
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

------

## Main Features

| Feature           | Description                                               |
| ----------------- | --------------------------------------------------------- |
| User Registration | Restaurant owners can sign up and manage their dashboard  |
| Menu Management   | Create, edit, and delete menus, categories, and items     |
| Table Management  | Generate table-specific QR codes for each physical table  |
| Customer Ordering | Customers scan QR to view menu and place orders           |
| Order Tracking    | Restaurant dashboard shows live orders with total amounts |

------

