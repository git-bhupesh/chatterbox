# 🗨️ Chatterbox

**Chatterbox** is a full-stack social networking platform built with **Django**. It features real-time messaging, live notifications, and a dynamic social feed, providing a seamless user experience for connecting with others.

---

## 🚀 Key Features

* **Real-Time Chat**: Private and group messaging powered by **Django Channels** and **WebSockets**.
* **Live Notifications**: Instant alerts for likes, comments, and follows using **HTMX** and **Signals**.
* **Dynamic Feed**: A social wall where users can post images (via **Cloudinary**) and interact with content.
* **Social Graph**: Follow/Unfollow system and user search functionality.
* **Typing Indicators**: Real-time "User is typing..." status managed via **Redis** caching.
* **Media Management**: Secure image hosting and delivery through **Cloudinary**.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend** | Python / Django |
| **Real-time** | Django Channels & Daphne |
| **Database** | SQLite (Dev) / PostgreSQL (Prod) |
| **Task Queue** | Celery & Redis |
| **Frontend** | HTMX, Django Templates, Tailwind CSS |
| **Storage** | Cloudinary |

---

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/git-bhupesh/chatterbox.git

2. Create and activate a virtual environment:
   python -m venv venv
   .\venv\Scripts\Activate.ps1

3. Install dependencies:
   pip install -r requirements.txt

4. Run Migrations:
   python manage.py migrate

5. Start the development server:
   python manage.py runserver

🤝 Contributing
 contributions are welcome! Feel free to open an issue or submit a pull request.
 ### How to update it on GitHub:
1. Open your project in **VS Code**.
2. Open the `README.md` file.
3. **Delete everything** currently in there.
4. **Paste** the code I gave you above.
5. **Save** the file.
6. In your terminal, run:
   ```powershell
   git add README.md
   git commit -m "Fixed README formatting"
   git push
