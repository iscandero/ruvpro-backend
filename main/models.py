from django.db import models
from django.db.models import Sum, Avg
from django.db.models.signals import post_save


class User(models.Model):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    # аватарка пользователя будет сохранена в  MEDIA_ROOT / users_avatar/ user_<id>/<filename>
    def user_avatar_path(self, filename):
        return 'users_avatar/' + 'user_{0}/{1}'.format(self.id, filename)

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    name = models.CharField(verbose_name="Имя пользователя", null=False, unique=False, blank=False, max_length=255)
    email = models.EmailField(verbose_name="email пользователя", null=True, blank=True)
    phone = models.CharField(verbose_name="Телефон пользователя", null=True, blank=True, max_length=255)
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
    name = models.CharField(verbose_name="Название соц.сети", unique=True, max_length=255)

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
    name = models.CharField(verbose_name="Название проекта", unique=True, max_length=255)
    proposed_income = models.FloatField(verbose_name="Предполагаемый заработок в проекте", unique=False, null=True,
                                        blank=True)
    is_archived = models.BooleanField(verbose_name="Флаг архивности проекта", unique=False, null=False, blank=False)
    owner_id = models.ForeignKey(to=User, verbose_name="ID Создателя", null=False, blank=False,
                                 on_delete=models.PROTECT)
    work_time = models.FloatField(verbose_name="Общее рабочее время", unique=False, null=False, blank=False, default=0)

    average_rate = models.FloatField(verbose_name="Средняя ставка", unique=False, null=False, blank=False, default=0)

    @staticmethod
    def calculate_general_work_time(sender, instance, **kwargs):
        calculate_work_time = sender.objects.filter(project_id=instance.project_id).aggregate(sum_time=Sum('work_time'))
        if calculate_work_time is None:
            calculate_work_time = 0
        instance.work_time = calculate_work_time['sum_time']

    @staticmethod
    def calculate_average_rate(sender, instance, **kwargs):
        calculate_rate = sender.objects.filter(project_id=instance.project_id).aggregate(avg_rate=Avg('rate'))
        if calculate_rate is None:
            calculate_rate = 0
        instance.average_rate = calculate_rate['avg_rate']

    def __str__(self):
        return f"Проект {self.id}: {self.name}"


class Role(models.Model):
    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    name = models.CharField(verbose_name="Название роли", unique=True, null=False, blank=False, max_length=255)
    description = models.TextField(verbose_name="Описание роли", null=True, blank=True)
    color = models.CharField(verbose_name="Цвет роли HEX", unique=False, null=False, blank=False, max_length=255)
    percentage = models.FloatField(verbose_name="Доля в процентах", unique=False, null=True, blank=True)
    amount = models.FloatField(verbose_name="Размер платы", unique=False, null=True, blank=True)
    author_id = models.ForeignKey(to=User, verbose_name="ID Создателя роли", on_delete=models.CASCADE)

    def __str__(self):
        return f"Роль {self.id}: {self.name}"


class Project_employee(models.Model):
    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    user_id = models.ForeignKey(to=User, verbose_name="ID Пользователя", on_delete=models.CASCADE)
    role_id = models.ForeignKey(to=Role, verbose_name="ID Роли пользователя", on_delete=models.CASCADE)
    rate = models.FloatField(verbose_name="Ставка рабочего", unique=False, null=False, blank=False)
    # Считать по ёбнутой формуле нахуй
    salary = models.FloatField(verbose_name="З/П рабочего", unique=False, null=False, blank=False)
    # work_time = models.FloatField(verbose_name="Рабочее время", unique=False, null=False, blank=False)
    project_id = models.ForeignKey(to=Project, verbose_name="ID Проекта", on_delete=models.CASCADE)

    def __str__(self):
        return f"Работник {self.id}: User_id {self.user_id.id}"


post_save.connect(Project.calculate_average_rate, sender=Project_employee)


