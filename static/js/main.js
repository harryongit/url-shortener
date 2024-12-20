// static/js/main.js
class URLShortener {
    constructor() {
        this.baseURL = window.location.origin;
        this.setupEventListeners();
    }

    setupEventListeners() {
        const shortenButton = document.getElementById('shortenButton');
        const urlInput = document.getElementById('urlInput');
        const copyButtons = document.querySelectorAll('.copy-btn');

        if (shortenButton) {
            shortenButton.addEventListener('click', () => this.shortenURL());
        }

        if (urlInput) {
            urlInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.shortenURL();
                }
            });
        }

        copyButtons.forEach(button => {
            button.addEventListener('click', (e) => this.copyToClipboard(e.target));
        });
    }

    async shortenURL() {
        const urlInput = document.getElementById('urlInput');
        const resultDiv = document.getElementById('result');
        const shortUrlInput = document.getElementById('shortUrl');
        const alertDiv = document.getElementById('alert');

        if (!urlInput.value) {
            this.showAlert('Please enter a URL', 'error');
            return;
        }

        try {
            const response = await fetch('/api/shorten', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: urlInput.value }),
            });

            const data = await response.json();
            
            if (response.ok) {
                const shortUrl = `${this.baseURL}/${data.short_code}`;
                shortUrlInput.value = shortUrl;
                resultDiv.classList.remove('hidden');
                resultDiv.classList.add('fade-in');
                this.showAlert('URL shortened successfully!', 'success');
                this.updateRecentURLs(data);
            } else {
                this.showAlert(data.error || 'An error occurred', 'error');
            }
        } catch (error) {
            this.showAlert('An error occurred while shortening the URL', 'error');
            console.error('Error:', error);
        }
    }

    copyToClipboard(button) {
        const input = document.getElementById('shortUrl');
        if (!input) return;

        input.select();
        document.execCommand('copy');

        // Update button text temporarily
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        button.classList.add('btn-success');

        setTimeout(() => {
            button.textContent = originalText;
            button.classList.remove('btn-success');
        }, 2000);

        this.showAlert('Copied to clipboard!', 'success');
    }

    showAlert(message, type) {
        const alertDiv = document.getElementById('alert');
        if (!alertDiv) return;

        alertDiv.textContent = message;
        alertDiv.className = `alert alert-${type} fade-in`;
        alertDiv.style.display = 'block';

        setTimeout(() => {
            alertDiv.style.display = 'none';
        }, 3000);
    }

    updateRecentURLs(newUrl) {
        const tableBody = document.querySelector('.table tbody');
        if (!tableBody) return;

        const row = document.createElement('tr');
        row.classList.add('fade-in');
        
        row.innerHTML = `
            <td class="truncate">${newUrl.original_url}</td>
            <td>
                <a href="/${newUrl.short_code}" target="_blank" class="text-primary hover:text-primary-dark">
                    ${newUrl.short_code}
                </a>
            </td>
            <td>${newUrl.clicks}</td>
            <td>${newUrl.created_at}</td>
        `;

        tableBody.insertBefore(row, tableBody.firstChild);
        
        // Remove last row if more than 10 rows
        if (tableBody.children.length > 10) {
            tableBody.removeChild(tableBody.lastChild);
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new URLShortener();
});
