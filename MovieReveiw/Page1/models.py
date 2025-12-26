from django.db import models
from django.contrib.auth.hashers import check_password
from django.utils import timezone


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=50, default='user')
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name
    def get_email(self):
        return self.email
    def get_role(self):
        return self.role
    def get_First_name(self):
        return self.first_name
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    def check_password(self, password):
        return check_password(password, self.password)
    def set_password(self, new_password):
        self.password = new_password
        self.save()

class Movie(models.Model):
    moID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    additional_genres = models.CharField(max_length=200, blank=True, null=True)
    release_date = models.DateField()
    director = models.CharField(max_length=100)
    cast = models.TextField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    rating = models.CharField(max_length=10, blank=True, null=True)
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    description = models.TextField(default='No description available')
    poster_url = models.URLField(blank=True, null=True)
    trailer_url = models.URLField(blank=True, null=True)
    language = models.CharField(max_length=50, default='English')
    country = models.CharField(max_length=50, default='USA')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    def get_genre(self):
        return self.genre
    def get_release_date(self):
        return self.release_date
    def get_director(self):
        return self.director
    def get_moID(self):
        return self.moID

class Review(models.Model):
    reviewID = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    status = models.CharField(max_length=50, default='pending')
    admin_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Review by {self.user.get_full_name()} for {self.movie.title}"
    def get_rating(self):
        return self.rating
    def get_comment(self):
        return self.comment
    def get_user(self):
        return self.user
    def get_movie(self):
        return self.movie
    def set_rating(self, new_rating):
        self.rating = new_rating
        self.save()
    def moID(self):
        return self.movie.moID
    def userID(self):
        return self.user.id

class Admin(models.Model):
    adminID = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, default='admin')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Admin: {self.get_full_name()}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_email(self):
        return self.email

    def get_role(self):
        return self.role

    def check_password(self, password):
        return check_password(password, self.password)

    def set_password(self, new_password):
        self.password = new_password
        self.save()

    def get_adminID(self):
        return self.adminID
