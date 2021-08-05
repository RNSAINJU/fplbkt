from django.core.management.base import BaseCommand, CommandError
from fplengine.models import *
import requests

base_url = 'https://fantasy.premierleague.com/api/'

class Command(BaseCommand):
    help = 'populate gameweek table'

    def handle(self, *args, **kwargs):
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