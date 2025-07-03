import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import personal_blog.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal_blog.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            personal_blog.routing.websocket_urlpatterns
        )
    ),
})
