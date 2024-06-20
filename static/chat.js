document.addEventListener("DOMContentLoaded", function() {
    const textarea = document.getElementById('autoresizing');
    const inputarea = document.getElementById('input');

    textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
});