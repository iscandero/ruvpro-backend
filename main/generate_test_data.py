import random

from django.db.models import Sum, Count

from main.models import SocialNetworks, AppUser, Project, Role, ProjectEmployee, TimeEntry
from main.services.team.selectors import get_team_by_owner
from main.services.time_entry.selectors import get_time_entry_by_date_and_worker
from main.services.user.selectors import is_exist_user_phone, get_app_user_by_phone, get_app_user_by_email
from main.services.work_with_date import convert_timestamp_to_date

DOMAIN_EMAIL_LIST = ['@ruvim.pro', '@incetro.com', '@ruv.pro', '@ya.ru', '@green.ru', '@icloud.com']
INSTAGRAM_BASE = 'https://www.instagram.com/'
VK_BASE = 'https://vk.com/'
TWITTER_BASE = 'https://twitter.com/'
YOUTUBE_BASE = 'https://www.youtube.com/c/'
FACEBOOK_BASE = 'https://www.facebook.com/'
TELEGRAM_BASE = 'https://t.me/'


def get_sum_salarys_by_project(project: Project):
    salary_aggregate = ProjectEmployee.objects.filter(project=project).aggregate(sum_salary=Sum('salary'))
    return salary_aggregate['sum_salary'] if salary_aggregate['sum_salary'] is not None else 0


def create_test_user_if_need(name: str, phone: str, path_to_avatar: str, bio: str, authority: int):
    if not is_exist_user_phone(phone=phone):
        name_for_email_and_social = name.replace(' ', '').lower()
        email = name_for_email_and_social + random.choice(DOMAIN_EMAIL_LIST)

        socials = {"Instagram": INSTAGRAM_BASE + name_for_email_and_social + '/',
                   "VK": VK_BASE + name_for_email_and_social,
                   "Twitter": TWITTER_BASE + name_for_email_and_social,
                   "YouTube": YOUTUBE_BASE + name_for_email_and_social,
                   "Facebook": FACEBOOK_BASE + name_for_email_and_social,
                   "Telegram": TELEGRAM_BASE + name_for_email_and_social,
                   }

        user = AppUser.objects.create(name=name, email=email, phone=phone, avatar=path_to_avatar, bio=bio,
                                      authority=authority, currency='RUB', is_register=True)

        for social in socials:
            url = socials[social]
            user.socials.add(SocialNetworks.objects.create(name=social, url=url))

        return user

    else:
        return get_app_user_by_phone(phone=phone)


def add_user_by_team_owner(owner, user_to_add):
    team = get_team_by_owner(owner=owner)
    team.participants.add(user_to_add)


