🗨️ ChatterboxChatterbox is a full-stack social networking platform built with Django. It features real-time messaging, live notifications, and a dynamic social feed, providing a seamless user experience for connecting with others.🚀 Key FeaturesReal-Time Chat: Private and group messaging powered by Django Channels and WebSockets.Live Notifications: Instant alerts for likes, comments, and follows using HTMX and Signals.Dynamic Feed: A social wall where users can post images (via Cloudinary) and interact with content.Social Graph: Follow/Unfollow system and user search functionality.Typing Indicators: Real-time "User is typing..." status managed via Redis caching.Media Management: Secure image hosting and delivery through Cloudinary.🛠️ Tech StackComponentTechnologyBackendPython / DjangoReal-timeDjango Channels & DaphneDatabaseSQLite (Development) / PostgreSQL (Production ready)Task QueueCelery & RedisFrontendHTMX, Django Templates, Tailwind CSSStorageCloudinary📦 Installation & SetupClone the repository:Bashgit clone https://github.com/git-bhupesh/chatterbox.git
cd chatterbox
Create and activate a virtual environment:Bashpython -m venv venv
.\venv\Scripts\Activate.ps1  # On Windows
Install dependencies:Bashpip install -r requirements.txt
Set up Environment Variables:Create a .env file and add your credentials:PlaintextSECRET_KEY=your_django_secret_key
CLOUDINARY_CLOUD_NAME=your_name
CLOUDINARY_API_KEY=your_key
CLOUDINARY_API_SECRET=your_secret
Run Migrations:Bashpython manage.py migrate
Start the development server:Bashpython manage.py runserver
Note: Ensure Redis is running on 127.0.0.1:6379 for chat and typing indicators to function.📸 Screenshots(Pro-tip: Add some screenshots of your UI here later!)🤝 ContributingContributions are welcome! Feel free to open an issue or submit a pull request.
