from asyncio.tasks import ensure_future
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404, HttpResponse
import requests, json
from pprint import pprint
from django.views.generic import TemplateView, ListView
from .models import  *
from django.contrib.auth.models import User
from fpl import FPL
import aiohttp
import asyncio
from .utils import *
import random

class HomeView(TemplateView):
    template_name = 'newtemplate/index.html'

    def get(self, request):
        company=get_object_or_404(Company, id=1)
        gwwinner=Gameweekwinner.objects.filter(activeinhome='active')
        winner=Winner.objects.all()
        latest_gameweek = get_latest_gameweek()
        gameweekwinner=get_object_or_404(Gameweekwinner,gameweek=latest_gameweek)

        args={
            'company':company,
            'gwwinner':gwwinner,
            'winner':winner,
            'latest_gameweek':latest_gameweek,
            'gameweekwinner':gameweekwinner

        }
        return render(request,self.template_name,args)

class RewardsView(TemplateView):
    template_name='newtemplate/rewards.html'

    def get(self,request):
        company=get_object_or_404(Company, id=1)
        teams=Teams.objects.all()
        args={
            'company':company,
        }
        return render(request,self.template_name,args)

class RulesView(TemplateView):
    template_name='newtemplate/rules.html'

    def get(self,request):
        company=get_object_or_404(Company, id=1)
        teams=Teams.objects.all()
        args={
            'company':company,
        }
        return render(request,self.template_name,args)

# standing results
class TeamView(TemplateView):
    template_name='newtemplate/teams.html'

    def get(self,request):
        classic_league=asyncio.run(get_players_data())
        # print(classic_league)
        for player in classic_league['standings']['results']:
            # print(player['id'])
            # print(player['event_total'])
            name=player['player_name']
            rank=player['rank']
            rank=player['last_rank']
            totalpoints=(player['total'])
            entry=player['entry']
            teamname=player['entry_name']

            try:
                obj=Teams.objects.get(entry=entry)
                print(name+'Data already exists')
            except Teams.DoesNotExist:
                Teams.objects.create(name=name,teamname=teamname,entry=entry)

        winner=Winner.objects.all()
        # company=get_object_or_404(Company, id=1)
        teams=Teams.objects.all()
        args={
            # 'company':company,
            'teams':teams,
            'winner':winner
        }
        return render(request,self.template_name,args)

# class newEntryTeamView(TemplateView):
#     template_name='newtemplate/teams.html'

#     def get(self,request):
#         classic_league=get_newentries_classicleagues()
#         print(classic_league)

#         for player in classic_league['new_entries']['results']:
#             # print(player['id'])
#             # print(player['event_total'])
#             name=player['player_first_name']+""+player['player_last_name']
#             # rank=player['rank']
#             # rank=player['last_rank']
#             # totalpoints=(player['total'])
#             entry=player['entry']
#             teamname=player['entry_name']

#             try:
#                 obj=Teams.objects.get(entry=entry)
#                 # print(name+'Data already exists')
#             except Teams.DoesNotExist:
#                 Teams.objects.create(name=name,teamname=teamname,entry=entry)

#         winner=Winner.objects.all()
#         # company=get_object_or_404(Company, id=1)
#         teams=Teams.objects.all()
#         args={
#             # 'company':company,
#             'teams':teams,
#             'winner':winner
#         }
#         return render(request,self.template_name,args)

class PlayerDetailsView(TemplateView):
    template_name='newtemplate/include/player-detail.html'

    def get(self,request,pk):
        # company=get_object_or_404(Company, id=1)
        team=Teams.objects.get(id=pk)
        gameweek=Gameweek.objects.filter(player__id=pk)
        args={
            # 'company':company,
            'team':team,
            'gameweek':gameweek
        }
        return render(request,self.template_name,args)



class AboutView(TemplateView):
    template_name='newtemplate/about.html'
    
    def get(self,request):
        company=get_object_or_404(Company, id=1)

        args={
            'company':company
        }
        return render(request,self.template_name,args)

class GameweekWinnerView(TemplateView):
    template_name='newtemplate/gameweekwinner.html'

    def get(self,request):
        company=get_object_or_404(Company, id=1)
        gwwinner=Gameweekwinner.objects.all().order_by('-gameweek')

        args={
            'company':company,
            'gwwinner':gwwinner,
        }
        return render(request,self.template_name,args)

class ClassicLeagueView(ListView):
    template_name='newtemplate/classicleague.html'
    model = ClassicLeague
    
    def get_queryset(self):
        return super().get_queryset().order_by('position')


class RulesView(TemplateView):
    template_name='newtemplate/rules.html'

    def get(self,request):
        company=get_object_or_404(Company, id=1)
        args={
            'company':company,
        }
        return render(request,self.template_name,args)