def create_test_users_and_owner_team():
    owner = create_test_user_if_need(
        name='William Strickland',
        phone='+79186857995',
        path_to_avatar='http://gorozhanin.space/media/users_files/11.jpg',
        bio="""Прораб с 20-летним стажем. Пунктуален, исполнителен, без вредных привычек.
Наличие личного автомобиля, права Категории A, B, C, D, E. 
Ведение работ на разных объектах, общее руководство объектами, общее руководство подразделением компании. 
Командировки возможны.""",
        authority=1
    )

    henry = create_test_user_if_need(
        name='Henry Pearson',
        phone='+79189990102',
        path_to_avatar='http://gorozhanin.space/media/users_files/2.jpg',
        bio="""Предлагаю свои услуги по разработке организационно-технологической и проектной документации.
А также полное сопровождение строительства на всех этапах работ.
Мой опыт и квалификация, позволяет выполнять поставленные задачи в кротчайшие сроки.
Проекты только с гарантией согласования заказчиком. Опыт работы в строительстве 7 лет.""",
        authority=0
    )

    add_user_by_team_owner(owner=owner, user_to_add=henry)

    edmund = create_test_user_if_need(
        name='Edmund Freeman',
        phone='+79185555999',
        path_to_avatar='http://gorozhanin.space/media/users_files/3.jpg',
        bio="""- внутренняя отделка помещений;
- работа с гипсокартоном любой сложности, возведение потолков, перегородок, коробов;
- монтаж багета, плинтуса;
- сборка ламинат, паркетной доски любой сложности;
- покраска стен, потолков;
- сантехника, электрика без подключения щита;
- установка окон;
- установка дверей без вырезки замков;
- установка выключателей, розеток;
- сборка и установка люстр;
- утепление крыш каменной ватой;
- сборка щитовой мебели;
- делаю внутреннюю теплоизоляцию.
Имею свой профессиональный инструмент. Делаю быстро, качественно и надёжно. Опыт работы более 30 лет""",
        authority=0
    )

    add_user_by_team_owner(owner=owner, user_to_add=edmund)

    andrew = create_test_user_if_need(
        name='Andrew Sidney',
        phone='+79189090777',
        path_to_avatar='http://gorozhanin.space/media/users_files/4.jpg',
        bio="""Фундамент, стройка, электропроводка.
Системы: отопления, котельных, водоснабжения, внутренней сантехники, канализации, дренажа.
Отделочные работы помещений, тепловые зазоры, утепления, кровли, благоустройства территории, дворовые строения,
ограждения, обслуживание дома, и многое другое.""",
        authority=0
    )

    add_user_by_team_owner(owner=owner, user_to_add=andrew)

    jim = create_test_user_if_need(
        name='Jim Lane',
        phone='+79180550015',
        path_to_avatar='http://gorozhanin.space/media/users_files/5.jpg',
        bio="""Произвожу врезку фурнитуры только по шаблону Солдатова.
Места петель замков будут без сколов и царапин. Работаю только профессиональным электроинструментом.
Вручную не врезаю (петли,замки).
Работаю чисто, с пылесосом.""",
        authority=0
    )

    add_user_by_team_owner(owner=owner, user_to_add=jim)

    nancy = create_test_user_if_need(
        name='Nancy Adamson',
        phone='+79182224455',
        path_to_avatar='http://gorozhanin.space/media/users_files/6.jpg',
        bio="""Алмазное Бурение/Алмазная Резка
Под силу любой материал:
Бетон, монолит (железобетон), кирпич, гранит, асфальт, камень.
Опытный специалист оперативно, качественно и в любое время выполнит для Вас:
-алмазное бурение (сверление) технологических отверстий для прокладки инженерных коммуникаций:
- отопления
- водоснабжения
- кондиционирования
- приточная вентиляция
- дымоудаления
- канализация
- газоснабжения
- электроснабжения
- устройство продухов(отдушин) в фундаменте;
- алмазная резка дверных и оконных проемов;
- расширение существующих проемов
- усиление(обрамление) проемов металлоконструкциями с выдачей документов;
- демонтаж стен и перекрытий методом алмазной резки и электро-перфораторами.
Сверление бетона так же возможно без крепления.
Диаметры сверления от 16 до 800мм""",
        authority=0
    )

    add_user_by_team_owner(owner=owner, user_to_add=nancy)

    edward = create_test_user_if_need(
        name='Edward Casey',
        phone='+79093444330',
        path_to_avatar='http://gorozhanin.space/media/users_files/7.jpg',
        bio="""✅ Сэкономлю вам деньги на переделках, время на контроле за рабочими, 
поездках по магазинам и объяснениях всем всего и вся! Помогу Вам определиться с выбором состава проекта, 
совместно выявим ваши предпочтения для достижения желаемого результата.
✅ Свои опытные ремонтно-строительная бригады для реализации проекта любой сложности, 
производство корпусной и мягкой мебели, скидки на отделочные материалы, светильники, элементы декора и т.д. 
Реализую ваш проект мечты под ключ, от эскиза до сдачи в пользование. Гарантийное обслуживание.""",
        authority=0
    )

    add_user_by_team_owner(owner=owner, user_to_add=edward)

    megan = create_test_user_if_need(
        name='Megan Gross',
        phone='+79005788755',
        path_to_avatar='http://gorozhanin.space/media/users_files/8.jpg',
        bio="""Все виды бетонных работ (стяжка, отмостка, фундамент),
а также монтаж забора из проф. настила, демонтаж и многое другое.
Работу выполняю быстро и качественно! По цене всегда можно договориться.
По всем вопросам обращаться по телефону а также покос травы спил деревьев, вывоз мусора и многое другое""",
        authority=0
    )

    add_user_by_team_owner(owner=owner, user_to_add=megan)

    jamie = create_test_user_if_need(
        name='Jamie Cole',
        phone='+79909557480',
        path_to_avatar='http://gorozhanin.space/media/users_files/9.jpg',
        bio="""Универсальный строитель! Выполняю любые ремонтно-строительные работы: электрика,сантехника.
Сварочные работы. Сборка и ремонт мебели,окон и дверей (пвх, al, дерево). Ремонт квартир, ванных комнат. 
Строительство домов, бань, саун! Я не посредник! Всё делаю качественно, своими руками! 
Опыт работы в сфере строительства более 10 лет! Гражданство РФ, качество. Порядочность гарантирую.""",
        authority=0
    )

    add_user_by_team_owner(owner=owner, user_to_add=jamie)

    leticia = create_test_user_if_need(
        name='Leticia Francis',
        phone='+79188944801',
        path_to_avatar='http://gorozhanin.space/media/users_files/10.jpg',
        bio="""Наружная и внутренняя отделка: помещений, балконов, лоджий, бань, домов, квартир.
Ремонт пластиковых окон, устранение продувов, регулировка.
Монтаж откосов, подоконников и любых конструкций ПВХ.
Пластиковые панели, МДФ, вагонка пластиковая и деревянная, блокхаус и другой материал.
Кирпичная кладка, облицовочный кирпич, газосиликат, мелкоштучный блок.
Жёстекая кровля.
Утепление и пароизоляция.
Демонтаж.""",
        authority=0
    )

    add_user_by_team_owner(owner=owner, user_to_add=leticia)


