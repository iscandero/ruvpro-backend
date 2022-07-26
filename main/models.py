from django.db import models

from main.const_data.currency_codes import currency_list


class AppUser(models.Model):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    # аватарка пользователя будет сохранена в  MEDIA_ROOT / users_avatar/ user_<id>/<filename>
    def user_avatar_path(self, filename):
        return 'users_avatar/' + 'user_{0}/{1}'.format(self.id, filename)

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    name = models.CharField(verbose_name="Имя пользователя", null=False, unique=False, blank=False, max_length=255,
                            default='Имя')
    email = models.EmailField(verbose_name="email пользователя", unique=True, null=False, blank=False,
                              default='admin@admin.com')
    phone = models.CharField(verbose_name="Телефон пользователя", null=True, blank=False, max_length=255)
    avatar = models.ImageField(verbose_name="Аватар пользователя", upload_to=user_avatar_path, null=True,
                               blank=True)
    bio = models.TextField(verbose_name="Биография пользователя", null=True, blank=True)
    authority = models.IntegerField(verbose_name="Полномочия пользователя", null=False, blank=False, unique=False)
    is_register = models.BooleanField(verbose_name='Флаг зарегистрированого пользователя', null=False, blank=False,
                                      default=True)
    currency = models.CharField(verbose_name='Валюта', null=True, blank=True, choices=currency_list, default='RUB',
                                max_length=3)

    def __str__(self):
        return f"Пользователь {self.id}: {self.name}"


class AuthData(models.Model):
    class Meta:
        verbose_name = "Токены пользователя"
        verbose_name_plural = "Токены пользователей"

    user = models.ForeignKey(to=AppUser, verbose_name="Пользователь", on_delete=models.CASCADE)
    token_data = models.TextField(verbose_name="token", unique=True, null=False, blank=False)
    refresh_token_data = models.TextField(verbose_name="refresh token", unique=True, null=False, blank=False)
    valid_until = models.DateField(verbose_name='Срок годности токена', null=False, blank=False)

    def __str__(self):
        return f"Auth data user - {self.user.name}"


class SocialNetwork(models.Model):
    class Meta:
        verbose_name = "Социальная сеть"
        verbose_name_plural = "Социальные сети"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    name = models.CharField(verbose_name="Название соц.сети", unique=True, max_length=255)

    def __str__(self):
        return f"Соц.сеть {self.id}: {self.name}"


class Social(models.Model):
    class Meta:
        verbose_name = "Связь пользователя и социальной сети"
        verbose_name_plural = "Связи пользователей и социальных сетей"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    user = models.ForeignKey(to=AppUser, verbose_name="ID Пользователя", on_delete=models.CASCADE)
    social_network = models.ForeignKey(to=SocialNetwork, verbose_name="ID соц.сети", on_delete=models.CASCADE)
    url = models.TextField(verbose_name="URL", null=True, blank=True)

    def __str__(self):
        return f"Соц.сеть {self.social_network.id}: {self.social_network.name} - Пользователь {self.user}"


class Project(models.Model):
    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    name = models.CharField(verbose_name="Название проекта", unique=False, max_length=255)
    budget = models.FloatField(verbose_name="Бюджет проекта", unique=False, null=True,
                               blank=True)
    is_archived = models.BooleanField(verbose_name="Флаг архивности проекта", unique=False, null=False, blank=False)
    owner = models.ForeignKey(to=AppUser, verbose_name="ID Создателя", null=False, blank=False,
                              on_delete=models.PROTECT)
    work_time = models.FloatField(verbose_name="Общее рабочее время", unique=False, null=True, blank=False, default=0)

    average_rate = models.FloatField(verbose_name="Средняя ставка", unique=False, null=False, blank=False, default=0)

    sum_salary = models.FloatField(verbose_name="Суммарная зп, всех работников", null=True, blank=True,
                                   unique=False,
                                   default=0)

    masters_work_time = models.FloatField(verbose_name="Суммарное рабочее время всех мастеров проекта",
                                          unique=False, null=True, blank=True,
                                          default=0)

    mentors_work_time = models.FloatField(verbose_name="Суммарное рабочее время всех менторов проекта", unique=False,
                                          null=True,
                                          blank=True,
                                          default=0)

    assists_work_time = models.FloatField(verbose_name="Суммарное рабочее время всех подсобных проекта", unique=False,
                                          null=True,
                                          blank=True,
                                          default=0)

    interns_work_time = models.FloatField(verbose_name="Суммарное рабочее время всех интернов проекта", unique=False,
                                          null=True,
                                          blank=True,
                                          default=0)

    pupils_work_time = models.FloatField(verbose_name="Суммарное рабочее время всех учеников проекта", unique=False,
                                         null=True,
                                         blank=True,
                                         default=0)

    currency = models.CharField(verbose_name='Валюта', null=False, blank=False, choices=currency_list, default='RUB',
                                max_length=3)

    def __str__(self):
        return f"Проект {self.id}: {self.name}"