class DivisionView(TemplateView):
    template_name='newtemplate/division.html'

    def get(self,request):
        company=get_object_or_404(Company, id=1)
        teama=DivisionLeague.objects.filter(name__divisions__name="A")
        for obj in teama:
            print(obj)
        teamb=DivisionLeague.objects.filter(name__divisions__name="B")
        # teamc=DivisionLeague.objects.filter(name__divisions__name="C")
        # teamd=DivisionLeague.objects.filter(name__divisions__name="D")


        args={
            'company':company,
            'teama':teama,
            'teamb':teamb,
            # 'teamc':teamc,
            # 'teamd':teamd
        }
        return render(request,self.template_name,args)

class DivisionSelectionView(TemplateView):
    template_name='newtemplate/include/getdivisions.html'

    def get(self,request,division):
        company=get_object_or_404(Company, id=1)
        team=DivisionLeague.objects.filter(name__divisions__name=division)
        get_division=division
        print(team)
        args={
            'company':company,
            'team':team,
            'get_division':get_division
        }
        return render(request,self.template_name,args)

class EliminationLeagueView(TemplateView):
    template_name='newtemplate/elimination.html'

    def get(self,request):
        company=get_object_or_404(Company, id=1)
        eliminitedteam=Teams.objects.filter(elimination="eliminated").order_by('-eliminated_gameweek')
        totalmanagers=Teams.objects.count()
        eliminatedmanagers=Teams.objects.filter(elimination='eliminated').count()
        remainingmanagers=totalmanagers-eliminatedmanagers

        # for team in divisiona.team.all():
        #     print(team.name)
            
        divisions=Division.objects.all()

        args={
            'company':company,
            'eliminitedteam':eliminitedteam,
            'totalmanagers':totalmanagers,
            'eliminatedmanagers':eliminatedmanagers,
            'remainingmanagers':remainingmanagers
        }
        return render(request,self.template_name,args)


class DivisionGameWeekWinnerView(TemplateView):
    template_name='newtemplate/divisiongameweekwinner.html'

    def get(self,request):
        company=get_object_or_404(Company, id=1)
        gwwinner=DivisionGameweekWinner.objects.filter().order_by('-gameweek')

        args={
            'company':company,
            'gwwinner':gwwinner,
        }
        return render(request,self.template_name,args)

class IamSafeView(ListView):
    template_name='newtemplate/iamsafe.html'
    model = ClassicLeague

    def get_queryset(self):
        return super().get_queryset().filter()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["safe_teams"] = self.model.objects.filter(name__issafe="safe")
        context["unsafe_teams"] = self.model.objects.filter(name__issafe="not safe")
        return context

        divisions=Division.objects.all()

        args={
            'company':company,
            'totalmanagers':totalmanagers,
            'eliminatedmanagers':eliminatedmanagers,
            'remainingmanagers':remainingmanagers
        }
        return render(request,self.template_name,args)

class RewardsView(TemplateView):
    template_name='newtemplate/rewards.html'

    def get(self,request):
        company=get_object_or_404(Company, id=1)

        args={
            'company':company
        }
        return render(request,self.template_name,args)

class BlogsView(TemplateView):
    template_name='blog.html'

    def get(self,request):
        args={

        }
        return render(request,self.template_name,args)

class BlogsingleView(TemplateView):
    template_name='single.html'

    def get(self,request):
        args={

        }
        return render(request,self.template_name,args)


class ContactView(TemplateView):
    template_name='newtemplate/contact.html'

    def get(self,request):
        company=get_object_or_404(Company, id=1)

        args={
            'company':company
        }
        return render(request,self.template_name,args)



async def get_fpl_data():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        # data = {"email":"yomeroenpal7@gmail.com", "password":"Rojesh9849#"}
        # await fpl.login(data)
        # print(fpl.get_player(302,return_json=True,9999999)
        user = await fpl.get_user(1501325)
        return await user.get_team()


async def get_home(request):
    data=[]
    player = asyncio.ensure_future(get_fpl_data())
    data.append(player)
    
    result = await asyncio.gather(*data)
    print(result)
    return HttpResponse(player)


def classicleagues():
        '''get all past season info for a given player_id'''
        
        # send GET request to
        # https://fantasy.premierleague.com/api/element-summary/{PID}/
        r = requests.get(
                base_url + 'leagues-classic/188305/standings/'
        ).json()
        
        # extract 'history_past' data from response into dataframe
        return r

async def get_players_data():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        await fpl.login(email="aryan.sainju@gmail.com",password="probook450")
        # classic_league = await fpl.get_classic_league(188305,return_json=True)
        classic_league=classicleagues()

    return classic_league

async def get_deadline():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        gameweek = await fpl.get_gameweek(1,return_json=True)
    print(gameweek)


# # base url for all FPL API endpoints
base_url = 'https://fantasy.premierleague.com/api/'

# # get data from bootstrap-static endpoint
# r = requests.get(base_url+'bootstrap-static/').json()


def get_gw():
        '''get all past season info for a given player_id'''
        
        # send GET request to
        # https://fantasy.premierleague.com/api/element-summary/{PID}/
        r = requests.get(
                base_url + 'entry/1311418/history/'
        ).json()
        
        # extract 'history_past' data from response into dataframe
        for gw in r['current']:
            gameweeek=gw['event']
            try:
                obj=Gameweek.objects.get(no=gameweeek)
                # print(str(gameweeek)+'Data already exists')
            except Gameweek.DoesNotExist:
                Gameweek.objects.create(no=gameweeek)


