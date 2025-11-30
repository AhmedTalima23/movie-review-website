// Function to generate movie ID from title
function generateMovieId(title) {
    return title.toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-+|-+$/g, '');
}

// Function to get all movies from localStorage
function getMoviesArray() {
    const movies = localStorage.getItem('movies');
    if (movies) {
        try {
            return JSON.parse(movies);
        } catch (e) {
            console.error('Error parsing movies from localStorage:', e);
            return [];
        }
    }
    return [];
}

// Function to save movies array to localStorage
function saveMoviesArray(movies) {
    localStorage.setItem('movies', JSON.stringify(movies));
}

// Function to initialize default movies in localStorage
function initializeDefaultMovies() {
    const existingMovies = getMoviesArray();
    
    // Only initialize if localStorage is empty
    if (existingMovies.length === 0) {
        const defaultMovies = [
            {
                movieId: 'the-shawshank-redemption',
                title: 'The Shawshank Redemption',
                genre: 'Drama',
                additionalGenres: '',
                releaseYear: 1994,
                director: 'Frank Darabont',
                cast: 'Tim Robbins, Morgan Freeman, Bob Gunton',
                duration: 142,
                rating: 'R',
                imdbRating: 9.3,
                description: 'Two imprisoned men bond over years, finding solace and eventual redemption through acts of common decency. The film captures the essence of hope and humanity in the darkest of times.',
                poster: '../../assets/img/movies/shaw.jpg',
                image: '../../assets/img/movies/shaw.jpg',
                trailer: '',
                language: 'English',
                country: 'USA',
                createdAt: new Date().toISOString()
            },
            {
                movieId: 'the-dark-knight',
                title: 'The Dark Knight',
                genre: 'Action',
                additionalGenres: 'Crime, Drama',
                releaseYear: 2008,
                director: 'Christopher Nolan',
                cast: 'Christian Bale, Heath Ledger, Aaron Eckhart',
                duration: 152,
                rating: 'PG-13',
                imdbRating: 9.0,
                description: 'When the menace known as the Joker causes chaos in Gotham, Batman faces his greatest moral test yet. A psychological thriller that explores the fine line between hero and vigilante.',
                poster: '../../assets/img/movies/R.jpeg',
                image: '../../assets/img/movies/R.jpeg',
                trailer: '',
                language: 'English',
                country: 'USA',
                createdAt: new Date().toISOString()
            },
            {
                movieId: 'the-godfather',
                title: 'The Godfather',
                genre: 'Crime',
                additionalGenres: 'Drama',
                releaseYear: 1972,
                director: 'Francis Ford Coppola',
                cast: 'Marlon Brando, Al Pacino, James Caan',
                duration: 175,
                rating: 'R',
                imdbRating: 9.2,
                description: 'The aging patriarch of an organized crime dynasty transfers control of his empire to his reluctant son. A powerful tale of family, loyalty, and the corrupting influence of power.',
                poster: '../../assets/img/movies/godf.jpg',
                image: '../../assets/img/movies/godf.jpg',
                trailer: '',
                language: 'English',
                country: 'USA',
                createdAt: new Date().toISOString()
            }
        ];
        
        saveMoviesArray(defaultMovies);
        console.log('Default movies initialized in localStorage');
        return true;
    }
    return false;
}

// Function to check if movie ID already exists
function movieIdExists(movieId, currentMovies) {
    return currentMovies.some(movie => {
        const existingId = movie.movieId || movie.id || generateMovieId(movie.title);
        return existingId === movieId;
    });
}

