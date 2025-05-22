document.addEventListener('DOMContentLoaded', () => {
    const themeToggleButton = document.getElementById('theme-toggle-button');
    const currentTheme = localStorage.getItem('theme') || 'light'; // Default to light

    // Apply the stored theme on initial load
    if (currentTheme === 'dark') {
        document.body.classList.add('dark-mode');
        if (themeToggleButton) themeToggleButton.textContent = 'Light Mode';
        // For Bootstrap 5.3+ data attribute theming
        document.documentElement.setAttribute('data-bs-theme', 'dark');
    } else {
        if (themeToggleButton) themeToggleButton.textContent = 'Dark Mode';
        document.documentElement.setAttribute('data-bs-theme', 'light');
    }

    if (themeToggleButton) {
        themeToggleButton.addEventListener('click', () => {
            let theme;
            if (document.body.classList.contains('dark-mode')) {
                document.body.classList.remove('dark-mode');
                if (themeToggleButton) themeToggleButton.textContent = 'Dark Mode';
                localStorage.setItem('theme', 'light');
                theme = 'light';
                document.documentElement.setAttribute('data-bs-theme', 'light');
            } else {
                document.body.classList.add('dark-mode');
                if (themeToggleButton) themeToggleButton.textContent = 'Light Mode';
                localStorage.setItem('theme', 'dark');
                theme = 'dark';
                document.documentElement.setAttribute('data-bs-theme', 'dark');
            }

            // Optional: AJAX call to save theme preference to backend
            // This is a basic example; you'd need a URL and view to handle this.
            // fetch('/users/update-theme/', { // Replace with your actual URL
            //     method: 'POST',
            //     headers: {
            //         'Content-Type': 'application/json',
            //         'X-CSRFToken': getCookie('csrftoken') // Function to get CSRF token
            //     },
            //     body: JSON.stringify({ theme: theme })
            // }).then(response => response.json())
            //   .then(data => console.log('Theme preference saved:', data))
            //   .catch(error => console.error('Error saving theme preference:', error));
        });
    }
});

// Function to get CSRF token (if making AJAX calls to Django POST views)
// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