from main.const_data.base_roles import *


def generate_test_project(name: str, budget: float, owner: AppUser):
    currency = 'RUB'
    project = Project.objects.create(owner=owner, name=name, budget=budget, currency=currency, is_archived=False)

    master_role_for_project = MASTER_ROLE.copy()
    master_role_for_project['is_base'] = False
    master_role_for_project['project'] = project
    master_role_for_project['author'] = owner

    mentor_role_for_project = MENTOR_ROLE.copy()
    mentor_role_for_project['is_base'] = False
    mentor_role_for_project['project'] = project
    mentor_role_for_project['author'] = owner

    auxiliary_role_for_project = AUXILIARY_ROLE.copy()
    auxiliary_role_for_project['is_base'] = False
    auxiliary_role_for_project['project'] = project
    auxiliary_role_for_project['author'] = owner

    student_role_for_project = STUDENT_ROLE.copy()
    student_role_for_project['is_base'] = False
    student_role_for_project['project'] = project
    student_role_for_project['author'] = owner

    acc_journal_role_for_project = ACC_JOURNAL_ROLE.copy()
    acc_journal_role_for_project['is_base'] = False
    acc_journal_role_for_project['project'] = project
    acc_journal_role_for_project['author'] = owner

    amortization_role_for_project = AMORTIZATION_INST_ROLE.copy()
    amortization_role_for_project['is_base'] = False
    amortization_role_for_project['project'] = project
    amortization_role_for_project['author'] = owner

    intern_role_for_project = INTERN_ROLE.copy()
    intern_role_for_project['is_base'] = False
    intern_role_for_project['project'] = project
    intern_role_for_project['author'] = owner

    resp_role_for_project = RESPONSIBLE_ROLE.copy()
    resp_role_for_project['is_base'] = False
    resp_role_for_project['project'] = project
    resp_role_for_project['author'] = owner

    master = Role.objects.create(**master_role_for_project)
    mentor = Role.objects.create(**mentor_role_for_project)
    aux = Role.objects.create(**auxiliary_role_for_project)
    student = Role.objects.create(**student_role_for_project)
    acc = Role.objects.create(**acc_journal_role_for_project)
    amort = Role.objects.create(**amortization_role_for_project)
    intern = Role.objects.create(**intern_role_for_project)
    resp = Role.objects.create(**resp_role_for_project)

    project_roles_dict = {
        "master": master,
        "mentor": mentor,
        "aux": aux,
        "student": student,
        "acc": acc,
        "amort": amort,
        "intern": intern,
        "resp": resp
    }

    return project, project_roles_dict


def generate_random_work_time_by_worker(worker: ProjectEmployee, start_date, end_date):
    if worker.project.owner == worker.user:
        project_budget = worker.project.budget
        workers_count_dict = ProjectEmployee.objects.filter(project=worker.project).aggregate(count=Count('id'))
        workers_count = int(workers_count_dict['count'])
        worker_percent = worker.role.percentage if worker.role.percentage is not None else 100
        timestamp = start_date
        while timestamp <= end_date:
            if end_date - timestamp >= 157766400:
                """
                5 лет - шаг 60 дней
                """
                step = 5184000
            elif end_date - timestamp >= 31536000:
                """
                1 год - шаг 12 дней
                """
                step = 1036800

            elif end_date - timestamp >= 15638400:
                """
                полгода - шаг 6 дней
                """
                step = 518400
            elif end_date - timestamp >= 2592000:
                """
                месяц - шаг 2 или 3 дня
                """
                steps_list = [172800, 259200]
                step = random.choice(steps_list)

            else:
                """
                неделя - 1 день
                """
                step = 86400

            date = convert_timestamp_to_date(timestamp)
            random_hours = random.randint(2, 10)
            # if (get_sum_salarys_by_project(
            #         project=worker.project) + worker_percent * random_hours) < project_budget * workers_count:
            # time_entry_on_this_date = get_time_entry_by_date_and_worker(date=date, worker=worker)
            # if time_entry_on_this_date:
            #     pass
            # else:
            TimeEntry.objects.create(employee=worker, date=date, work_time=random_hours)
            timestamp += step


