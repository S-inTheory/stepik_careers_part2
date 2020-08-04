from datetime import datetime

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import CreateView, UpdateView

from careers.forms import ApplicationForm, CompanyForm, ResumeForm, VacancyForm
from careers.models import Company, Resume, Speciality, Vacancy


class MainView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):

        return render(request, r'careers/index.html',
                      {'companies': Company.objects.all(),
                       'specialities': Speciality.objects.all(),
                       })


class SearchView(View):

    def get(self, request, *args, **kwargs):
        query = request.GET.get('s', '')
        results = Vacancy.objects.filter(Q(title__icontains=query)
                                         | Q(description__icontains=query))
        count = results.count()
        return render(request, 'careers/search.html', {'results': results,
                                                       'query': query,
                                                       'count': count})


class VacanciesView(View):
    template_name = 'vacancies.html'

    def get(self, request, *args, **kwargs):
        return render(request, r'careers/vacancies.html',
                      {'vacancies': Vacancy.objects.all(),
                       'title': 'Все вакансии',
                       'count': Vacancy.objects.all().count()
                       }, )


class VacanciesCatView(View):
    template_name = 'vacancies.html'

    def get(self, request, category: str, *args, **kwargs):
        cat = Speciality.objects.all().filter(code=category)
        return render(request, r'careers\vacancies.html',
                      {'vacancies': Vacancy.objects.all().filter(speciality=cat[0].id),
                       'title': cat[0].title,
                       'count': Vacancy.objects.all().filter(speciality=cat[0].id).count(),
                       })


class VacancyView(View):
    template_name = 'vacancy.html'

    def get(self, request, id: int, *args, **kwargs):
        vac = Vacancy.objects.all().filter(id=id)
        comp = Company.objects.all().filter(id=vac.first().id)
        form = ApplicationForm()
        return render(request, r'careers/vacancy.html',
                      {'company': comp.first(),
                       'vacancy': vac.first(),
                       'form': form
                       })


class ApplicationView(View):
    form_class = ApplicationForm
    template_name = 'vacancy.html'

    def post(self, request, id: int):
        if request.method == 'POST':
            form = ApplicationForm(request.POST)
            vac = Vacancy.objects.all().filter(id=id)
            if form.is_valid():
                application = form.save(commit=False)
                application.user = request.user
                application.vacancy = Vacancy.objects.get(title=vac[0].title)
                application.save()
                return render(request, 'careers/sent.html', {'vacancy': vac[0]})


class CompanyView(View):
    template_name = 'company.html'

    def get(self, request, id: int, *args, **kwargs):
        comp = Company.objects.all().filter(id=id)
        if comp:
            return render(request, r'careers/company.html',
                          {'company': comp[0],
                           'vacancies':
                               Vacancy.objects.all().filter(company=comp[0].id),
                           'count':
                               Vacancy.objects.all().filter(company=comp[0].id).count(),
                           })
        else:
            return HttpResponseNotFound('Такой страницы не существует')


class MyCompanyView(UpdateView):
    form_class = CompanyForm
    template_name = 'company-edit.html'

    def get(self, request, *args, **kwargs):
        try:
            comp = Company.objects.get(owner=self.request.user.id)
            form = CompanyForm(instance=comp)
            return render(request, 'careers/company-edit.html',
                          {'form': form,
                           'company': comp,
                           })
        except Company.DoesNotExist:
            Company.objects.create(name='My Company', location='N', logo='', description='Default Description',
                                   employee_count=1, owner=request.user)
            return render(request, 'careers/company-create.html')

    def post(self, request, *args, **kwargs):
        comp = get_object_or_404(Company, owner_id=request.user.id)
        if request.method == 'POST':
            form = CompanyForm(request.POST, instance=comp)
            if form.is_valid():
                company = form.save(commit=False)
                company.owner = request.user
                company.save()
        return render(request, 'careers/company-edit.html', {'form': form})


class MyRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'careers/register.html'
    success_url = 'login'


class MyLoginView(LoginView):
    redirect_authenticated_user = True

    template_name = 'careers/login.html'


class MyVacanciesView(View):
    template_name = 'vacancy-list.html'

    def get(self, request, *args, **kwargs):
        comp = Company.objects.get(owner=self.request.user.id)
        vacancies = Vacancy.objects.all().filter(company_id=Company.objects.get(owner_id=self.request.user.id))

        return render(request, 'careers/vacancy-list.html', {'company': comp,
                                                             'vacancies': vacancies})


class MyVacancyView(UpdateView):
    template_name = 'vacancy-edit.html'
    form_class = VacancyForm

    def get(self, request, id, *args, **kwargs):
        if id != 0:
            comp = Company.objects.get(owner=self.request.user.id)
            vacancy = get_object_or_404(Vacancy, id=id)
            form = VacancyForm(instance=vacancy)
            return render(request, 'careers/vacancy-edit.html',
                          {'form': form,
                           'company': comp
                           })
        elif id == 0:
            comp = Company.objects.get(owner=self.request.user.id)
            vacancy = Vacancy.objects.create(title='новая вакансия',
                                             speciality=Speciality.objects.get(title='Фронтенд'),
                                             company=Company.objects.get(id=comp.id), description='',
                                             salary_min=0.0,
                                             salary_max=0.0,
                                             published_at=datetime.today())
            form = VacancyForm(instance=vacancy)
            return render(request, 'careers/vacancy-edit.html',
                          {'form': form,
                           'company': comp
                           })

    def post(self, request, id, *args, **kwargs):
        vacancy = get_object_or_404(Vacancy, id=id)
        if request.method == 'POST':
            form = VacancyForm(request.POST, instance=vacancy)
            if form.is_valid():
                vac = form.save(commit=False)
                vac.company_id = Company.objects.get(owner_id=self.request.user.id)
                vac.save()
        return render(request, 'careers/vacancy-edit.html', {'form': form,
                                                             'vacancy': vacancy})


class ResumeView(UpdateView):
    form_class = ResumeForm
    template_name = 'resume-edit.html'

    def get(self, request, *args, **kwargs):
        resume = Resume.objects.all().first()
        if resume:
            form = ResumeForm(instance=resume)
            return render(request, 'careers/resume-edit.html',
                          {'form': form})
        else:
            Resume.objects.create(user=request.user, name='', surname='', salary=0.0,
                                  speciality=Speciality.objects.get(title='Фронтенд'),
                                  education='',
                                  experience='',
                                  portfolio='')
        return render(request, 'careers/resume-create.html')

    def post(self, request, *args, **kwargs):
        resume = get_object_or_404(Resume, user=request.user.id)
        if request.method == 'POST':
            form = ResumeForm(request.POST, instance=resume)
            if form.is_valid():
                resume_edit = form.save(commit=False)
                resume_edit.user = request.user
                resume_edit.save()
                return render(request, 'careers/resume-edit.html', {'form': form})


def custom_handler404(request, exception):
    return HttpResponseNotFound('Такой страницы не существует')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера')
