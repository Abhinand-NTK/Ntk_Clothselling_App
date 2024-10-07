# from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
#     def pre_social_login(self, request, sociallogin):
#         # Case when the social login already exists in the database
#         if sociallogin.is_existing:
#             return  # Account already exists, proceed as usual

#         # Case when the account does not exist but email matches
#         try:
#             user = User.objects.get(email=sociallogin.account.extra_data['email'])
#             sociallogin.connect(request, user)  # Connect the social account with the existing user
#         except User.DoesNotExist:
#             pass  # Account does not exist, continue with regular signup
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Case when the social login already exists in the database
        if sociallogin.is_existing:
            return  # Account already exists, proceed as usual

        # Case when the account does not exist but email matches
        try:
            user = User.objects.get(email=sociallogin.account.extra_data['email'])
            sociallogin.connect(request, user)  # Connect the social account with the existing user

        except User.DoesNotExist:
            # Account does not exist, so we proceed with account creation.
            # Modify user data before the user gets created
            user = sociallogin.user
            if not user.pk:  # If this is a new user
                user.is_verified = True  # Set your custom field to True
                user.save()  # Save the user

            # Proceed with the default signup logic
            pass  # Continue the signup process