class Role(models.Model):
    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    name = models.CharField(verbose_name="Название роли", unique=False, null=False, blank=False, max_length=255)
    description = models.TextField(verbose_name="Описание роли", null=True, blank=True)
    color = models.CharField(verbose_name="Цвет роли HEX", unique=False, null=False, blank=False, max_length=255)
    percentage = models.FloatField(verbose_name="Доля в процентах", unique=False, null=True, blank=True)
    amount = models.FloatField(verbose_name="Размер платы", unique=False, null=True, blank=True)
    author = models.ForeignKey(to=AppUser, verbose_name="ID Создателя роли", on_delete=models.CASCADE)

    # Флаг базовой роли, если - True, то роль не проектная, а создалась автоматически для платного пользователя
    is_base = models.BooleanField(verbose_name='Флаг базовой роли', null=False, blank=False, default=False)

    # Если тип = 1, то данную роль нельзя присвоить работнику, эта роль относится к дополнительным распределениям
    type = models.IntegerField(verbose_name='Тип роли', null=False, blank=True, default=0)

    # не null, если роль - проектная
    project = models.ForeignKey(to=Project, verbose_name='Проект, которому принадлежит роль', null=True, blank=True,
                                on_delete=models.CASCADE)

    def __str__(self):
        return f"Роль {self.id}: {self.name}"


class ProjectEmployee(models.Model):
    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    user = models.ForeignKey(to=AppUser, verbose_name="ID Пользователя", on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, verbose_name="ID Проекта", on_delete=models.CASCADE)
    role = models.ForeignKey(to=Role, verbose_name="ID Роли пользователя", on_delete=models.CASCADE)
    advance = models.FloatField(verbose_name="Размер аванса", null=False, blank=False, unique=False, default=0)
    salary = models.FloatField(verbose_name="Размер зп, считается автоматически", null=True, blank=True, unique=False,
                               default=0)
    work_time = models.FloatField(verbose_name="Суммарное рабочее время", unique=False, null=True, blank=True,
                                  default=0)

    def __str__(self):
        return f"Работник {self.id}: User {self.user}, {self.project.name}"


class HistoryAdvance(models.Model):
    class Meta:
        verbose_name = "Аванс работника"
        verbose_name_plural = "Авансы работников"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    date = models.DateField(verbose_name='Дата выдачи', null=True, blank=True)
    employee = models.ForeignKey(to=ProjectEmployee, verbose_name="ID Рабочего", on_delete=models.CASCADE)
    advance = models.FloatField(verbose_name="Размер аванса", null=True, blank=True, unique=False, default=0)

    def __str__(self):
        return f"Аванс {self.id} - работник {self.employee.id}"


class TimeEntry(models.Model):
    class Meta:
        verbose_name = "Рабочее время работника"
        verbose_name_plural = "Рабочие времена работников"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    initiator = models.ForeignKey(to=AppUser, verbose_name="ID Инициатора", unique=False, on_delete=models.CASCADE)
    employee = models.ForeignKey(to=ProjectEmployee, verbose_name="ID Рабочего", on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Дата", unique=False, null=False,
                            blank=False)
    work_time = models.FloatField(verbose_name="Выданное рабочее время", unique=False, null=False, blank=False)

    def __str__(self):
        return f"Рабочее время {self.id} работника {self.employee.id}"


class HistoryWorker(models.Model):
    class Meta:
        verbose_name = "История работника"
        verbose_name_plural = "Истории работников"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    date_change = models.DateField(verbose_name='Дата внесения изменений', null=True, blank=True, auto_now=True)
    employee = models.ForeignKey(to=ProjectEmployee, verbose_name="ID Рабочего", on_delete=models.CASCADE)
    salary = models.FloatField(verbose_name="Размер зп", null=True, blank=True, unique=False, default=0)
    rate = models.FloatField(verbose_name="Ставка рабочего", null=True, blank=True, unique=False, default=0)
    work_time = models.FloatField(verbose_name="Суммарное рабочее время", unique=False, null=True, blank=True,
                                  default=0)

    def __str__(self):
        return f"История {self.id} - работник {self.employee.id}"


class HistoryProject(models.Model):
    class Meta:
        verbose_name = "История проекта"
        verbose_name_plural = "Истории проектов"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    date_change = models.DateField(verbose_name='Дата внесения изменений', null=True, blank=True, auto_now=True)
    project = models.ForeignKey(to=Project, verbose_name="ID Проекта", on_delete=models.CASCADE, default=0)
    income = models.FloatField(verbose_name="Доход всех работников", null=True, blank=True, unique=False, default=0)

    def __str__(self):
        return f"История {self.id} проекта {self.project.id}"


class Team(models.Model):
    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    owner = models.OneToOneField(to=AppUser, verbose_name="ID Создателя", null=False, blank=False, related_name='owner',
                                 on_delete=models.CASCADE)
    participants = models.ManyToManyField(to=AppUser, verbose_name="Участники команды", null=True, blank=True,
                                          related_name='participants')

    def __str__(self):
        return f"Команда {self.id}"


class ProjectTimeEntryHistory(models.Model):
    class Meta:
        verbose_name = "Рабочие времена на проекте"
        verbose_name_plural = "Рабочие времена на проекте"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    project = models.ForeignKey(to=Project, verbose_name="Проект", on_delete=models.CASCADE)
    work_time = models.FloatField(verbose_name="Общее рабочее время", unique=False, null=True, blank=False, default=0)

    def __str__(self):
        return f"Изменение времени {self.id} проекта {self.project.id}"
