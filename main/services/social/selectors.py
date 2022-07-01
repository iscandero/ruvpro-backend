from main.models import AppUser, Social


def get_socials_by_user(user: AppUser):
    return Social.objects.filter(user=user)
