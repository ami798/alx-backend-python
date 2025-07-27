# chats/auth.py

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Basic view wrappers to ensure file is not empty
def get_token_view():
    return TokenObtainPairView.as_view()

def refresh_token_view():
    return TokenRefreshView.as_view()
