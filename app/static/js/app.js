// ConectaTalentos — frontend helpers

// Auto-dismiss alerts after 5s
document.querySelectorAll('.alert').forEach(el => {
    setTimeout(() => el.classList.remove('show'), 5000);
});
