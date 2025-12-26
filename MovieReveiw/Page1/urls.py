from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('get_movies/', views.get_movies, name='get_movies'),
    path('get_users/', views.get_users, name='get_users'),
    path('get_reviews/', views.get_reviews, name='get_reviews'),
    path('get_recent_activity/', views.get_recent_activity, name='get_recent_activity'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('add-movie/', views.add_movie_view, name='add_movie_page'),
    path('admin/manage_movies/', views.manage_movies_view, name='manage_movies'),
    path('admin/manage_reviews/', views.manage_reviews_view, name='manage_reviews'),
    path('admin/reviews/approve/<int:review_id>/', views.approve_review_view, name='approve_review'),
    path('admin/reviews/reject/<int:review_id>/', views.reject_review_view, name='reject_review'),
    path('admin/movies/edit/<int:movie_id>/', views.edit_movie_view, name='edit_movie'),
    path('admin/movies/delete/<int:movie_id>/', views.delete_movie_view, name='delete_movie'),
    path('signup/', views.signup_view, name='signup'),
    path('home_user/', views.user_home_view, name='user_home'),
    path('home_admin/', views.admin_home_view, name='admin_home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # User Pages
    path('movies/', views.movie_list_view, name='movie_list'),
    path('movies/<int:movie_id>/', views.movie_details_view, name='movie_details'),
    path('my_reviews/', views.my_reviews_view, name='my_reviews'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('submit_review/<int:movie_id>/', views.submit_review_view, name='submit_review'),
    path('submit_review/', views.submit_review_view, name='submit_review_page'),

    # Admin Pages
    path('admin/', views.admin_home_view, name='admin_home'),
    path('admin/manage_movies/', views.manage_movies_view, name='manage_movies'),
    path('admin/manage_reviews/', views.manage_reviews_view, name='manage_reviews'),
    path('admin/reviews/approve/<int:review_id>/', views.approve_review_view, name='approve_review'),
    path('admin/reviews/reject/<int:review_id>/', views.reject_review_view, name='reject_review'),
    path('admin/movies/edit/<int:movie_id>/', views.edit_movie_view, name='edit_movie'),
    path('admin/movies/delete/<int:movie_id>/', views.delete_movie_view, name='delete_movie'),
]