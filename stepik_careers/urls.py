from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from careers.views import MainView, VacanciesView, VacanciesCatView, CompanyView, VacancyView, MyRegisterView, \
    MyLoginView, ApplicationView, MyCompanyView, MyVacanciesView, MyVacancyView, SearchView, ResumeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='index'),
    path('vacancies', VacanciesView.as_view()),
    path('vacancies/cat/<str:category>/', VacanciesCatView.as_view()),
    path('companies/<int:id>/', CompanyView.as_view()),
    path('vacancies/<int:id>', VacancyView.as_view()),
    path('vacancies/<int:id>/send', ApplicationView.as_view()),
    path('mycompany', MyCompanyView.as_view()),
    path('search', SearchView.as_view()),
    path('myresume', ResumeView.as_view()),
    path('mycompany/vacancies', MyVacanciesView.as_view()),
    path('mycompany/vacancies/<int:id>', MyVacancyView.as_view()),
    path('login', MyLoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('signup', MyRegisterView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
