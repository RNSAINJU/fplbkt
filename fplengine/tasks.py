from celery import shared_task
from .models import *
from celery.decorators import periodic_task
from celery.schedules import crontab
# from .utils import get_random_code
import requests



base_url = 'https://fantasy.premierleague.com/api/'

@shared_task
def get_gw_history():

    players=Teams.objects.all()
    for player in players:
        player_id=player.entry
            
        '''get all past season info for a given player_id'''
        
        # send GET request to
        # https://fantasy.premierleague.com/api/element-summary/{PID}/
        r = requests.get(
                base_url + 'entry/' + str(player_id) + '/history/'
        ).json()

        # print(r)
        # extract 'history_past' data from response into dataframe
        for gw in r['current']:
            gameweeek=gw['event']
            points=gw['points']
            point_on_bench=gw['points_on_bench']
            totalpoints=gw['total_points']
            inbank=gw['bank']
            bank=inbank/10      
            value=gw['value']
            new_value=value/10
            event_transfers=gw['event_transfers']
            event_transfers_cost=gw['event_transfers_cost']

        # for gw in r['past']:

        # for chip in r['chips']:
        #     name=chip['name']
        #     time=chip['time']
        #     event=chip['event']

            try:
                obj=Gameweek.objects.get(no=gameweeek,player__entry=player_id)
                print(player.name+str(gameweeek)+'Data already exists')
            except Gameweek.DoesNotExist:
                gameweek=Gameweek.objects.create(
                    no=gameweeek,
                    point=points,
                    point_on_bench=point_on_bench,
                    totalpoints=totalpoints,
                    bank=bank,
                    value=new_value,
                    event_transfers=event_transfers,
                    event_transfers_cost=event_transfers_cost
                    )
                player=get_object_or_404(Teams,entry=player_id)
                gameweek.player=player
                gameweek.save()
                # gameweek.player.add(player)
                print(player.name + "-Gameweek:" + str(gameweeek) + "-"+ str(points))


@periodic_task(run_every=(crontab(minute='*/10')))
def get_gw_history_task():
    get_gw_history.delay()

@shared_task
def get_classic_league():
    url = "https://fantasy.premierleague.com/api/leagues-classic/188305/standings"
    r = requests.get(url).json()
    data=str(r['standings']['has_next'])

    if data == "True":
        firsturl=url
        firstpageresult = requests.get(firsturl).json()
        secondurl="https://fantasy.premierleague.com/api/leagues-classic/188305/standings/?page_standings=2"
        secondpageresult = requests.get(secondurl).json()
        get_results(firstpageresult)
        get_results(secondpageresult)
    else:
      get_results(r)


@periodic_task(run_every=(crontab(minute='*/1')))
def get_classic_league_data():
    get_classic_league.delay()


# def check_iam_safe():
#     teams = Teams.objects.all()
#     for team in teams:
#         gameweek = Gameweek.objects.filter(player=team)
