from django.contrib import admin
from django.urls import path, include
from soccer.views import index, search_view, test1, homepage, search_similar, shot_view, pass_view, goal_view, goal_pass_relation, total_stat

from soccer.views import total_map, draw_chart, draw_y_chart, draw_x, sim_view, player_search, radier_p

urlpatterns = [
    path('', homepage),
    path('bar', index),
    path('search_f/', search_view),
    path('test1', test1),
    path('search_sim', search_similar),
    path('total_stat', total_stat),
    path('shot_view', shot_view),
    path('pass_view', pass_view),
    path('goal_view', goal_view),
    path('heatmap_view', goal_pass_relation),
    path('total_map', total_map),
    path('draw', draw_chart),
    path('y_draw', draw_y_chart),

    path('draw/<int:x>', draw_x),
    path('search_sim_plus', sim_view),
    path('player_search', player_search),
    path('radier_p', radier_p),
]