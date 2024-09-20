from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Teams,Match,Logs
# Create your views here.

def showTable(request):
    all_teams = Teams.objects.all()
    context = {'teams': all_teams}
    return render(request, 'table.html', context)

def addTeams(request):
    if request.method == 'POST':
        team = request.POST.get('team')
        regDate = request.POST.get('registrationDate')
        groupNo = request.POST.get('groupNo')
        newTeam = Teams(name=team,regDate = regDate,groupNo = groupNo)
        newTeam.save()
        # Process the team here (e.g., save it to a database, display a message)
        return render(request, 'result.html', {'team': team})
    else:
        return render(request, 'index.html')

def showMatches(request):
    match = Match.objects.all()
    context = {'match':match}
    return render(request, 'matches.html', context)

def showLogs(request):
    logs = Logs.objects.all()
    context = {'logs':logs}
    return render(request, 'logs.html', context)

def showSearch(request):
    logs = Logs.objects.all()
    context = {'logs':logs}
    return render(request, 'search.html', context)