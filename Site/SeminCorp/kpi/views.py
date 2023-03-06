import datetime
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import *
from .models import *
from .serializers import SalesSerializer
from .utils import *
from pytils.translit import slugify
from rest_framework import generics


# class SalesAPIView(generics.ListAPIView):
#     queryset = Sales.objects.all()
#     serializer_class = SalesSerializer

class SalesAPIView(APIView):
    def get(self, request):
        lst = Sales.objects.all().values()
        return Response({"sales": list(lst)})

    def post(self, request):
        post_new = Sales.objects.create(
            fio=request.data['fio'],
            extradition=request.data['extradition'],
            ti=request.data['ti'],
            kis=request.data['kis'],
            trener=request.data['trener'],
            client=request.data['client']
        )

        return Response({'post': model_to_dict(post_new)})




class SalesHome(DataMixin, ListView):
    model = Sales
    template_name = 'kpi/home.html'
    context_object_name = 'sales'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Semin corp'
        return context

    def get_queryset(self):
        return Sales.objects.all()
        # return Sales.objects.filter(time_create__month=1).select_related('fio')


class SalesView(DataMixin, ListView):
    paginate_by = 10
    model = Sales
    template_name = 'kpi/sales.html'
    context_object_name = 'sales'

    def get_context_data(self, *, object_list=None, **kwargs):
        # sale = get_object_or_404(Sales, slug=staff_slug)
        # context = {'staff': sale}
        context = super().get_context_data(**kwargs)
        # c_def = self.get_user_context(title='Продажи')
        context['title'] = 'Продажи'
        if not self.request.user.is_authenticated:
            context['menu'] = []
        else:
            context['menu'] = [{'title': "Добавить продажу", 'url_name': 'add_sale'}]
        return context


class AddSale(LoginRequiredMixin, CreateView):
    form_class = AddSaleForm
    template_name = 'kpi/add_sale.html'
    success_url = reverse_lazy('sales')
    # login_url = reverse_lazy('home')
    login_url = '/admin/'

    # raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить сотрудника'
        return context


class StaffView(DataMixin, ListView):
    model = Staff
    template_name = 'kpi/staff.html'
    context_object_name = 'staff'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # c_def = self.get_user_context(title='Продажи')
        context['title'] = 'Сотрудники'
        if not self.request.user.is_authenticated:
            context['menu'] = []
        else:
            context['menu'] = [{'title': "Добавить сотрудника", 'url_name': 'add_staff'}]
        return context


class AddStaff(DataMixin, CreateView):
    model = Staff
    form_class = AddStaffForm
    template_name = 'kpi/add_staff.html'
    success_url = reverse_lazy('staff')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавить сотрудника')
        # context['slug'] = slugify(kwargs['name'])
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.save()
        # login(self.request, user)
        return redirect('staff')


def s(request, sale_id):
    sales = get_list_or_404(Sales, fio_id=sale_id)
    context = {'sales': sales}
    return render(request, 'kpi/sale.html', context=context)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'kpi/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    # form_class = AuthenticationForm
    form_class = LoginUserForm
    template_name = 'kpi/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
