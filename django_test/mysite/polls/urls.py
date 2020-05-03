from django.urls import path
from . import views


# 应用中的路由文件时单独建立的
# 可以不使用应用路由，而从项目直接路由到应用的视图


app_name = 'polls'


urlpatterns = [
    path('index', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]