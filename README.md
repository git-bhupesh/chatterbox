---

# 🗨️ Chatterbox

### Real-Time Social Networking Platform (Django)

![Django](https://img.shields.io/badge/Django-4.x-darkgreen)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active%20Development-orange)

---

## 📌 Overview

**Chatterbox** is a **full-stack social networking application** built with **Django**, designed to demonstrate real-world backend, real-time, and system design skills.

The platform supports **real-time messaging**, **live notifications**, and a **dynamic social feed**, showcasing scalable architecture using **WebSockets, Redis, Celery, and Django Signals**.

> 🎯 Built to mirror features found in modern social platforms like WhatsApp, Instagram, and Twitter — with a focus on clean backend design.

---

## ✨ Key Highlights

* ⚡ Real-time chat using **Django Channels & WebSockets**
* 🔔 Live notifications without page reloads
* 🧵 Social feed with image uploads
* 👥 Follow / Unfollow & user discovery
* ⌨️ Typing indicators via Redis
* ☁️ Cloudinary-based media storage
* 🧩 Modular, scalable Django app structure

---

## 📸 Screenshots


Login
<img width="1919" height="913" alt="Screenshot 2026-02-05 175444" src="https://github.com/user-attachments/assets/619afefd-13b3-4c84-92b3-b21686915efe" />
Chat
<img width="1919" height="915" alt="image" src="https://github.com/user-attachments/assets/95519cb8-e081-4d65-b4d5-6e2169f08e18" />
Feed
<img width="1919" height="913" alt="image" src="https://github.com/user-attachments/assets/7ce8dd96-b74b-4831-9690-08decd08becf" />
Notifications
<img width="1919" height="915" alt="image" src="https://github.com/user-attachments/assets/043be9f0-7db7-4ec8-b70c-5560479f3191" />
Profile
<img width="1919" height="917" alt="image" src="https://github.com/user-attachments/assets/4d9abc9c-3609-42a2-b4f0-474a6232174e" />
Signup
<img width="1903" height="913" alt="image" src="https://github.com/user-attachments/assets/19c09bc5-f1ad-45a6-a905-cf2ebe8563e2" />
MobileView
<img width="393" height="828" alt="image" src="https://github.com/user-attachments/assets/2b05ea6d-6644-4a35-b432-a82816f5ed69" />


---

## 🧠 What This Project Demonstrates

✅ Real-time systems with WebSockets
✅ Event-driven architecture using Signals
✅ Async task handling with Celery
✅ Redis caching & pub/sub concepts
✅ Secure media handling
✅ Clean Django app separation
✅ Production-aware setup

---

## 🛠️ Tech Stack

| Category          | Technologies                         |
| ----------------- | ------------------------------------ |
| **Backend**       | Python, Django                       |
| **Real-Time**     | Django Channels, Daphne, WebSockets  |
| **Frontend**      | Django Templates, HTMX, Tailwind CSS |
| **Database**      | SQLite (Dev), PostgreSQL (Prod)      |
| **Async / Cache** | Celery, Redis                        |
| **Media Storage** | Cloudinary                           |

---

## 🚀 Core Features

### 💬 Real-Time Messaging

* Private and group chat
* WebSocket-based bi-directional communication
* Typing indicators using Redis

### 🔔 Live Notifications

* Likes, comments, and follows
* Signal-driven backend logic
* HTMX-powered UI updates

### 🧱 Social Feed

* Post creation with images
* Like & comment system
* Optimized media delivery via Cloudinary

### 🧑‍🤝‍🧑 Social Graph

* Follow / Unfollow users
* User search
* Feed personalization logic

### 🏗️ System Architecture

graph TD
    User((User/Browser)) -->|HTTP Requests| Django[Django Server]
    User -->|WebSockets| Daphne[Daphne/Channels ASGI]
    
    subgraph "Real-Time Layer"
        Daphne <--> Redis_Channel[Redis Channel Layer]
        Redis_Channel <--> Daphne
    end
    
    subgraph "Async Task Layer"
        Django -->|Trigger Task| Redis_Broker[Redis Broker]
        Redis_Broker --> Celery[Celery Worker]
        Celery -->|Update Status| DB[(PostgreSQL/SQLite)]
    end
    
    subgraph "Storage & Data"
        Django --> DB
        Django --> Cloudinary[Cloudinary Media Storage]
    end
    
    style User fill:#f9f,stroke:#333,stroke-width:2px
    style Redis_Channel fill:#ff9999,stroke:#333
    style Redis_Broker fill:#ff9999,stroke:#333
    style Daphne fill:#99ff99,stroke:#333
    style Celery fill:#99ccff,stroke:#333
---

## 📦 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/git-bhupesh/chatterbox.git
cd chatterbox
```

### 2️⃣ Virtual Environment

```bash
python -m venv venv
```

**Windows**

```powershell
.\venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key
DEBUG=True

CLOUDINARY_CLOUD_NAME=xxxx
CLOUDINARY_API_KEY=xxxx
CLOUDINARY_API_SECRET=xxxx

REDIS_URL=redis://127.0.0.1:6379
```

---

## ▶️ Running the Project

### Start Redis

```bash
redis-server
```

### Apply Migrations

```bash
python manage.py migrate
```

### Run Development Server

```bash
python manage.py runserver
```

### (Optional) Run Celery Worker

```bash
celery -A chatterbox worker -l info
```

---

## 🛣️ Roadmap

* [ ] Online / Offline user presence
* [ ] Message read receipts
* [ ] Emoji reactions
* [ ] Push notifications
* [ ] Production deployment (Render / Railway)

---
## 🔮 Future Improvements

* Online / Offline user presence
* Message read receipts & delivery status
* Emoji reactions & message replies
* Push notifications (Web / Mobile)
* Role-based permissions (Admin / Moderator)
* Rate limiting & spam protection
* Dockerized deployment
* Full CI/CD pipeline
* Production deployment with monitoring

---

## 👨‍💻 Author

**Bhupesh Dewangan**

* GitHub: [https://github.com/bhupeshkd](https://github.com/bhupeshkd)
* Passionate about backend development, real-time systems, and scalable web applications.

---

## 🤝 Contributing

Contributions are welcome.
Feel free to open issues or submit pull requests.

---

## 📄 License

Licensed under the **MIT License**.

---

## ⭐ This project reflects my hands-on experience with:

* Real-time backend systems
* Django production patterns
* Async processing & caching
* Clean, scalable architecture

⭐ **Star the repo if you find it useful!**

---

