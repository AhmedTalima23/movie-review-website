from urllib import request
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db import models
import json
from .models import User, Admin, Movie,Review

def home_view(request):
    user_data = None
    if 'user_id' in request.session:
        user_data = {
            'name': request.session.get('user_name'),
            'role': request.session.get('user_role'),
            'type': request.session.get('user_type')
        }
    return render(request, 'assets/home.html', {'user': user_data})

def user_home_view(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'user':
        return redirect('/login/')
    user_data = {
        'name': request.session.get('user_name'),
        'role': request.session.get('user_role'),
        'type': request.session.get('user_type')
    }
    return render(request, 'home_user.html', {'user': user_data})

def admin_home_view(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'admin':
        return redirect('/login/')
    user_data = {
        'name': request.session.get('user_name'),
        'role': request.session.get('user_role'),
        'type': request.session.get('user_type')
    }
    return render(request, 'home_admin.html', {'user': user_data})

def add_movie_view(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'admin':
        return redirect('/login/')
    user_data = {
        'name': request.session.get('user_name'),
        'role': request.session.get('user_role'),
        'type': request.session.get('user_type')
    }
    return render(request, 'add_movie.html', {'user': user_data})

def get_movies(request):
    movies = Movie.objects.all().values('moID', 'title', 'genre', 'release_date', 'director', 'poster_url', 'created_at', 'updated_at')
    return JsonResponse(list(movies), safe=False)

def get_users(request):
    users = User.objects.all().values('id', 'first_name', 'last_name', 'email', 'role', 'created_at', 'updated_at')
    return JsonResponse(list(users), safe=False)

def get_reviews(request):
    reviews = Review.objects.all().values('id', 'user__first_name', 'user__last_name', 'movie__title', 'rating', 'comment', 'created_at', 'updated_at')
    return JsonResponse(list(reviews), safe=False)

def get_recent_activity(request):
    # Get recent movies (last 10 created)
    recent_movies = Movie.objects.all().order_by('-created_at')[:10].values(
        'moID', 'title', 'created_at', 'updated_at'
    )
    movies_data = [{'type': 'movie', 'action': 'created', **movie} for movie in recent_movies]

    # Get recent movie updates (last 10 updated, excluding very recent creations)
    recent_movie_updates = Movie.objects.filter(
        updated_at__gt=models.F('created_at')  # Only if updated after creation
    ).order_by('-updated_at')[:10].values(
        'moID', 'title', 'created_at', 'updated_at'
    )
    movie_updates_data = [{'type': 'movie', 'action': 'updated', **movie} for movie in recent_movie_updates]

    # Get recent users (last 10 registered)
    recent_users = User.objects.all().order_by('-created_at')[:10].values(
        'id', 'first_name', 'last_name', 'email', 'created_at', 'updated_at'
    )
    users_data = [{'type': 'user', 'action': 'registered', **user} for user in recent_users]

    # Get recent reviews (last 10 submitted)
    recent_reviews = Review.objects.all().order_by('-created_at')[:10].values(
        'id', 'user__first_name', 'user__last_name', 'movie__title', 'rating', 'created_at', 'updated_at'
    )
    reviews_data = [{'type': 'review', 'action': 'submitted', **review} for review in recent_reviews]

    # Get recent review updates (last 10 updated)
    recent_review_updates = Review.objects.filter(
        updated_at__gt=models.F('created_at')  # Only if updated after creation
    ).order_by('-updated_at')[:10].values(
        'id', 'user__first_name', 'user__last_name', 'movie__title', 'rating', 'created_at', 'updated_at'
    )
    review_updates_data = [{'type': 'review', 'action': 'updated', **review} for review in recent_review_updates]

    # Get recent admins (last 10 created)
    recent_admins = Admin.objects.all().order_by('-created_at')[:10].values(
        'adminID', 'first_name', 'last_name', 'email', 'created_at', 'updated_at'
    )
    admins_data = [{'type': 'admin', 'action': 'created', **admin} for admin in recent_admins]

    # Combine all activities and sort by timestamp (use updated_at for updates, created_at for creations)
    all_activities = movies_data + movie_updates_data + users_data + reviews_data + review_updates_data + admins_data

    # Sort by the most recent timestamp (updated_at if it's an update, otherwise created_at)
    for activity in all_activities:
        if activity['action'] == 'updated':
            activity['timestamp'] = activity['updated_at']
        else:
            activity['timestamp'] = activity['created_at']

    all_activities.sort(key=lambda x: x['timestamp'], reverse=True)

    # Return top 20 most recent activities
    return JsonResponse(all_activities[:20], safe=False)

def signup_view(request):
    if request.method == 'POST':
        # Handle traditional form POST request
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        role = request.POST.get('role', 'user')

        # Validation
        if not all([first_name, last_name, email, password, confirm_password]):
            return render(request, 'signup.html', {'error': 'Please fill in all fields.'})

        # Validate email format
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return render(request, 'signup.html', {'error': 'Please enter a valid email address.'})

        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Passwords do not match.'})

        if len(password) < 6:
            return render(request, 'signup.html', {'error': 'Password must be at least 6 characters long.'})

        # Check if email already exists in User or Admin
        if User.objects.filter(email=email).exists() or Admin.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'An account with this email already exists.'})

        try:
            if role == 'user':
                # Create user
                user = User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=make_password(password),  # Hash the password
                    role=role
                )
                request.session['user_type'] = 'user'
                request.session['user_id'] = user.id
                request.session['user_role'] = user.role
                request.session['user_name'] = user.get_full_name()
                return redirect('user_home')
            elif role == 'admin':
                # Create admin
                admin = Admin.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=make_password(password),  # Hash the password
                    role=role
                )
                request.session['user_type'] = 'admin'
                request.session['user_id'] = admin.adminID
                request.session['user_role'] = admin.role
                request.session['user_name'] = admin.get_full_name()
                return redirect('admin_home')
            else:
                return render(request, 'signup.html', {'error': 'Invalid role selected.'})

        except Exception as e:
            return render(request, 'signup.html', {'error': f'An error occurred: {str(e)}'})

    # GET request - render the signup form
    return render(request, 'signup.html')
