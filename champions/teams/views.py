from django.shortcuts import redirect, render
from django.http import HttpResponse,JsonResponse
from django.views.generic import TemplateView
from django.core import serializers
from .models import Teams,Match,Logs
import re
from datetime import datetime
from django.db.models import Q
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
        return response
    else:
        all_teams = Teams.objects.all()
        context = {'teams': all_teams}
        return render(request, 'table.html', context)

def showMatches(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        match action:
            case 'add':
                response = addMatches(data.get('data'))
            case 'remove':
                response = removeMatches(data.get('data'))
            case 'clear':
                response = clearMatches()
            case 'update':
                response = updateMatches(data.get('data'))
            case _:
                response = JsonResponse({'Error':'Unable to recognise button'},status=400)
        return response
    else:
        match = Match.objects.all()
        context = {'match':match}
        return render(request, 'matches.html', context)

def showLogs(request):
    logs = Logs.objects.all()
    context = {'logs':logs}
    return render(request, 'logs.html', context)

def showSearch(request):
    context = {'match':None,'team':None}
    if request.method == 'POST':
        data = json.loads(request.body)
        team = Teams.objects.filter(name=data)
        if len(team) != 0:
            
            teamList = serializers.serialize('json', team)
            team = team[0]
            match = Match.objects.filter(Q(team1=team) | Q(team2=team))
            matchList = serializers.serialize('json', match)
            context = JsonResponse({"match":matchList,"team":teamList,"status":"success"},status=200)
            return context
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
            error = str(e)
            break
    if success:
        return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse({'Error':error},status=400)
    
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
        error = str(e)
    if success:
        return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse({'Error':error},status=400)
    
def addMatches(data):
    success=True
    data = data.strip().split("\n")
    for team in data:
        try:
            team = team.strip().split(" ")
            assert len(team) == 4, "Wrong Number of Fields" 
            team1 = Teams.objects.filter(name=team[0])[0]
            team2 = Teams.objects.filter(name=team[1])[0]
            newMatch = Match(team1=team1,team2=team2,score1=team[2],score2=team[3])
            newMatch.save()
        except Exception as e:
            success = False
            error = str(e)
            break
    if success:
        return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse({'Error':error},status=400)
        

def clearMatches():
    success=True
    try:
        Match.objects.all().delete()
    except Exception as e:
        success = False
        error = str(e)
    if success:
        return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse({'Error':error},status=400)

def updateMatches(data):
    print(data)

def removeMatches(data):
    success=True
    # Parse NodeList
    indexList = []
    for x in data:
        indexList.append(int(x[:-1]))
    try:
        query = Match.objects.filter(id__in=indexList)
        query.delete()
    except Exception as e:
        success = False
        error = str(e)
    if success:
        return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse({'Error':error},status=400)