from django.shortcuts import render, redirect
# from seoullibrary.visualization import visual
from visualization import visual


def index(request):
    contexts = dict()
    contexts['intro_library_num'] = visual.intro_library_num()
    contexts['intro_map'] = visual.intro_map()
    contexts['rent_ages'] = visual.rent_ages()
    contexts['gu_lib_budget'] = visual.gu_lib_budget()
    contexts['income_lib'] = visual.income_lib

    return render(request, 'index.html', contexts)

def newloc(request):
    contexts = dict()
    contexts['income_lib'] = visual.income_lib
    contexts['satisfaction'] = visual.satisfaction()
    contexts['lib_visitor'] = visual.lib_visitor()
    contexts['pop_visit'] = visual.pop_visit()
    contexts['schoolage_visit'] = visual.schoolage_visit()
    contexts['age_percent'] = visual.age_percent()

    return render(request, 'newloc.html', contexts)

def disadv(request):
    contexts = dict()
    contexts['corr_heatmap'] = visual.corr_heatmap()
    contexts['disadv_budget_users'] = visual.disadv_budget_users()
    contexts['disadv_av_budget_income'] = visual.disadv_av_budget_income()

    return render(request, 'disadv.html', contexts)

def conclusion(request):
    contexts = dict()
    contexts['conclusion'] = visual.conclusion()

    return render(request, 'conclusion.html', contexts)