// Function to show success message
function showSuccessMessage(message) {
    // Remove any existing messages
    const existingMsg = document.querySelector('.form-message');
    if (existingMsg) {
        existingMsg.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = 'form-message success';
    messageDiv.style.cssText = 'background-color: #4CAF50; color: white; padding: 1rem; margin: 1rem 0; border-radius: 5px; text-align: center;';
    messageDiv.textContent = message;
    
    const form = document.getElementById('addMovieForm');
    form.insertBefore(messageDiv, form.firstChild);
    
    // Scroll to top to show message
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    // Remove message after 5 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

// Function to show error message
function showErrorMessage(message) {
    // Remove any existing messages
    const existingMsg = document.querySelector('.form-message');
    if (existingMsg) {
        existingMsg.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = 'form-message error';
    messageDiv.style.cssText = 'background-color: #f44336; color: white; padding: 1rem; margin: 1rem 0; border-radius: 5px; text-align: center;';
    messageDiv.textContent = message;
    
    const form = document.getElementById('addMovieForm');
    form.insertBefore(messageDiv, form.firstChild);
    
    // Scroll to top to show message
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    // Remove message after 5 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

// Handle add movie form submission
document.addEventListener('DOMContentLoaded', function() {
    const addMovieForm = document.getElementById('addMovieForm');
    
    if (addMovieForm) {
        addMovieForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form values
            const formData = {
                movieId: document.getElementById('movieId').value.trim(),
                title: document.getElementById('title').value.trim(),
                genre: document.getElementById('genre').value,
                additionalGenres: document.getElementById('additionalGenres').value.trim(),
                releaseYear: document.getElementById('releaseYear').value,
                director: document.getElementById('director').value.trim(),
                cast: document.getElementById('cast').value.trim(),
                duration: document.getElementById('duration').value,
                rating: document.getElementById('rating').value,
                imdbRating: document.getElementById('imdbRating').value,
                description: document.getElementById('description').value.trim(),
                poster: document.getElementById('poster').value.trim(),
                trailer: document.getElementById('trailer').value.trim(),
                language: document.getElementById('language').value.trim(),
                country: document.getElementById('country').value.trim()
            };
            
            // Validate required fields
            if (!formData.title) {
                showErrorMessage('Movie title is required.');
                return;
            }
            
            if (!formData.genre) {
                showErrorMessage('Primary genre is required.');
                return;
            }
            
            if (!formData.releaseYear) {
                showErrorMessage('Release year is required.');
                return;
            }
            
            if (!formData.director) {
                showErrorMessage('Director is required.');
                return;
            }
            
            if (!formData.description || formData.description.length < 20) {
                showErrorMessage('Description is required and must be at least 20 characters.');
                return;
            }
            
            if (!formData.language) {
                showErrorMessage('Language is required.');
                return;
            }
            
            if (!formData.country) {
                showErrorMessage('Country is required.');
                return;
            }
            
            if (!formData.imdbRating || isNaN(formData.imdbRating) || parseFloat(formData.imdbRating) < 0 || parseFloat(formData.imdbRating) > 10) {
                showErrorMessage('IMDb rating is required and must be between 0 and 10.');
                return;
            }
            
            // Get existing movies
            const existingMovies = getMoviesArray();
            
            // Generate movieId from title if not provided or if provided ID doesn't match pattern
            let finalMovieId = formData.movieId;
            if (!finalMovieId || !/^M[0-9]{3,}$/.test(finalMovieId)) {
                // Generate from title instead
                finalMovieId = generateMovieId(formData.title);
            }
            
            // Check if movie ID already exists
            if (movieIdExists(finalMovieId, existingMovies)) {
                showErrorMessage(`A movie with ID "${finalMovieId}" already exists. Please use a different ID or title.`);
                return;
            }
            
            // Check if movie with same title already exists
            const titleExists = existingMovies.some(movie => 
                movie.title.toLowerCase() === formData.title.toLowerCase()
            );
            
            if (titleExists) {
                showErrorMessage(`A movie with the title "${formData.title}" already exists.`);
                return;
            }
            
            // Create movie object
            const newMovie = {
                movieId: finalMovieId,
                title: formData.title,
                genre: formData.genre,
                additionalGenres: formData.additionalGenres || '',
                releaseYear: parseInt(formData.releaseYear),
                director: formData.director,
                cast: formData.cast || '',
                duration: formData.duration ? parseInt(formData.duration) : null,
                rating: formData.rating || '',
                imdbRating: formData.imdbRating ? parseFloat(formData.imdbRating) : null,
                description: formData.description,
                poster: formData.poster || '',
                trailer: formData.trailer || '',
                language: formData.language,
                country: formData.country,
                createdAt: new Date().toISOString()
            };
            
            // Add movie to array
            existingMovies.push(newMovie);
            
            // Save to localStorage
            saveMoviesArray(existingMovies);
            
            // Show success message
            showSuccessMessage(`Movie "${formData.title}" has been added successfully!`);
            
            // Reset form
            addMovieForm.reset();
            
            // Optionally redirect to manage movies page after 2 seconds
            setTimeout(() => {
                if (confirm('Movie added successfully! Would you like to go to Manage Movies page?')) {
                    window.location.href = 'manage_movies.html';
                }
            }, 2000);
        });
    }
});

