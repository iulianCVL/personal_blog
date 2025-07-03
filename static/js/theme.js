const icon = document.getElementById('themeIcon');

if (localStorage.getItem('theme') === 'light') {
  body.classList.add('light-mode');
  icon.textContent = '🌙';
} else {
  icon.textContent = '☀️';
}

toggleBtn.addEventListener('click', function () {
  body.classList.toggle('light-mode');
  const isLight = body.classList.contains('light-mode');
  icon.textContent = isLight ? '🌙' : '☀️';
  localStorage.setItem('theme', isLight ? 'light' : 'dark');
});