def login_view(request):
    if request.method == 'POST':
        # Handle traditional form POST request
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        # Validation
        if not all([email, password]):
            return render(request, 'login.html', {'error': 'Please fill in all fields.'})

        # Check in User model
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                request.session['user_type'] = 'user'
                request.session['user_id'] = user.id
                request.session['user_role'] = user.role
                request.session['user_name'] = user.get_full_name()
                return redirect('user_home')
            else:
                return render(request, 'login.html', {'error': 'Invalid email or password.'})
        except User.DoesNotExist:
            pass

        # Check in Admin model
        try:
            admin = Admin.objects.get(email=email)
            if admin.check_password(password):
                request.session['user_type'] = 'admin'
                request.session['user_id'] = admin.adminID
                request.session['user_role'] = admin.role
                request.session['user_name'] = admin.get_full_name()
                return redirect('admin_home')
            else:
                return render(request, 'login.html', {'error': 'Invalid email or password.'})
        except Admin.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid email or password.'})

    # GET request - render the login form
    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    return redirect('/')

@require_POST
@csrf_exempt
def add_movie(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'admin':
        return JsonResponse({'success': False, 'message': 'Unauthorized access.'})

    try:
        data = json.loads(request.body)

        # Validate required fields
        required_fields = ['title', 'genre', 'releaseYear', 'director', 'description', 'language', 'country']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({'success': False, 'message': f'{field} is required.'})

        # Check if movie with same title already exists
        if Movie.objects.filter(title__iexact=data['title']).exists():
            return JsonResponse({'success': False, 'message': f'A movie with the title "{data["title"]}" already exists.'})

        # Create the movie
        movie = Movie.objects.create(
            title=data['title'],
            genre=data['genre'],
            additional_genres=data.get('additionalGenres', ''),
            release_date=f"{data['releaseYear']}-01-01",  # Convert year to date
            director=data['director'],
            cast=data.get('cast', ''),
            duration=int(data['duration']) if data.get('duration') else None,
            rating=data.get('rating', ''),
            imdb_rating=float(data['imdbRating']) if data.get('imdbRating') else None,
            description=data['description'],
            poster_url=data.get('poster', ''),
            trailer_url=data.get('trailer', ''),
            language=data['language'],
            country=data['country']
        )
        ##

        return JsonResponse({
            'success': True,
            'message': f'Movie "{movie.title}" has been added successfully!',
            'movie_id': movie.moID
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid request data.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'})

def manage_movies_view(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'admin':
        return redirect('/login/')
    
    # Get all movies from database
    movies = Movie.objects.all().order_by('-created_at')
    
    # Convert to list of dictionaries for template
    movies_list = []
    for movie in movies:
        movies_list.append({
            'id': movie.moID,
            'movieId': movie.moID,  # For backward compatibility
            'title': movie.title,
            'genre': movie.genre,
            'additionalGenres': movie.additional_genres,
            'releaseYear': movie.release_date.year if movie.release_date else None,
            'year': movie.release_date.year if movie.release_date else None,  # For backward compatibility
            'director': movie.director,
            'poster': movie.poster_url,
            'image': movie.poster_url,  # For backward compatibility
        })
    
    user_data = {
        'name': request.session.get('user_name'),
        'role': request.session.get('user_role'),
        'type': request.session.get('user_type')
    }
    
    return render(request, 'manage_movies.html', {
        'user': user_data,
        'movies': movies_list
    })

def edit_movie_view(request, movie_id):
    if 'user_id' not in request.session or request.session.get('user_type') != 'admin':
        return redirect('/login/')
    
    try:
        movie = Movie.objects.get(moID=movie_id)
    except Movie.DoesNotExist:
        messages.error(request, 'Movie not found.')
        return redirect('/admin/manage_movies/')
    
    if request.method == 'POST':
        # Handle movie update
        movie.title = request.POST.get('title', movie.title)
        movie.genre = request.POST.get('genre', movie.genre)
        movie.additional_genres = request.POST.get('additionalGenres', movie.additional_genres)
        
        release_year = request.POST.get('releaseYear')
        if release_year:
            movie.release_date = f"{release_year}-01-01"
        
        movie.director = request.POST.get('director', movie.director)
        movie.cast = request.POST.get('cast', movie.cast)
        
        duration = request.POST.get('duration')
        if duration:
            movie.duration = int(duration)
        
        movie.rating = request.POST.get('rating', movie.rating)
        
        imdb_rating = request.POST.get('imdbRating')
        if imdb_rating:
            movie.imdb_rating = float(imdb_rating)
        
        movie.description = request.POST.get('description', movie.description)
        movie.poster_url = request.POST.get('poster', movie.poster_url)
        movie.trailer_url = request.POST.get('trailer', movie.trailer_url)
        movie.language = request.POST.get('language', movie.language)
        movie.country = request.POST.get('country', movie.country)
        
        movie.save()
        
        messages.success(request, f'Movie "{movie.title}" has been updated successfully.')
        return redirect('/admin/manage_movies/')
    
    # GET request - show edit form
    movie_data = {
        'id': movie.moID,
        'movieId': movie.moID,
        'title': movie.title,
        'genre': movie.genre,
        'additionalGenres': movie.additional_genres,
        'releaseYear': movie.release_date.year if movie.release_date else None,
        'director': movie.director,
        'cast': movie.cast,
        'duration': movie.duration,
        'rating': movie.rating,
        'imdbRating': movie.imdb_rating,
        'description': movie.description,
        'poster': movie.poster_url,
        'trailer': movie.trailer_url,
        'language': movie.language,
        'country': movie.country,
    }
    
    user_data = {
        'name': request.session.get('user_name'),
        'role': request.session.get('user_role'),
        'type': request.session.get('user_type')
    }
    
    return render(request, 'edit_movie.html', {
        'user': user_data,
        'movie': movie_data
    })

@require_POST
def delete_movie_view(request, movie_id):
    if 'user_id' not in request.session or request.session.get('user_type') != 'admin':
        return redirect('/login/')
    
    try:
        movie = Movie.objects.get(moID=movie_id)
        movie_title = movie.title
        
        # Delete associated reviews first
        Review.objects.filter(movie_id=movie_id).delete()
        
        # Then delete the movie
        movie.delete()
        
        messages.success(request, f'Movie "{movie_title}" has been deleted successfully.')
    except Movie.DoesNotExist:
        messages.error(request, 'Movie not found.')
    
    return redirect('/admin/manage_movies/')