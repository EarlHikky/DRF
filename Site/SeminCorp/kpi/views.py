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
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import *
from .models import *
from .permissions import IsAdminOrReadOnly
from .serializers import SalesSerializer
from .utils import *
from pytils.translit import slugify
from rest_framework import generics, viewsets


# class SalesAPIView(generics.ListCreateAPIView):
#     queryset = Sales.objects.all()
#     serializer_class = SalesSerializer

# class SalesAPIView(APIView):
#     def get(self, request):
#         # lst = Sales.objects.all().values()
#         s = Sales.objects.all()
#         return Response({'posts': SalesSerializer(s, many=True).data})
#         # return Response({"sales": list(lst)})
#
#     def post(self, request):
#         # serializer = SalesSerializer(data=request.data)
#         # serializer.is_valid(raise_exception=True)
#
#         post_new = Sales.objects.create(
#             fio=request.data['fio'],
#             extradition=request.data['extradition'],
#             ti=request.data['ti'],
#             kis=request.data['kis'],
#             trener=request.data['trener'],
#             client=request.data['client']
#         )
#
#         return Response({'post': SalesSerializer(post_new).data})

# class SalesAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Sales.objects.all()
#     serializer_class = SalesSerializer

class SalesAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10000

class SalesViewSet(viewsets.ModelViewSet):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = SalesAPIListPagination

    # def get_queryset(self):
    #     pk = self.kwargs.get("pk")
    #     if not pk:
    #         return Sales.objects.all()[:3]
    #         return Sales.objects.filter(pk=pk)

    @action(methods=['get'], detail=False)
    def staff(self, request):
        staff = Staff.objects.all()
        return Response({'staff': [s.name for s in staff]})


# @action(methods=['get'], detail=True)
# def staff(self, request, pk=None):
#         staff = Staff.objects.get(pk=pk)
#         return Response({'staff': staff.name})

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
