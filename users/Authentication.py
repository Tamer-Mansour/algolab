from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class UserAuthentication(TokenAuthentication):
    def authenticate(self, request):
        result = super().authenticate(request)

        if result is None:
            return None

        user, token = result

        # Check if the user is a student
        if not user.is_student:
            raise AuthenticationFailed('Invalid credentials')

        return user, token
