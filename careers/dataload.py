from datetime import date

from careers import data
from careers.models import Company, Speciality, Vacancy


def load_data():
    for title in data.companies:
        Company.objects.create(name=title['title'])

    for unit in data.specialties:
        Speciality.objects.create(code=unit['code'], title=unit['title'])

    for unit in data.jobs:
        unit_posted = unit['posted'].split('-')
        speciality = Speciality.objects.get(code=unit['cat'])
        company = Company.objects.get(name=unit['company'])
        Vacancy.objects.create(title=unit['title'], speciality=speciality,
                               company=company, salary_min=unit['salary_from'],
                               salary_max=unit['salary_to'],
                               published_at=date(int(unit_posted[0]),
                                                 int(unit_posted[1]),
                                                 int(unit_posted[2])),
                               description=unit['desc'])


if __name__ == '__main__':
    load_data()
