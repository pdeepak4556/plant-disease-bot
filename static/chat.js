document.addEventListener("DOMContentLoaded", function() {
    const textarea = document.getElementById('autoresizing');

    textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
});