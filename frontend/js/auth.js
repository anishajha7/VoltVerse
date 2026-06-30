// auth.js — Login, Register, Logout


function getCurrentUser() {
  const u = localStorage.getItem('ev_user');
  return u ? JSON.parse(u) : null;
}

function logout() {
  localStorage.removeItem('ev_user');
  window.location.href = 'index.html';
}

function updateNavUser() {
  const user = getCurrentUser();
  const navUser = document.getElementById('nav-user');
  const authBtn = document.getElementById('auth-btn');
  if (user) {
    if (navUser) navUser.textContent = 'Hi, ' + user.name.split(' ')[0];
    if (authBtn) authBtn.textContent = 'Logout';
  } else {
    if (navUser) navUser.textContent = '';
    if (authBtn) authBtn.textContent = 'Login';
  }
}
