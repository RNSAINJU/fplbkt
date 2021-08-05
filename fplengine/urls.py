from .views import *
from django.conf.urls import url
from django.urls import include,path

app_name = 'cv'

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    path('teams', TeamView.as_view(), name='teams'),
    path('player/<int:pk>/', PlayerDetailsView.as_view(), name='player-detail'),
    path('division/<str:division>/', DivisionSelectionView.as_view(), name='divisionselection'),
    path('about',AboutView.as_view(),name='about'),
    path('rewards',RewardsView.as_view(),name='rewards'),
    path('rewards',RulesView.as_view(),name='rewards'),
    path('gameweekwinner',GameweekWinnerView.as_view(),name='gameweekwinner'),
    path('classicleague',ClassicLeagueView.as_view(),name='classicleague'),
    path('divisionleague',DivisionView.as_view(),name='divisionleague'),
    path('divisiongameweekwinner',DivisionGameWeekWinnerView.as_view(),name='divisiongameweekwinner'),
    path('eliminationleague',EliminationLeagueView.as_view(),name='eliminationleague'),
    path('iamsafe',IamSafeView.as_view(),name='iamsafe'),
    path('blogs',BlogsView.as_view(),name='blogs'),
    path('blog/',BlogsingleView.as_view(),name='blog'),
    path('rules',RulesView.as_view(),name='rules'),
    path('contact',ContactView.as_view(),name='contact'),


    path('home', get_home, name='fpl-home'),
    path('check-safe', check_iam_safe ,name="check-safe"),
    path('latest-gameweek-winner', get_gameweek_winner, name='gameweek-winner'),
]

