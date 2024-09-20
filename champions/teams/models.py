from django.db import models

# Create your models here.

from django.db import models
from django.db.models import Q
class Teams(models.Model):
    name = models.CharField(max_length=200)
    regDate = models.DateField()
    groupNo = models.IntegerField()
    score  = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    loss = models.IntegerField(default=0)
    draw = models.IntegerField(default=0)
    games = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)
    def calculate_result(self):
        matches = self.match_set.filter(
            Q(team1=self.name) & Q(team2=self.name)  # Filter using Q objects and AND
        )
        return matches
    
class Match(models.Model):
    team1 = models.ForeignKey(Teams,on_delete=models.CASCADE,related_name='team1_matches')
    team2 = models.ForeignKey(Teams,on_delete=models.CASCADE,related_name='team2_matches')
    score1 = models.IntegerField()
    score2 = models.IntegerField()
    winner = models.ForeignKey(Teams, null=True, blank=True, related_name='won_matches',on_delete=models.CASCADE)

    def calculate_winner(self):
        if self.score1 > self.score2:
            return self.team1
        elif self.score2 > self.score1:
            return self.team2
        return "Draw"

    def save(self, *args, **kwargs):
        self.winner = self.calculate_winner()
        super().save(*args, **kwargs)

class Logs(models.Model):
    string = models.TextField()
