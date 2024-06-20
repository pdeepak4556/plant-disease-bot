function setFontSize() {
    const navbar = document.getElementById('navbar');
    const navbarHeight = navbar.offsetHeight;

    const logoText = document.getElementById('logo-text');
    const shortlogoText = document.getElementById('short-logo');
    const logo = document.getElementById('logo');
    const button1 = document.getElementById('button1');
    const button2 = document.getElementById('button2');

    logoText.style.fontSize = `${navbarHeight * 0.5}px`;
    shortlogoText.style.fontSize = `${navbarHeight * 0.5}px`;

    logo.style.paddingLeft = `${navbarHeight * 0.3}px`;
    shortlogoText.style.paddingLeft = `${navbarHeight * 0.3}px`;
}
setFontSize();

window.addEventListener('resize', setFontSize);