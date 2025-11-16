const API_BASE = 'http://localhost:8000/api';

const movieForm = document.getElementById('movieForm');
const moviesContainer = document.getElementById('moviesContainer');
const searchInput = document.getElementById('searchInput');
const genreFilter = document.getElementById('genreFilter');
const modal = document.getElementById('movieModal');
const closeBtn = document.querySelector('.close');
const editForm = document.getElementById('editForm');

let allMovies = [];
let currentEditId = null;

document.addEventListener('DOMContentLoaded', () => {
    loadMovies();
    setupEventListeners();
});

function setupEventListeners() {
    movieForm.addEventListener('submit', handleAddMovie);
    searchInput.addEventListener('input', filterMovies);
    genreFilter.addEventListener('change', filterMovies);
    closeBtn.addEventListener('click', closeModal);
    editForm.addEventListener('submit', handleEditMovie);
    window.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
    });
}

async function loadMovies() {
    try {
        const response = await fetch(`${API_BASE}/movies`);
        allMovies = await response.json();
        renderMovies(allMovies);
        updateGenreFilter();
    } catch (error) {
        console.error(error);
        showEmptyState();
    }
}

function renderMovies(movies) {
    if (movies.length === 0) {
        showEmptyState();
        return;
    }

    moviesContainer.innerHTML = movies.map(movie => `
        <div class="movie-card" data-id="${movie.id}">
            <div class="movie-poster">🎬</div>
            <div class="movie-content">
                <h3 class="movie-title">${escapeHtml(movie.title)}</h3>
                <div class="movie-meta">
                    <span class="movie-year">${movie.year}</span>
                    <span class="movie-genre">${escapeHtml(movie.genre)}</span>
                </div>
                <div class="movie-actions">
                    <button class="btn btn-primary" onclick="editMovie(${movie.id})">✏️ Редактирай</button>
                    <button class="btn btn-danger" onclick="deleteMovie(${movie.id})">🗑️ Изтрий</button>
                </div>
            </div>
        </div>
    `).join('');
}

function showEmptyState() {
    moviesContainer.innerHTML = `
        <div class="empty-state">
            <div class="empty-state-icon">📽️</div>
            <p class="empty-state-text">Няма филми. Добави първия си!</p>
        </div>
    `;
}

async function handleAddMovie(e) {
    e.preventDefault();

    const movie = {
        title: document.getElementById('title').value,
        year: parseInt(document.getElementById('year').value),
        genre: document.getElementById('genre').value
    };

    try {
        const response = await fetch(`${API_BASE}/movies`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(movie)
        });

        const newMovie = await response.json();
        allMovies.push(newMovie);
        renderMovies(allMovies);
        updateGenreFilter();
        movieForm.reset();
        alert('Филмът е добавен!');
    } catch (error) {
        alert('Грешка при добавяне!');
    }
}

function filterMovies() {
    const searchTerm = searchInput.value.toLowerCase();
    const selectedGenre = genreFilter.value;

    const filtered = allMovies.filter(movie => {
        const titleMatch = movie.title.toLowerCase().includes(searchTerm);
        const genreMatch = !selectedGenre || movie.genre === selectedGenre;
        return titleMatch && genreMatch;
    });

    renderMovies(filtered);
}

function updateGenreFilter() {
    const genres = [...new Set(allMovies.map(m => m.genre))];
    const currentValue = genreFilter.value;
    
    genreFilter.innerHTML = '<option value="">Всички жанрове</option>' +
        genres.map(g => `<option value="${g}">${g}</option>`).join('');
    
    genreFilter.value = currentValue;
}

function editMovie(id) {
    const movie = allMovies.find(m => m.id === id);
    if (!movie) return;

    currentEditId = id;
    document.getElementById('editTitle').value = movie.title;
    document.getElementById('editYear').value = movie.year;
    document.getElementById('editGenre').value = movie.genre;

    openModal();
}

async function handleEditMovie(e) {
    e.preventDefault();

    const updatedMovie = {
        title: document.getElementById('editTitle').value,
        year: parseInt(document.getElementById('editYear').value),
        genre: document.getElementById('editGenre').value
    };

    try {
        const response = await fetch(`${API_BASE}/movies/${currentEditId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updatedMovie)
        });

        const movieIndex = allMovies.findIndex(m => m.id === currentEditId);
        if (movieIndex !== -1) {
            allMovies[movieIndex] = { ...allMovies[movieIndex], ...updatedMovie };
        }

        renderMovies(allMovies);
        updateGenreFilter();
        closeModal();
        alert('Филмът е обновен!');
    } catch (error) {
        alert('Грешка при обновяване!');
    }
}

async function deleteMovie(id) {
    if (!confirm('Сигурна ли си?')) return;

    try {
        const response = await fetch(`${API_BASE}/movies/${id}`, {
            method: 'DELETE'
        });

        allMovies = allMovies.filter(m => m.id !== id);
        renderMovies(allMovies);
        updateGenreFilter();
        alert('Филмът е изтрит!');
    } catch (error) {
        alert('Грешка при изтриване!');
    }
}

function openModal() {
    modal.classList.add('show');
}

function closeModal() {
    modal.classList.remove('show');
    currentEditId = null;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
