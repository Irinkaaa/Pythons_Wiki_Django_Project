from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from pythons_core.decorators import group_required
from .forms import PythonCreateForm, FilterForm
from .models import Python


def extract_filter_values(params):
    order = params['order'] if 'order' in params else FilterForm.ORDER_ASC
    text = params['text'] if 'text' in params else ''
    return {
        'order': order,
        'text': text,
    }


def index(req):
    params = extract_filter_values(req.GET)
    order_by = 'name' if params['order'] == FilterForm.ORDER_ASC else '-name'
    pythons = Python.objects.filter(name__icontains=params['text']).order_by(order_by)
    for python in pythons:
        python.can_delete = python.created_by_id == req.user.id

    context = {
        'pythons': pythons,
        'filter_form': FilterForm(initial=params)
    }
    return render(req, 'index.html', context)


def python_details(request, pk, slug=None):
    python = Python.objects.get(pk=pk)
    if slug and python.name.lower() != slug.lower():
        return redirect('404')
    context = {
        'python': python,
    }
    return render(request, 'pythons/details.html', context)


# @group_required(groups=['Regular User'])
@login_required
def create(req):
    if req.method == 'GET':
        context = {
            'form': PythonCreateForm(),
            'current_page': 'create',
        }
        return render(req, 'create.html', context)
    else:
        data = req.POST
        form = PythonCreateForm(data, req.FILES)
        print(form)
        if form.is_valid():
            python = form.save()
            python.save()
            return redirect('index')