def create_test_projects(owner: AppUser):
    henry = get_app_user_by_email('henrypearson@ruvim.pro')
    edmund = get_app_user_by_email('edmundfreeman@incetro.com')
    andrew = get_app_user_by_email('andrewsidney@ruvim.pro')
    jim = get_app_user_by_email('jimlane@incetro.com')
    nancy = get_app_user_by_email('nancyadamson@ruvim.pro')
    edward = get_app_user_by_email('edwardcasey@incetro.com')
    megan = get_app_user_by_email('megangross@icloud.com')
    jamie = get_app_user_by_email('jamiecole@ruvim.pro')
    leticia = get_app_user_by_email('leticiafrancis@ruv.pro')

    project, roles_dict = generate_test_project(name='Пушкина 22/2', budget=1000000, owner=owner)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=owner, project=project, role=roles_dict['master']), 1621694443, 1660322597)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=edmund, project=project, role=roles_dict['aux']), 1621694443, 1660322597)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=nancy, project=project, role=roles_dict['student']), 1621694443, 1660322597)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=edward, project=project, role=roles_dict['mentor']), 1621694443, 1660322597)

    project, roles_dict = generate_test_project(name='ЖК Тургенев', budget=3000000, owner=owner)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=owner, project=project, role=roles_dict['aux']), 1621694443, 1660322597)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=andrew, project=project, role=roles_dict['master']), 1621694443, 1660322597)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=nancy, project=project, role=roles_dict['student']), 1621694443, 1660322597)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=megan, project=project, role=roles_dict['student']), 1621694443, 1660322597)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=jamie, project=project, role=roles_dict['master']), 1621694443, 1660322597)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=leticia, project=project, role=roles_dict['mentor']), 1621694443,
        1660322597)

    project, roles_dict = generate_test_project(name='Ворошиловский проспект 11', budget=2500000, owner=owner)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=owner, project=project, role=roles_dict['master']), 1621694443, 1660322597)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=henry, project=project, role=roles_dict['master']), 1621694443, 1660322597)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=jim, project=project, role=roles_dict['aux']), 1621694443, 1660322597)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=edmund, project=project, role=roles_dict['aux']), 1621694443, 1660322597)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=nancy, project=project, role=roles_dict['student']), 1621694443, 1660322597)

    project, roles_dict = generate_test_project(name='Пролетарская 93', budget=2880000, owner=owner)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=owner, project=project, role=roles_dict['mentor']), 1621694443, 1660322597)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=megan, project=project, role=roles_dict['student']), 1621694443, 1660322597)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=edmund, project=project, role=roles_dict['intern']), 1621694443, 1660322597)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=leticia, project=project, role=roles_dict['aux']), 1621694443, 1660322597)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=nancy, project=project, role=roles_dict['student']), 1621694443, 1660322597)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=jamie, project=project, role=roles_dict['master']), 1621694443, 1660322597)

    project, roles_dict = generate_test_project(name='Базовская 156/5', budget=1700000, owner=owner)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=owner, project=project, role=roles_dict['master']), 1621694443, 1660322597)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=edmund, project=project, role=roles_dict['aux']), 1621694443, 1660322597)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=jim, project=project, role=roles_dict['aux']), 1621694443, 1660322597)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=megan, project=project, role=roles_dict['master']), 1621694443, 1660322597)

    project, roles_dict = generate_test_project(name='ЖК Восточный кв.17', budget=900000, owner=owner)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=owner, project=project, role=roles_dict['master']), 1621694443, 1660322597)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=jim, project=project, role=roles_dict['master']), 1621694443, 1660322597)
    generate_random_work_time_by_worker(
        ProjectEmployee.objects.create(user=megan, project=project, role=roles_dict['aux']), 1621694443, 1660322597)
