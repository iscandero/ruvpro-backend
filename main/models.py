from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver


class AppUser(models.Model):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    # аватарка пользователя будет сохранена в  MEDIA_ROOT / users_avatar/ user_<id>/<filename>
    def user_avatar_path(self, filename):
        return 'users_avatar/' + 'user_{0}/{1}'.format(self.id, filename)

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    token_data = models.TextField(verbose_name="token", unique=False, null=True, blank=True)
    name = models.CharField(verbose_name="Имя пользователя", null=False, unique=False, blank=False, max_length=255)
    email = models.EmailField(verbose_name="email пользователя", unique=True, null=False, blank=False,
                              default='admin@admin.com')
    phone = models.CharField(verbose_name="Телефон пользователя", unique=True, null=False, blank=False, max_length=255,
                             default='+777')
    avatar = models.ImageField(verbose_name="Аватар пользователя", upload_to=user_avatar_path, null=True,
                               blank=True)
    bio = models.TextField(verbose_name="Биография пользователя", null=True, blank=True)
    authority = models.IntegerField(verbose_name="Полномочия пользователя", null=False, blank=False, unique=False)

    def __str__(self):
        return f"Пользователь {self.id}: {self.name}"


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

    # Флаг базовой роли, если - True, то роль создалась
    is_base = models.BooleanField(verbose_name='Флаг базовой роли', null=False, blank=False, default=False)

    # Если тип = 1, то данную роль нельзя присвоить работнику, эта роль относится к дополнительным распределениям
    type = models.IntegerField(verbose_name='Тип роли', null=False, blank=True, default=0)

    # Если тип = 1, то не null.
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
    rate = models.FloatField(verbose_name="Ставка рабочего", unique=False, null=True, blank=True, default=0)
    role = models.ForeignKey(to=Role, verbose_name="ID Роли пользователя", on_delete=models.CASCADE)
    advance = models.FloatField(verbose_name="Размер аванса", null=True, blank=True, unique=False)
    salary = models.FloatField(verbose_name="Размер зп, считается автоматически", null=True, blank=True, unique=False,
                               default=0)
    work_time = models.FloatField(verbose_name="Суммарное рабочее время", unique=False, null=True, blank=False,
                                  default=0)

    @staticmethod
    def calculate_project_average_rate(sender, instance, created, update_fields, **kwargs):
        if created or update_fields == {'rate'}:
            avg_rate = sender.objects.filter(project=instance.project).aggregate(avg_rate=Avg('rate'))
            instance.project.average_rate = avg_rate['avg_rate']

    def __str__(self):
        return f"Работник {self.id}: User {self.user}"


post_save.connect(ProjectEmployee.calculate_project_average_rate, sender=ProjectEmployee)


class HistoryRate(models.Model):
    class Meta:
        verbose_name = "История ставок работника"
        verbose_name_plural = "Истории ставок работников"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    rate = models.FloatField(verbose_name="Ставка рабочего", unique=False, null=False, blank=False)
    employee = models.ForeignKey(to=ProjectEmployee, verbose_name="ID Рабочего", on_delete=models.CASCADE)
    date_change = models.DateField(verbose_name='Дата внесения изменений', null=True, blank=True, auto_now=True)

    @receiver(post_save, sender=ProjectEmployee)
    def write_rate_to_history_model(sender, instance, created, update_fields, **kwargs):
        if created or update_fields == {'rate'}:
            HistoryRate.objects.create(rate=instance.rate, employee=instance)

    def __str__(self):
        return f"Ставка {self.id} работника {self.employee.id}"


class HistoryAdvance(models.Model):
    class Meta:
        verbose_name = "История авансов работника"
        verbose_name_plural = "Истории авансов работников"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    advance = models.FloatField(verbose_name="Размер аванса", null=False, blank=False, unique=False)
    employee = models.ForeignKey(to=ProjectEmployee, verbose_name="ID Рабочего", on_delete=models.CASCADE)
    date_change = models.DateField(verbose_name='Дата внесения изменений', null=True, blank=True, auto_now=True)

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


class EmployeeStatistics(models.Model):
    class Meta:
        verbose_name = "Статистика работника"
        verbose_name_plural = "Статистики работников"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    employee = models.ForeignKey(to=ProjectEmployee, verbose_name="ID Пользователя", on_delete=models.CASCADE)
    start_date = models.DateField(verbose_name="Дата с которой считать статистику", unique=False, null=False,
                                  blank=False)
    end_date = models.DateField(verbose_name="Дата до которой считать статистику", unique=False, null=False,
                                blank=False)

    # доход
    income = models.FloatField(verbose_name="Доход", null=False, blank=False, unique=False, default=0)

    # work_time - суммарное время, которое выдавали в TimeEntry этому пассажиру
    work_time = models.FloatField(verbose_name="Рабочее время", unique=False, null=False, blank=False, default=0)

    # Последняя ставка
    rate = models.FloatField(verbose_name="Текущая ставка рабочего", unique=False, null=False, blank=False, default=0)

    def __str__(self):
        return f"Статистика {self.id} работника {self.employee.id}"


class ProjectStatistics(models.Model):
    class Meta:
        verbose_name = "Статистика проекта"
        verbose_name_plural = "Статистики проектов"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    project = models.ForeignKey(to=Project, verbose_name="ID Проекта", on_delete=models.CASCADE, default=0)
    start_date = models.DateField(verbose_name="Дата с которой считать статистику", unique=False, null=False,
                                  blank=False)
    end_date = models.DateField(verbose_name="Дата до которой считать статистику", unique=False, null=False,
                                blank=False)
    income = models.FloatField(verbose_name="Доход всех работников", null=False, blank=False, unique=False, default=0)

    def __str__(self):
        return f"Статистика {self.id} проекта {self.project.id}"


class AdvanceStatistics(models.Model):
    class Meta:
        verbose_name = "Статистика аванса"
        verbose_name_plural = "Статистики авансов"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    employee = models.ForeignKey(to=ProjectEmployee, verbose_name="ID Пользователя", on_delete=models.CASCADE)
    start_date = models.DateField(verbose_name="Дата с которой считать статистику", unique=False, null=False,
                                  blank=False)
    end_date = models.DateField(verbose_name="Дата до которой считать статистику", unique=False, null=False,
                                blank=False)

    # доход авансов
    advance = models.FloatField(verbose_name="Сумма авансов работника", null=False, blank=False, unique=False,
                                default=0)

    def __str__(self):
        return f"Статистика авансов {self.id} работника {self.employee.id}"


class Team(models.Model):
    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    owner = models.OneToOneField(to=AppUser, verbose_name="ID Создателя", null=False, blank=False, related_name='owner',
                                 on_delete=models.PROTECT)
    participants = models.ManyToManyField(to=AppUser, verbose_name="Участники команды", null=True, blank=True,
                                          related_name='participants')

    def __str__(self):
        return f"Команда {self.id}"

# class UsersTeam(models.Model):
#     class Meta:
#         verbose_name = "Связь команды с участником"
#         verbose_name_plural = "Связи команды с участниками"
#
#     id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
#     user = models.ForeignKey(to=AppUser, verbose_name="ID Пользователя", on_delete=models.CASCADE)
#     team = models.ForeignKey(to=Team, verbose_name="ID команды", on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f"Команда {self.team.id} - Пользователь {self.user.id}"
