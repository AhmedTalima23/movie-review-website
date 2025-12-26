// Function to get CSRF token from cookies
function getCSRFToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to show success message
function showSuccessMessage(message) {
    // Remove any existing messages
    const existingMessages = document.querySelectorAll('.message');
    existingMessages.forEach(msg => msg.remove());

    // Create and show success message
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message success';
    messageDiv.innerHTML = `
        <div class="message-content">
            <span class="message-icon">✓</span>
            <span class="message-text">${message}</span>
            <span class="message-close" onclick="this.parentElement.parentElement.remove()">×</span>
        </div>
    `;

    document.body.appendChild(messageDiv);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (messageDiv.parentElement) {
            messageDiv.remove();
        }
    }, 5000);
}

// Function to show error message
function showErrorMessage(message) {
    // Remove any existing messages
    const existingMessages = document.querySelectorAll('.message');
    existingMessages.forEach(msg => msg.remove());

    // Create and show error message
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message error';
    messageDiv.innerHTML = `
        <div class="message-content">
            <span class="message-icon">✕</span>
            <span class="message-text">${message}</span>
            <span class="message-close" onclick="this.parentElement.parentElement.remove()">×</span>
        </div>
    `;

    document.body.appendChild(messageDiv);

    // Scroll to top to show message
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Remove message after 5 seconds
    setTimeout(() => {
        if (messageDiv.parentElement) {
            messageDiv.remove();
        }
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

            // Show loading state
            const submitButton = addMovieForm.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            submitButton.textContent = 'Adding Movie...';
            submitButton.disabled = true;

            // Send AJAX request to Django backend
            fetch('/add_movie/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showSuccessMessage(data.message);
                    addMovieForm.reset();

                    // Optionally redirect after 2 seconds
                    setTimeout(() => {
                        if (confirm('Movie added successfully! Would you like to add another movie?')) {
                            // Stay on page
                        } else {
                            // Could redirect to manage movies if that view exists
                            // window.location.href = '/manage_movies/';
                        }
                    }, 2000);
                } else {
                    showErrorMessage(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showErrorMessage('An error occurred while adding the movie. Please try again.');
            })
            .finally(() => {
                // Reset button state
                submitButton.textContent = originalText;
                submitButton.disabled = false;
            });
        });
    }
});

// Handle add movie form submission
document.addEventListener('DOMContentLoaded', function() {
    const addMovieForm = document.getElementById('addMovieForm');
    
    if (addMovieForm) {
        addMovieForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form values
            const formData = {
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
            
            // Show loading state
            const submitButton = addMovieForm.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            submitButton.textContent = 'Adding Movie...';
            submitButton.disabled = true;
            
            // Send AJAX request to Django backend
            fetch('/add_movie/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showSuccessMessage(data.message);
                    addMovieForm.reset();
                    
                    // Optionally redirect after 2 seconds
                    setTimeout(() => {
                        if (confirm('Movie added successfully! Would you like to add another movie?')) {
                            // Stay on page
                        } else {
                            // Could redirect to manage movies if that view exists
                            // window.location.href = '/manage_movies/';
                        }
                    }, 2000);
                } else {
                    showErrorMessage(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showErrorMessage('An error occurred while adding the movie. Please try again.');
            })
            .finally(() => {
                // Reset button state
                submitButton.textContent = originalText;
                submitButton.disabled = false;
            });
        });
    }
});

