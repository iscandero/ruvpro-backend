from django.db import models
from django.db.models import Sum, Avg
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(models.Model):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    # аватарка пользователя будет сохранена в  MEDIA_ROOT / users_avatar/ user_<id>/<filename>
    def user_avatar_path(self, filename):
        return 'users_avatar/' + 'user_{0}/{1}'.format(self.id, filename)

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    token_data = models.TextField(verbose_name="token", unique=False, null=True, blank=True)
    name = models.CharField(verbose_name="Имя пользователя", null=False, unique=False, blank=False, max_length=255)
    email = models.EmailField(verbose_name="email пользователя", unique=True, null=False, blank=False, default='admin@admin.com')
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
    user_id = models.ForeignKey(to=User, verbose_name="ID Пользователя", on_delete=models.CASCADE)
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
    owner_id = models.ForeignKey(to=User, verbose_name="ID Создателя", null=False, blank=False,
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
    author_id = models.ForeignKey(to=User, verbose_name="ID Создателя роли", on_delete=models.CASCADE)
    is_base = models.BooleanField(verbose_name='Флаг бозовой роли', null=False, blank=False, default=False)

    # При создании платника создать ему прототипы базовых ролей, которые уже созданы
    @receiver(post_save, sender=User)
    def create_base_roles(sender, instance, created, update_fields, **kwargs):
        admin = instance
        if (created or update_fields == {'authority'}) and admin.authority == 1:
            if not Role.objects.filter(name='Мастер', author_id=admin):
                copy_base_instance = Role.objects.filter(name='Мастер').first()
                copy_base_name = copy_base_instance.name
                copy_base_description = copy_base_instance.description
                copy_base_color = copy_base_instance.color
                copy_base_percentage = copy_base_instance.percentage
                copy_base_amount = copy_base_instance.amount
                data_to_create = {
                    'name': copy_base_name,
                    'description': copy_base_description,
                    'color': copy_base_color,
                    'percentage': copy_base_percentage,
                    'amount': copy_base_amount,
                    'author_id': admin
                }
                Role.objects.create(**data_to_create)

            if not Role.objects.filter(name='Ментор', author_id=admin):
                copy_base_instance = Role.objects.filter(name='Ментор').first()
                copy_base_name = copy_base_instance.name
                copy_base_description = copy_base_instance.description
                copy_base_color = copy_base_instance.color
                copy_base_percentage = copy_base_instance.percentage
                copy_base_amount = copy_base_instance.amount
                data_to_create = {
                    'name': copy_base_name,
                    'description': copy_base_description,
                    'color': copy_base_color,
                    'percentage': copy_base_percentage,
                    'amount': copy_base_amount,
                    'author_id': admin
                }
                Role.objects.create(**data_to_create)

            if not Role.objects.filter(name='Подсобный', author_id=admin):
                copy_base_instance = Role.objects.filter(name='Подсобный').first()
                copy_base_name = copy_base_instance.name
                copy_base_description = copy_base_instance.description
                copy_base_color = copy_base_instance.color
                copy_base_percentage = copy_base_instance.percentage
                copy_base_amount = copy_base_instance.amount
                data_to_create = {
                    'name': copy_base_name,
                    'description': copy_base_description,
                    'color': copy_base_color,
                    'percentage': copy_base_percentage,
                    'amount': copy_base_amount,
                    'author_id': admin
                }
                Role.objects.create(**data_to_create)

            if not Role.objects.filter(name='Ученик', author_id=admin):
                copy_base_instance = Role.objects.filter(name='Ученик').first()
                copy_base_name = copy_base_instance.name
                copy_base_description = copy_base_instance.description
                copy_base_color = copy_base_instance.color
                copy_base_percentage = copy_base_instance.percentage
                copy_base_amount = copy_base_instance.amount
                data_to_create = {
                    'name': copy_base_name,
                    'description': copy_base_description,
                    'color': copy_base_color,
                    'percentage': copy_base_percentage,
                    'amount': copy_base_amount,
                    'author_id': admin
                }
                Role.objects.create(**data_to_create)

            if not Role.objects.filter(name='Журнал учета', author_id=admin):
                copy_base_instance = Role.objects.filter(name='Журнал учета').first()
                copy_base_name = copy_base_instance.name
                copy_base_description = copy_base_instance.description
                copy_base_color = copy_base_instance.color
                copy_base_percentage = copy_base_instance.percentage
                copy_base_amount = copy_base_instance.amount
                data_to_create = {
                    'name': copy_base_name,
                    'description': copy_base_description,
                    'color': copy_base_color,
                    'percentage': copy_base_percentage,
                    'amount': copy_base_amount,
                    'author_id': admin
                }
                Role.objects.create(**data_to_create)

            if not Role.objects.filter(name='Аммортизация инструмента', author_id=admin):
                copy_base_instance = Role.objects.filter(name='Аммортизация инструмента').first()
                copy_base_name = copy_base_instance.name
                copy_base_description = copy_base_instance.description
                copy_base_color = copy_base_instance.color
                copy_base_percentage = copy_base_instance.percentage
                copy_base_amount = copy_base_instance.amount
                data_to_create = {
                    'name': copy_base_name,
                    'description': copy_base_description,
                    'color': copy_base_color,
                    'percentage': copy_base_percentage,
                    'amount': copy_base_amount,
                    'author_id': admin
                }
                Role.objects.create(**data_to_create)

            if not Role.objects.filter(name='Испытательный срок', author_id=admin):
                copy_base_instance = Role.objects.filter(name='Испытательный срок').first()
                copy_base_name = copy_base_instance.name
                copy_base_description = copy_base_instance.description
                copy_base_color = copy_base_instance.color
                copy_base_percentage = copy_base_instance.percentage
                copy_base_amount = copy_base_instance.amount
                data_to_create = {
                    'name': copy_base_name,
                    'description': copy_base_description,
                    'color': copy_base_color,
                    'percentage': copy_base_percentage,
                    'amount': copy_base_amount,
                    'author_id': admin
                }
                Role.objects.create(**data_to_create)

        if update_fields == {'authority'} and admin.authority == 0:
            if Role.objects.filter(name='Мастер', author_id=admin):
                Role.objects.filter(name='Мастер', author_id=admin).delete()
            if Role.objects.filter(name='Ментор', author_id=admin):
                Role.objects.filter(name='Ментор', author_id=admin).delete()
            if Role.objects.filter(name='Подсобный', author_id=admin):
                Role.objects.filter(name='Подсобный', author_id=admin).delete()
            if Role.objects.filter(name='Ученик', author_id=admin):
                Role.objects.filter(name='Ученик', author_id=admin).delete()
            if Role.objects.filter(name='Журнал учета', author_id=admin):
                Role.objects.filter(name='Журнал учета', author_id=admin).delete()
            if Role.objects.filter(name='Аммортизация инструмента', author_id=admin):
                Role.objects.filter(name='Аммортизация инструмента', author_id=admin).delete()
            if Role.objects.filter(name='Испытательный срок', author_id=admin):
                Role.objects.filter(name='Испытательный срок', author_id=admin).delete()

    def __str__(self):
        return f"Роль {self.id}: {self.name}"


# post_init.connect(Role.create_base_roles, sender=User)


class ProjectEmployee(models.Model):
    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"

    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    user_id = models.ForeignKey(to=User, verbose_name="ID Пользователя", on_delete=models.CASCADE)
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
    def write_rate_to_history_model(sender, instance, created, update_fields, **kwargs):
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
    def write_advance_to_history_model(sender, instance, created, update_fields, **kwargs):
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
    initiator = models.ForeignKey(to=User, verbose_name="ID Инициатора", unique=False, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(to=ProjectEmployee, verbose_name="ID Рабочего", on_delete=models.CASCADE)
    # project_id = models.ForeignKey(to=Project, verbose_name="ID Проекта", on_delete=models.CASCADE, default=0)
    date = models.DateField(verbose_name="Дата", unique=False, null=False,
                            blank=False)
    work_time = models.FloatField(verbose_name="Выданное рабочее время", unique=False, null=False, blank=False)

    @staticmethod
    def calculate_project_work_time(sender, instance, created, update_fields, **kwargs):
        if created or update_fields == {'work_time'}:
            project = instance.employee_id.project_id
            project.work_time += instance.work_time

    def __str__(self):
        return f"Рабочее время {self.id} работника {self.employee_id.id}"

post_save.connect(TimeEntry.calculate_project_work_time, sender=TimeEntry)

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
    employee_id = models.ForeignKey(to=ProjectEmployee, verbose_name="ID Рабочего", on_delete=models.CASCADE)
    transaction_date = models.DateField(verbose_name="Дата транзакции", blank=False, null=False)
    type_accrual = models.CharField(verbose_name="Тип начисления", choices=TRANSACTIONSTYPES, max_length=255)
    amount = models.FloatField(verbose_name="Размер начисления", null=False, blank=False, unique=False)

    def __str__(self):
        return f"Начисление {self.id} работнику {self.employee_id.id}"


class Salary_employee(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    employee_id = models.ForeignKey(to=ProjectEmployee, verbose_name="ID Рабочего", on_delete=models.CASCADE)
    salary = models.FloatField(verbose_name="З/П рабочего", unique=False, null=True, blank=True, default=0)

    @staticmethod
    def calculate_salary(sender, instance, **kwargs):
        # роль - объект модели Role
        role = instance.employee_id.role_id

        hours_emp = TimeEntry.objects.filter(employee_id=instance.employee_id).aggregate(sum_hours=Sum('work_time'))

        # сумма рабочих часов этого работника числом
        hours_employee = hours_emp['sum_hours']

        # проект - объект модели Project
        project = instance.employee_id.project_id

        hours_all_emp = TimeEntry.objects.filter(project_id=project).aggregate(sum_all_hours=Sum('work_time'))

        # сумма рабочих часов всех работников на проекте числом
        hours_employees = hours_all_emp['sum_all_hours']

        master_role = Role.objects.get(name='Мастер')
        masters = ProjectEmployee.objects.filter(role=master_role)

        hours_all_masters = TimeEntry.objects.filter(project_id=project, employee_id__in=masters).aggregate(
            sum_all_hours=Sum('work_time'))

        # сумма рабочих часов всех мастеров на проекте числом
        hours_masters = hours_all_masters['sum_all_hours']

        mentor_role = Role.objects.get(name='Ментор')
        mentors = ProjectEmployee.objects.filter(role=mentor_role)

        hours_all_mentors = TimeEntry.objects.filter(project_id=project, employee_id__in=mentors).aggregate(
            sum_all_hours=Sum('work_time'))

        # сумма рабочих часов всех менторов на проекте числом
        hours_mentors = hours_all_mentors['sum_all_hours']

        assist_role = Role.objects.get(name='Подсобный')
        assists = ProjectEmployee.objects.filter(role=assist_role)

        hours_all_assists = TimeEntry.objects.filter(project_id=project, employee_id__in=assists).aggregate(
            sum_all_hours=Sum('work_time'))

        # сумма рабочих часов всех ассистентов на проекте числом
        hours_assists = hours_all_assists['sum_all_hours']

        intern_role = Role.objects.get(name='Испытательный срок')
        interns = ProjectEmployee.objects.filter(role=intern_role)

        hours_all_interns = TimeEntry.objects.filter(project_id=project, employee_id__in=interns).aggregate(
            sum_all_hours=Sum('work_time'))

        # сумма рабочих часов всех интернов на проекте числом
        hours_interns = hours_all_interns['sum_all_hours']

        pupil_role = Role.objects.get(name='Ученик')
        pupils = ProjectEmployee.objects.filter(role=pupil_role)

        hours_all_pupils = TimeEntry.objects.filter(project_id=project, employee_id__in=pupils).aggregate(
            sum_all_hours=Sum('work_time'))

        # сумма рабочих часов всех учеников на проекте числом
        hours_pupils = hours_all_pupils['sum_all_hours']

        # количество работников с данной ролью на проекте числом
        count_employees_with_this_role = ProjectEmployee.objects.filter(project_id=project, role_id=role).count()

        interns_income = Transactions.objects.filter(employee_id__in=interns).aggregate(
            sum_interns_amounts=Sum('amount'))

        # сумма заработков всех интернов на проекте числом
        sum_interns_income = interns_income['sum_interns_amounts']

        sum_addit_income = Transactions.objects.filter(employee_id=instance.employee_id,
                                                       type_accrual__in=['REPAIR', 'AMORT', 'TIME']).aggregate(
            additional_income=Sum('amount'))

        # сумма доп. заработка работника числом
        sum_additional_income = sum_addit_income['additional_income']

        # бюджет проекта числом
        budget_project = project.budget

        # Промежуточная стоимость часа работы
        cost_hour = (budget_project - sum_additional_income) / hours_employees

        # у испытуемого зп не считается, она выдаётся статично
        if role.name != 'Испытательный срок':
            first_part = (
                                 cost_hour + 0.2 * cost_hour * hours_assists + cost_hour * hours_interns - sum_interns_income) / (
                                 hours_masters + hours_mentors)

            second_part = (cost_hour * 0.4 * hours_pupils) / (hours_masters + 1.1 * hours_mentors)

            instance.salary = hours_employee * (first_part + second_part)


# post_save.connect(Salary_employee.calculate_salary, sender=Salary_employee)


class Employee_Statistics(models.Model):
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

    @staticmethod
    def calculate_statistics_data(sender, instance, **kwargs):

        sum_amount_no_advance_transactions = Transactions.objects.filter(employee_id=instance.employee_id,
                                                                         transaction_date__gte=instance.start_date,
                                                                         transaction_date__lte=instance.end_date).exclude(
            type_accrual='ADV').aggregate(sum_no_adv=Sum('amount'))

        amount = sum_amount_no_advance_transactions['sum_no_adv']

        if amount is None:
            amount = 0

        instance.income = amount

        sum_work_time = TimeEntry.objects.filter(employee_id=instance.employee_id, date__gte=instance.start_date,
                                                 date__lte=instance.end_date).aggregate(amount_sum=Sum('work_time'))
        if sum_work_time is None:
            sum_work_time = 0

        instance.work_time = sum_work_time

        last_rate = HistoryRate.objects.filter(employee_id=instance.employee_id).last().rate

        if last_rate is None:
            last_rate = 0

        instance.rate = last_rate

    def __str__(self):
        return f"Статистика {self.id} работника {self.employee_id.id}"


# post_save.connect(Employee_Statistics.calculate_statistics_data, sender=Employee_Statistics)


class Project_Statistics(models.Model):
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

    @staticmethod
    def calculate_statistics_data(sender, instance, **kwargs):
        # Список всех id employees в проекте
        all_emp_in_this_prj = ProjectEmployee.objects.filter(project_id=instance.project_id)

        sum_amount_no_adv = Transactions.objects.filter(employee_id__in=all_emp_in_this_prj,
                                                        date__gte=instance.start_date,
                                                        date__lte=instance.end_date).exclude(
            type_accrual='ADV').aggregate(sum_inc=Sum('amount'))

        amount = sum_amount_no_adv['sum_inc']

        if amount is None:
            amount = 0
        instance.income = amount

    def __str__(self):
        return f"Статистика {self.id} проекта {self.project_id.id}"


# post_save.connect(Project_Statistics.calculate_statistics_data, sender=Project_Statistics)


class Advance_Statistics(models.Model):
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

    @staticmethod
    def calculate_statistics_data(sender, instance, **kwargs):
        sum_amount_advance_transactions = Transactions.objects.filter(employee_id=instance.employee_id,
                                                                      transaction_date__gte=instance.start_date,
                                                                      transaction_date__lte=instance.end_date,
                                                                      type_accrual='ADV').aggregate(
            sum_adv=Sum('amount'))

        amount = sum_amount_advance_transactions['sum_adv']

        if amount is None:
            amount = 0

        instance.advance = amount

    def __str__(self):
        return f"Статистика авансов {self.id} работника {self.employee_id.id}"


# post_save.connect(Advance_Statistics.calculate_statistics_data, sender=Advance_Statistics)


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