def check_iam_safe(request):
    teams = Teams.objects.filter(issafe="safe")
    for team in teams:
        gameweeks = Gameweek.objects.filter(player=team)
        for gameweek in gameweeks:
            safe_point = IamSafe.objects.get(gameweek=gameweek.no)
            if gameweek.no == safe_point.gameweek:
                if gameweek.point < safe_point.safemargin:
                    team.issafe = "not safe"
                    if not team.eliminated_gameweek:
                        team.eliminated_gameweek=gameweek.no
                    team.save()
                    print(team, gameweek.no)
    for team in teams:
        print(team.name)
    return HttpResponse(teams) 

# Get gameweek winner and save it in winner database

def get_gameweek_winner():
    latest_gameweek = get_latest_gameweek()
    Gameweeks=Gameweek.objects.filter(player__id=51)
    print(latest_gameweek)
    for gw in Gameweeks:
        no= gw.no
        gameweek_winner_point = Gameweek.objects.filter(no=no).order_by('-point').first()
        gameweek_winners = Gameweek.objects.filter(no=gameweek_winner_point.no, point=gameweek_winner_point.point)
        gameweek_winner, created = Gameweekwinner.objects.get_or_create(
            gameweek=gameweek_winner_point.no,
            points=gameweek_winner_point.point,
            activeinhome="active",
        )
        for game in gameweek_winners:
            gameweek_winner.name.add(game.player)
   
    
    return HttpResponse(f"{gameweek_winner_point.player.name}")

get_gameweek_winner()
# def get_division_gameweek_winner():
#     latest_gameweek = get_latest_gameweek()
#     Gameweeks=Gameweek.objects.filter(player__id=51)
#     divisions=Division.objects.all()
#     print(latest_gameweek)
#     for division in divisions:
#         for gw in Gameweeks:
#             no= gw.no
#             gameweek_winner_point = Gameweek.objects.filter(no=no).order_by('-point').first()
#             gameweek_winners = Gameweek.objects.filter(no=gameweek_winner_point.no, point=gameweek_winner_point.point)
#             gameweek_winner, created = DivisionGameweekWinner.objects.get_or_create(
#                 gameweek=gameweek_winner_point.no,
#                 points=gameweek_winner_point.point,
#             )
#             gameweek_winner.name.add(game.player)
   
    
#     return HttpResponse(f"{gameweek_winner_point.player.name}")

def partition (list_in, n):
    random.shuffle(list_in)
    return ([list_in[i::n] for i in range(n)])

# Creates respective division with teams divided accordingly
# def create_division():
#     teams=Teams.objects.all()
#     team_list=[]
#     i=1
#     for team in teams:
#         team_list.append(team.id)
#         i=i+1

#     p=partition(team_list,4)


#     divisions=['A','B','C','D']
#     i=0
#     for division in divisions:
#         division, created = Division.objects.get_or_create(
#                 name=division
#             )

#         for team in p[i]:
#             # print(team)
#             player=get_object_or_404(Teams,id=team)
#             player.divisions=division
#             player.save()

#         i=i+1


def create_iamsafe_margin():
    gameweeeks=([1,2,3,4,5,6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25],[26,27,28,29,30])
    average_gameweek=[31,32,33,34,35,36,37,38]
    safe_margin=[25,28,32,35,38]

    j=0
    for gameweek in gameweeeks:
        for i in gameweeeks[j]:
            safe, created = IamSafe.objects.get_or_create(
                safemargin=safe_margin[j],
                gameweek=i
            )
        j=j+1


def get_division_league():
    latest_gameweek = get_latest_gameweek()
    print(latest_gameweek)
    divisions=Division.objects.all()
    for division in divisions:
        print(division)
        teams=Gameweek.objects.filter(no=latest_gameweek,player__divisions__name=division).order_by("-totalpoints")
        position=1
        print(teams)
        for team in teams:
            user=get_object_or_404(Teams,id=team.player.id)
            classic_league,created = DivisionLeague.objects.get_or_create(
                position=position,
                event_total=team.point,
                total_points=team.totalpoints,
                defaults={'name':user})
            position=position+1



def get_newentries_classicleagues():
        '''get all past season info for a given player_id'''
        
        # send GET request to
        # https://fantasy.premierleague.com/api/element-summary/{PID}/
        r = requests.get(
                base_url + 'leagues-classic/188305/standings'
        ).json()
        
        # extract 'history_past' data from response into dataframe
        return r

def get_results(r):
    for standing in r['standings']['results']:
            user = get_object_or_404(Teams,entry=standing['entry'])
            classic_league,created = ClassicLeague.objects.get_or_create(position=standing['rank'],event_total=standing['event_total'], total_points=standing['total'],defaults={'name':user})
            if not created:
                classic_league.position =standing['rank']
                classic_league.event_total=standing['event_total']
                classic_league.total_points=standing['total']
                classic_league.save()
                print("updated")