class Time_entry(models.Model):
    class Meta:
        verbose_name = "Рабочее время работника"
        verbose_name_plural = "Рабочие времена работников"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    initiator = models.ForeignKey(to=User, verbose_name="ID Инициатора", unique=False, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(to=Project_employee, verbose_name="ID Рабочего", on_delete=models.CASCADE)
    # Костыль, при реализациях API учитывать
    project_id = models.ForeignKey(to=Project, verbose_name="ID Проекта", on_delete=models.CASCADE, default=0)
    date = models.DateField(verbose_name="Дата", unique=False, null=False,
                            blank=False)
    work_time = models.FloatField(verbose_name="Выданное рабочее время", unique=False, null=False, blank=False)

    def __str__(self):
        return f"Рабочее время {self.id} работнику {self.employee_id.id}"


post_save.connect(Project.calculate_general_work_time, sender=Time_entry)


class Transactions(models.Model):
    class Meta:
        verbose_name = "Начисление работника"
        verbose_name_plural = "Начисления работников"

    TRANSACTIONSTYPES = (
        ('SAL', 'SALARY'),
        ('ADV', 'ADVANCE'),
        ('REPAIR', 'RESPONSIBLE FOR REPAIR'),
        ('AMORT', 'AMORTIZATION OF INSTRUMENT'),
        ('TIME', 'RESPONSIBLE OF TIME'),
    )

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    employee_id = models.ForeignKey(to=Project_employee, verbose_name="ID Рабочего", on_delete=models.CASCADE)
    transaction_date = models.DateField(verbose_name="Дата транзакции", blank=False, null=False)
    type_accrual = models.CharField(verbose_name="Тип начисления", choices=TRANSACTIONSTYPES, max_length=255)
    amount = models.FloatField(verbose_name="Размер начисления", null=False, blank=False, unique=False)

    def __str__(self):
        return f"Начисление {self.id} работнику {self.employee_id.id}"


class Employee_Statistics(models.Model):
    class Meta:
        verbose_name = "Статистика работника"
        verbose_name_plural = "Статистики работников"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    employee_id = models.ForeignKey(to=Project_employee, verbose_name="ID Пользователя", on_delete=models.CASCADE)
    start_date = models.DateField(verbose_name="Дата с которой считать статистику", unique=False, null=False,
                                  blank=False)
    end_date = models.DateField(verbose_name="Дата до которой считать статистику", unique=False, null=False,
                                blank=False)

    income = models.FloatField(verbose_name="Доход", null=False, blank=False, unique=False, default=0)

    # work_time - суммарное время, которое выдавали в Time_entry этому пассажиру

    work_time = models.FloatField(verbose_name="Рабочее время", unique=False, null=False, blank=False, default=0)

    # Считать rate - УТОЧНИТЬ

    @staticmethod
    def calculate_statictics_data(sender, instance, **kwargs):
        salary_transactions = Transactions.objects.filter(employee_id=instance.employee_id,
                                                          transaction_date__gte=instance.start_date,
                                                          transaction_date__lte=instance.end_date,
                                                          type_accrual='SAL').aggregate(
            amount_sum=Sum('amount'))

        advance_transactions = Transactions.objects.filter(employee_id=instance.employee_id,
                                                           transaction_date__gte=instance.start_date,
                                                           transaction_date__lte=instance.end_date,
                                                           type_accrual='ADV').aggregate(
            amount_sum=Sum('amount'))

        no_salary_advance_transactions = Transactions.objects.filter(employee_id=instance.employee_id,
                                                                     transaction_date__gte=instance.start_date,
                                                                     transaction_date__lte=instance.end_date).exclude(
            type_accrual='SAL').exclude(type_accrual='ADV').aggregate(amount_sum=Sum('amount'))

        if salary_transactions is None:
            salary_transactions = 0
        if advance_transactions is None:
            advance_transactions = 0
        if no_salary_advance_transactions is None:
            no_salary_advance_transactions = 0

        instance.income = salary_transactions['amount_sum'] - advance_transactions['amount_sum'] + \
                          no_salary_advance_transactions['amount_sum']

        sum_work_time = Time_entry.objects.filter(employee_id=instance.employee_id, date__gte=instance.start_date,
                                                  date__lte=instance.end_date).aggregate(amount_sum=Sum('work_time'))
        if sum_work_time is None:
            sum_work_time = 0

        instance.work_time = sum_work_time

    def __str__(self):
        return f"Статистика {self.id} работника {self.employee_id.id}"


post_save.connect(Employee_Statistics.calculate_statictics_data, sender=Transactions)


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
