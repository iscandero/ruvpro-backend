from main.models import AppUser, Team


def get_team_by_owner(owner: AppUser):
    team = Team.objects.filter(owner=owner).first()
    if team is not None:
        return team
    else:
        team = Team.objects.create(owner=owner)
        team.participants.add(owner)
        return team


def is_user_in_team(user: AppUser, team: Team) -> bool:
    return team.participants.filter(pk=user.id).exists()
