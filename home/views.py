from django.shortcuts import render, redirect
from django.http import HttpResponse, request

from login.models import CharMaster, pSupergroup, pGroup, pModule, pClass

# Create your views here.


def home(request):
    if request.COOKIES.get("username"):
        charmaster = CharMaster.objects.all()
        supergroup = pSupergroup.objects.all()
        group = pGroup.objects.all()
        module = pModule.objects.all()
        pclass = pClass.objects.all()
        results = pClass.objects.all()
        return render(
            request,
            "home.html",
            {
                "charmaster": charmaster,
                "supergroup": supergroup,
                "group": group,
                "module": module,
                "pclass": pclass,
                "results": results,
            },
        )
    else:
        return redirect("/")


def charmap(request):
    return render(request, "charmap.html")


# def ruledef(request):
#     charmaster = CharMaster.objects.all()
#     supergroup = CharMaster.objects.all().distinct('pSuperGroup')
#     group = CharMaster.objects.all().distinct('pGroup')
#     module = CharMaster.objects.all().distinct('pModule')
#     pclass = CharMaster.objects.all().distinct('pClass')
#     return render(request, 'ruledef.html', {'charmaster': charmaster, 'supergroup': supergroup, 'group': group, 'module': module, 'pclass': pclass})
# return HttpResponse("This is the RULES DEFINITION PAGE")


# def ruleexe(request):
#     return render(request, 'ruleexe.html')
#     # return HttpResponse("This is the RULE EXECUTION PAGE")


def asschar(request):
    return render(request, "asschar.html")


def chardef(request):
    return render(request, "chardef.html")


def rolemaster(request):
    return render(request, "rolemaster.html")


def parameter(request):
    return render(request, "parameter_def")
