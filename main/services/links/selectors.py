from main.models import Link


def get_all_links():
    return Link.objects.all()
