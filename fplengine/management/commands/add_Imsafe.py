from django.core.management.base import BaseCommand, CommandError
from fplengine.models import *
import requests

im_safe=[
    (1,25),
    (2,25),
    (3,25),
    (4,25),
    (5,25),
    (6,25),
    (7,25),
    (8,25),
    (9,25),
    (10,25),
    (11,28),
    (12,28),
    (13,28),
    (14,28),
    (15,28),
    (16,32),
    (17,32),
    (18,32),
    (19,32),
    (20,32),
    (21,35),
    (22,35),
    (23,35),
    (24,35),
    (25,35),
    (26,38),
    (27,38),
    (28,38),
    (29,38),
    (30,38),
    (31,41),
    (32,41),
    (33,41),
    (34,41),
    (35,41),
    (36,41),
    (37,41),
    (38,41),
]

class Command(BaseCommand):
    help = 'populate gameweek table'

    def handle(self, *args, **kwargs):
        for m in im_safe:
            IamSafe.objects.create(
                safemargin=m[1],
                gameweek=m[0]
            )
        
        print("created")
