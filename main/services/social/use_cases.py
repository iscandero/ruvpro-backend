from main.models import AppUser, Social


def get_social_output_list_by_user(user: AppUser) -> list:
    socials_user = Social.objects.filter(user=user)

    instance_output_list_of_dicts = []
    if socials_user is not None:
        for social_network in socials_user:
            instance_output_list_of_dicts.append({
                'name': social_network.social_network.name,
                'url': social_network.url
            })

    return instance_output_list_of_dicts
