from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from .forms import PlanForm
from . import planner


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PlanForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            my_plan = planner.sanity_check(form.cleaned_data)
            print(my_plan)

            plan = planner.generate_plan(form.cleaned_data)
            request.session['plan_id'] = plan.id
            # process the data in form.cleaned_data as required
            return redirect('download')
            # return render(request, 'plans/plan.html', {'plan': my_plan})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PlanForm()

    return render(request, 'plans/plan_form.html', {'form': form})


def thanks(request):
    return render(request, 'plans/thanks.html', {})

def download(request):
    if 'plan_id' in request.session:
        context = {'plan_id': request.session['plan_id']}
    else:
        context = {}
    return render(request, 'plans/download.html', context)
