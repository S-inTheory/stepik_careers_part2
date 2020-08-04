from django import forms

from .models import Application, Company, Vacancy, Speciality, Resume


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        labels = {'written_username': 'Вас зовут',
                  'written_phone': 'Ваш телефон',
                  'written_cover_letter': 'Сопроводительное письмо'}
        fields = ('written_username', 'written_phone', 'written_cover_letter')


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        labels = {'name': 'Название компании',
                  'location': 'География',
                  'logo': 'Логотип',
                  'description': 'Информация о компании',
                  'employee_count': 'Количество человек в компании'}
        fields = ('name', 'location', 'logo', 'description', 'employee_count')


class VacancyForm(forms.ModelForm):
    speciality = forms.ModelChoiceField(queryset=Speciality.objects.all(),
                                        to_field_name='code',
                                        label='Специализация')

    class Meta:
        model = Vacancy
        labels = {'title': 'Название вакансии',
                  'skills': 'Требуемые навыки',
                  'description': 'Описание вакансии',
                  'salary_min': 'Зарплата от',
                  'salary_max': 'Зарплата до'}
        fields = ('title', 'speciality', 'skills', 'description',
                  'salary_min', 'salary_max')


class ResumeForm(forms.ModelForm):
    speciality = forms.ModelChoiceField(queryset=Speciality.objects.all(),
                                        to_field_name='code',
                                        label='Специализация')

    class Meta:
        model = Resume
        labels = {
            'name': 'Имя',
            'surname': 'Фамилия',
            'status': 'Готовность к работе',
            'salary': 'Ожидаемое вознаграждение',
            'grade': 'Квалификация',
            'education': 'Образование',
            'experience': 'Опыт работы',
            'portfolio': 'Ссылка на портфолио'
        }
        fields = ('name', 'surname', 'status', 'salary',
                  'speciality', 'grade', 'education',
                  'experience', 'portfolio')
