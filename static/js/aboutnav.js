function showMenu(category) {
    const categories = ['processor', 'vga', 'ram', 'motherboard', 'ssd', 'powersupply'];
    categories.forEach(cat => {
        const element = document.getElementById(cat);
        if (element) {
            element.style.display = 'none';
            document.querySelector(`.menu-tab[data-tab="${cat}"]`).classList.remove('selected');
        }
    });
    const selectedElement = document.getElementById(category);
    if (selectedElement) {
        selectedElement.style.display = 'block';
        document.querySelector(`.menu-tab[data-tab="${category}"]`).classList.add('selected');
    }
}

// Tampilkan kategori pertama secara default
document.addEventListener("DOMContentLoaded", function() {
    showMenu('processor');
});
