# from datetime import date

from django.contrib.auth.models import User
from django.db import models

# from careers import data
from stepik_careers.settings import MEDIA_SPECIALITY_IMAGE_DIR, MEDIA_COMPANY_IMAGE_DIR


class Company(models.Model):
    name = models.CharField(max_length=30,
                            unique=False,
                            default='')
    location = models.CharField(max_length=20,
                                default='')
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR,
                             blank=True)
    description = models.TextField(default='')
    employee_count = models.IntegerField(null=True,
                                         default=0)
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              null=True, default='')


class Speciality(models.Model):
    code = models.CharField(max_length=15,
                            unique=False,
                            default='')
    title = models.CharField(max_length=25,
                             default='')
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR)

    def __str__(self):
        return '%s' % self.title


class Vacancy(models.Model):
    title = models.CharField(max_length=30)
    speciality = models.ForeignKey(Speciality,
                                   related_name='vacancies',
                                   on_delete=models.CASCADE,
                                   unique=False)
    company = models.ForeignKey(Company,
                                related_name='vacancies',
                                on_delete=models.CASCADE,
                                unique=False)
    skills = models.CharField(max_length=100)
    description = models.TextField()
    salary_min = models.FloatField()
    salary_max = models.FloatField()
    published_at = models.DateField()


class Application(models.Model):
    written_username = models.CharField(max_length=30)
    written_phone = models.CharField(max_length=30)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy,
                                on_delete=models.CASCADE,
                                related_name='applications')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='applications')


class Resume(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=30)
    NOT_LOOKING = 'NL'
    CONSIDERING_OFFERS = 'CO'
    LOOKING_FOR = 'LF'
    STATUS_CHOICES = (
        (NOT_LOOKING, 'Не ищу работу'),
        (CONSIDERING_OFFERS, 'Рассматриваю предложения'),
        (LOOKING_FOR, 'Ищу работу')
    )
    status = models.CharField(max_length=2,
                              choices=STATUS_CHOICES,
                              default=NOT_LOOKING)

    salary = models.FloatField()
    speciality = models.ForeignKey(Speciality,
                                   on_delete=models.CASCADE,
                                   unique=False)
    INTERN = 'IN'
    JUNIOR = 'JN'
    MIDDLE = 'MD'
    SENIOR = 'SN'
    LEAD = 'LD'
    GRADE_CHOICES = (
        (INTERN, 'Стажер'),
        (JUNIOR, 'Джуниор'),
        (MIDDLE, 'Миддл'),
        (SENIOR, 'Сеньор'),
        (LEAD, 'Лид')
    )
    grade = models.CharField(max_length=2,
                             choices=GRADE_CHOICES,
                             default=INTERN)
    education = models.CharField(max_length=20)
    experience = models.CharField(max_length=20)
    portfolio = models.TextField()

#
# for title in data.companies:
#     Company.objects.create(name=title['title'])
#
# for unit in data.specialties:
#     Speciality.objects.create(code=unit['code'], title=unit['title'])
#
# for unit in data.jobs:
#     unit_posted = unit['posted'].split('-')
#     speciality = Speciality.objects.get(code=unit['cat'])
#     company = Company.objects.get(name=unit['company'])
#     Vacancy.objects.create(title=unit['title'], speciality=speciality,
#                            company=company, salary_min=unit['salary_from'],
#                            salary_max=unit['salary_to'],
#                            published_at=date(int(unit_posted[0]),
#                                              int(unit_posted[1]),
#                                              int(unit_posted[2])),
#                            description=unit['desc'])
