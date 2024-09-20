from django.shortcuts import redirect, render
from django.http import HttpResponse,JsonResponse
from django.views.generic import TemplateView
from .models import Teams,Match,Logs
import re
from datetime import datetime
import json
# Create your views here.
pattern = "^(0[1-9]|[1-2]\\d|3[0-1])\\/(0[1-9]|1[0-2])$"
def showTable(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        match action:
            case 'add':
                response = addTeams(data.get('data'))
            case 'remove':
                response = removeTeams(data.get('data'))
            case 'clear':
                response = clearTeams()
            case _:
                response = JsonResponse({'Error':'Unable to recognise button'},status=400)
        print(type(response))
        return response
    else:
        all_teams = Teams.objects.all()
        context = {'teams': all_teams}
        return render(request, 'table.html', context)

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

def addTeams(data):
    success=True
    data = data.strip().split("\n")
    for team in data:
        try:
            team = team.strip().split(" ")
            assert len(team) == 3, "Wrong Number of Fields" 
            assert re.match(pattern,team[1]),"Invalid Date"
            regDate =  datetime.strptime(team[1]+'/2000', "%d/%m/%Y")
            newTeam = Teams(name=team[0],regDate = regDate.strftime("%Y-%m-%d"),groupNo = team[2])
            newTeam.save()
        except Exception as e:
            success = False
            print(f"Error: {str(e)}")
        if success:
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'Error':'Error'},status=400)
        
def removeTeams(data):
    success=True
    data = data.strip().split("\n")
    for team in data:

        try:
            team = team.strip()
            query = Teams.objects.filter(name=team)
            if query.exists():
                query.delete()
            else:
                raise Exception("Team not found")
        except Exception as e:
            success = False
            error = str(e)
    if success:
        return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse({'Error': error},status=400)
        
def clearTeams():
    success=True
    try:
        Teams.objects.all().delete()
    except Exception as e:
        success = False
        print(f"Error: {str(e)}")
    if success:
        return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse({'Error':'Error'},status=400)
    