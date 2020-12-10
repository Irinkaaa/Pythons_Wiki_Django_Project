from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, FormView

from pythons_core.decorators import group_required
from pythons_core.view_mixin import GroupRequiredMixin
from .forms import PythonCreateForm, FilterForm
from .models import Python


def extract_filter_values(params):
    order = params['order'] if 'order' in params else FilterForm.ORDER_ASC
    text = params['text'] if 'text' in params else ''
    return {
        'order': order,
        'text': text,
    }


# def index(req):
#     params = extract_filter_values(req.GET)
#     order_by = 'name' if params['order'] == FilterForm.ORDER_ASC else '-name'
#     pythons = Python.objects.filter(name__icontains=params['text']).order_by(order_by)
#     for python in pythons:
#         python.can_delete = python.created_by_id == req.user.id
#
#     context = {
#         'pythons': pythons,
#         'filter_form': FilterForm(initial=params)
#     }
#     return render(req, 'index.html', context)


class IndexView(ListView):
    template_name = 'index.html'
    model = Python
    context_object_name = 'pythons'
    order_by_asc = True

    def dispatch(self, request, *args, **kwargs):
        params = extract_filter_values(request.GET)
        self.order_by_asc = params['order'] == FilterForm.ORDER_ASC
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pythons'] = sorted(context['pythons'], key=lambda x: x.name, reverse=not self.order_by_asc)
        context['filter_form'] = FilterForm(initial={'order': self.order_by_asc})
        return context


def python_details(request, pk, slug=None):
    python = Python.objects.get(pk=pk)
    if slug and python.name.lower() != slug.lower():
        return redirect('404')
    context = {
        'python': python,
    }
    return render(request, 'pythons/details.html', context)


# @group_required(groups=['Regular User'])
# @login_required
# def create(req):
#     if req.method == 'GET':
#         context = {
#             'form': PythonCreateForm(),
#             'current_page': 'create',
#         }
#         return render(req, 'create.html', context)
#     else:
#         form = PythonCreateForm(req.POST, req.FILES)
#         print(form)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#         context = {
#             'form': form,
#             'current_page': 'create',
#         }
#         return render(req, 'create.html', context)

# @method_decorator(group_required(groups=['Regular User']), name='dispatch')
class PythonCreateView(GroupRequiredMixin, LoginRequiredMixin, FormView):
    form_class = PythonCreateForm
    template_name = 'create.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
