from django import forms

from .models import Application, Company, Vacancy, Speciality


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
    speciality = forms.ModelChoiceField(queryset=Speciality.objects.all(), to_field_name='code')

    class Meta:
        model = Vacancy
        labels = {'title': 'Название вакансии',
                  'speciality': 'Специализация',
                  'skills': 'Требуемые навыки',
                  'description': 'Описание вакансии',
                  'salary_min': 'Зарплата от',
                  'salary_max': 'Зарплата до'}
        fields = ('title', 'speciality', 'skills', 'description', 'salary_min', 'salary_max')
