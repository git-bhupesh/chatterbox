# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatterbox.settings')

# application = get_asgi_application()


# # chatterbox/asgi.py
# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# import chat.routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatterbox.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             chat.routing.websocket_urlpatterns
#         )
#     ),
# })


import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Set settings before importing routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatterbox.settings')

# Initialize Django ASGI application early to ensure AppRegistry is populated
django_asgi_app = get_asgi_application()

import chat.routing  # Import this AFTER get_asgi_application()

application = ProtocolTypeRouter({
    # Handle traditional HTTP requests
    "http": django_asgi_app,
    
    # Handle WebSocket connections
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})