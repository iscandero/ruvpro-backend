from django.db import models
from django.db.models import Sum, Avg
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
    user_id = models.ForeignKey(to=AppUser, verbose_name="ID Пользователя", on_delete=models.CASCADE)
    social_network_id = models.ForeignKey(to=SocialNetwork, verbose_name="ID соц.сети", on_delete=models.CASCADE)
    url = models.TextField(verbose_name="URL", null=True, blank=True)

    def __str__(self):
        return f"Соц.сеть {self.social_network_id.id}: {self.social_network_id.name} - Пользователь {self.user_id}"


class Project(models.Model):
    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    name = models.CharField(verbose_name="Название проекта", unique=False, max_length=255)
    budget = models.FloatField(verbose_name="Бюджет проекта", unique=False, null=True,
                               blank=True)
    is_archived = models.BooleanField(verbose_name="Флаг архивности проекта", unique=False, null=False, blank=False)
    owner_id = models.ForeignKey(to=AppUser, verbose_name="ID Создателя", null=False, blank=False,
                                 on_delete=models.PROTECT)
    work_time = models.FloatField(verbose_name="Общее рабочее время", unique=False, null=False, blank=False, default=0)

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
    user_id = models.ForeignKey(to=AppUser, verbose_name="ID Пользователя", on_delete=models.CASCADE)
    project_id = models.ForeignKey(to=Project, verbose_name="ID Проекта", on_delete=models.CASCADE)
    rate = models.FloatField(verbose_name="Ставка рабочего", unique=False, null=False, blank=False)
    role_id = models.ForeignKey(to=Role, verbose_name="ID Роли пользователя", on_delete=models.CASCADE)
    advance = models.FloatField(verbose_name="Размер аванса", null=True, blank=True, unique=False)
    salary = models.FloatField(verbose_name="Размер зп, считается автоматически", null=True, blank=True, unique=False,
                               default=0)

    @staticmethod
    def calculate_project_average_rate(sender, instance, created, update_fields, **kwargs):
        if created or update_fields == {'rate'}:
            avg_rate = sender.objects.filter(project_id=instance.project_id).aggregate(avg_rate=Avg('rate'))
            instance.project_id.average_rate = avg_rate['avg_rate']

    def __str__(self):
        return f"Работник {self.id}: User_id {self.user_id}"


post_save.connect(ProjectEmployee.calculate_project_average_rate, sender=ProjectEmployee)


class HistoryRate(models.Model):
    class Meta:
        verbose_name = "История ставок работника"
        verbose_name_plural = "Истории ставок работников"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    rate = models.FloatField(verbose_name="Ставка рабочего", unique=False, null=False, blank=False)
    employee_id = models.ForeignKey(to=ProjectEmployee, verbose_name="ID Рабочего", on_delete=models.CASCADE)
    date_change = models.DateField(verbose_name='Дата внесения изменений', null=True, blank=True, auto_now=True)

    @receiver(post_save, sender=ProjectEmployee)
    def write_rate_to_history_model(self, instance, created, update_fields, **kwargs):
        if created or update_fields == {'rate'}:
            HistoryRate.objects.create(rate=instance.rate, employee_id=instance)

    def __str__(self):
        return f"Ставка {self.id} работника {self.employee_id.id}"


class HistoryAdvance(models.Model):
    class Meta:
        verbose_name = "История авансов работника"
        verbose_name_plural = "Истории авансов работников"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    advance = models.FloatField(verbose_name="Размер аванса", null=False, blank=False, unique=False)
    employee_id = models.ForeignKey(to=ProjectEmployee, verbose_name="ID Рабочего", on_delete=models.CASCADE)
    date_change = models.DateField(verbose_name='Дата внесения изменений', null=True, blank=True, auto_now=True)

    @receiver(post_save, sender=ProjectEmployee)
    def write_advance_to_history_model(self, instance, created, update_fields, **kwargs):
        if created or update_fields == {'advance'}:
            if instance.advance is not None:
                HistoryAdvance.objects.create(advance=instance.advance, employee_id=instance)

    def __str__(self):
        return f"Аванс {self.id} - работник {self.employee_id.id}"


