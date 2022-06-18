from django.db import models


class User(models.Model):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    # аватарка пользователя будет сохранена в  MEDIA_ROOT / users_avatar/ user_<id>/<filename>
    def user_avatar_path(self, filename):
        return 'users_avatar/' + 'user_{0}/{1}'.format(self.id, filename)

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    name = models.CharField(verbose_name="Имя пользователя", null=False, unique=False, blank=False)
    email = models.EmailField(verbose_name="email пользователя", null=True, blank=True)
    phone = models.CharField(verbose_name="Телефон пользователя", null=True, blank=True)
    avatar = models.ImageField(verbose_name="Аватар пользователя", upload_to=user_avatar_path, null=True,
                               blank=True)
    bio = models.TextField(verbose_name="Биография пользователя", null=True, blank=True)
    authority = models.IntegerField(verbose_name="Полномочия пользователя", null=True, blank=True, unique=False)

    def __str__(self):
        return f"Пользователь {self.id}: {self.name}"


class SocialNetwork(models.Model):
    class Meta:
        verbose_name = "Социальная сеть"
        verbose_name_plural = "Социальные сети"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    name = models.CharField(verbose_name="Название соц.сети", unique=True)

    def __str__(self):
        return f"Соц.сеть {self.id}: {self.name}"


class Social(models.Model):
    class Meta:
        verbose_name = "Связь пользователя и социальной сети"
        verbose_name_plural = "Связи пользователей и социальных сетей"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    user_id = models.ForeignKey(to=User, verbose_name="ID Пользователя", on_delete=models.CASCADE)
    social_network_id = models.ForeignKey(to=SocialNetwork, verbose_name="ID соц.сети", on_delete=models.CASCADE)

    def __str__(self):
        return f"Соц.сеть {self.social_network_id.id}: {self.social_network_id.name} - Пользователь {self.user_id.id}"


class Project(models.Model):
    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    name = models.CharField(verbose_name="Название проекта", unique=True)
    is_archived = models.BooleanField(verbose_name="Флаг архивности проекта", unique=False, null=False, blank=False)
    owner_id = models.ForeignKey(to=User, verbose_name="ID Создателя", null=False, blank=False,
                                 on_delete=models.PROTECT)

    # proposed income & work_time & average_rate ??

    def __str__(self):
        return f"Проект {self.id}: {self.name}"


class Role(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    name = models.CharField(verbose_name="Название роли", unique=True, null=False, blank=False)
    description = models.TextField(verbose_name="Описание роли", null=True, blank=True)
    color = models.CharField(verbose_name="Цвет роли HEX", unique=False, null=False, blank=False)
    percentage = models.FloatField(verbose_name="Доля в процентах", unique=False, null=True, blank=True)
    amount = models.FloatField(verbose_name="Размер платы", unique=False, null=True, blank=True)
    author_id = models.ForeignKey(to=User, verbose_name="ID Создателя роли", on_delete=models.CASCADE)

    def __str__(self):
        return f"Роль {self.id}: {self.name}"


class Project_employee(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    user_id = models.ForeignKey(to=User, verbose_name="ID Пользователя", on_delete=models.CASCADE)
    role_id = models.ForeignKey(to=Role, verbose_name="ID Роли пользователя", on_delete=models.CASCADE)
    rate = models.FloatField(verbose_name="Ставка рабочего", unique=False, null=False, blank=False)
    advance = models.FloatField(verbose_name="Аванс рабочего", unique=False, null=False, blank=False)
    salary = models.FloatField(verbose_name="З/П рабочего", unique=False, null=False, blank=False)
    work_time = models.FloatField(verbose_name="Рабочее время", unique=False, null=False, blank=False)
    project_id = models.ForeignKey(to=Project, verbose_name="ID Проекта", on_delete=models.CASCADE)

    def __str__(self):
        return f"Рабочий {self.id}: User_id {self.user_id.id}"


# ???
class Time_entry(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    initiator = models.ForeignKey(to=User, verbose_name="ID Инициатора", unique=False, on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Дата", unique=False, null=False,
                            blank=False)
    # employee


class Team(models.Model):
    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    owner_id = models.ForeignKey(to=User, verbose_name="ID Создателя", null=False, blank=False,
                                 on_delete=models.PROTECT)

    def __str__(self):
        return f"Команда {self.id}"


class UsersTeam(models.Model):
    class Meta:
        verbose_name = "Связь команды с участником"
        verbose_name_plural = "Связи команды с участниками"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    user_id = models.ForeignKey(to=User, verbose_name="ID Пользователя", on_delete=models.CASCADE)
    team_id = models.ForeignKey(to=Team, verbose_name="ID команды", on_delete=models.CASCADE)

    def __str__(self):
        return f"Команда {self.team_id.id} - Пользователь {self.user_id.id}"