class TimeEntry(models.Model):
    class Meta:
        verbose_name = "Рабочее время работника"
        verbose_name_plural = "Рабочие времена работников"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    initiator = models.ForeignKey(to=AppUser, verbose_name="ID Инициатора", unique=False, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(to=ProjectEmployee, verbose_name="ID Рабочего", on_delete=models.CASCADE)
    # project_id = models.ForeignKey(to=Project, verbose_name="ID Проекта", on_delete=models.CASCADE, default=0)
    date = models.DateField(verbose_name="Дата", unique=False, null=False,
                            blank=False)
    work_time = models.FloatField(verbose_name="Выданное рабочее время", unique=False, null=False, blank=False)

    @staticmethod
    def calculate_project_work_time(instance, created, update_fields, **kwargs):
        if created or update_fields == {'work_time'}:
            project = instance.employee_id.project_id
            project.work_time += instance.work_time

    def __str__(self):
        return f"Рабочее время {self.id} работника {self.employee_id.id}"


post_save.connect(TimeEntry.calculate_project_work_time, sender=TimeEntry)


class EmployeeStatistics(models.Model):
    class Meta:
        verbose_name = "Статистика работника"
        verbose_name_plural = "Статистики работников"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    employee_id = models.ForeignKey(to=ProjectEmployee, verbose_name="ID Пользователя", on_delete=models.CASCADE)
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
        return f"Статистика {self.id} работника {self.employee_id.id}"


class ProjectStatistics(models.Model):
    class Meta:
        verbose_name = "Статистика проекта"
        verbose_name_plural = "Статистики проектов"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    project_id = models.ForeignKey(to=Project, verbose_name="ID Проекта", on_delete=models.CASCADE, default=0)
    start_date = models.DateField(verbose_name="Дата с которой считать статистику", unique=False, null=False,
                                  blank=False)
    end_date = models.DateField(verbose_name="Дата до которой считать статистику", unique=False, null=False,
                                blank=False)
    income = models.FloatField(verbose_name="Доход всех работников", null=False, blank=False, unique=False, default=0)

    def __str__(self):
        return f"Статистика {self.id} проекта {self.project_id.id}"


class AdvanceStatistics(models.Model):
    class Meta:
        verbose_name = "Статистика аванса"
        verbose_name_plural = "Статистики авансов"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    employee_id = models.ForeignKey(to=ProjectEmployee, verbose_name="ID Пользователя", on_delete=models.CASCADE)
    start_date = models.DateField(verbose_name="Дата с которой считать статистику", unique=False, null=False,
                                  blank=False)
    end_date = models.DateField(verbose_name="Дата до которой считать статистику", unique=False, null=False,
                                blank=False)

    # доход авансов
    advance = models.FloatField(verbose_name="Сумма авансов работника", null=False, blank=False, unique=False,
                                default=0)

    def __str__(self):
        return f"Статистика авансов {self.id} работника {self.employee_id.id}"


class Team(models.Model):
    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    owner_id = models.ForeignKey(to=AppUser, verbose_name="ID Создателя", null=False, blank=False,
                                 on_delete=models.PROTECT)

    def __str__(self):
        return f"Команда {self.id}"


class UsersTeam(models.Model):
    class Meta:
        verbose_name = "Связь команды с участником"
        verbose_name_plural = "Связи команды с участниками"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    user_id = models.ForeignKey(to=AppUser, verbose_name="ID Пользователя", on_delete=models.CASCADE)
    team_id = models.ForeignKey(to=Team, verbose_name="ID команды", on_delete=models.CASCADE)

    def __str__(self):
        return f"Команда {self.team_id.id} - Пользователь {self.user_id.id}"
