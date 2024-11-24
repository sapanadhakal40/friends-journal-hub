

const menuBtn = document.getElementById('menu-btn');
const mobileMenu = document.getElementById('mobile-menu');

menuBtn.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
}
);
function updateDateTime() {
    const now = new Date();
    const clock = document.getElementById('clock');
    const date = document.getElementById('date');

    if (clock && date) {

        clock.textContent = now.toLocaleTimeString();
        date.textContent = now.toLocaleDateString('en-US', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }
}

// Initialize clock and update every second
updateDateTime();
setInterval(updateDateTime, 1000);

// Dismiss flash messages with animation
function dismissMessage(button) {
    const message = button.closest('.flash-message');
    if (message) {
        message.style.opacity = '0';
        message.style.transform = 'translateX(100%)';
        setTimeout(() => message.remove(), 300);
    }
}

// Delete milestone function (you'll need to implement the backend route)
function deleteMilestone(id) {
    if (confirm('Are you sure you want to delete this milestone?')) {
        fetch(`/milestone/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert('Error deleting milestone');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error deleting milestone');
            });
    }
}


// Add hover effect to milestone cards
document.querySelectorAll('.milestone-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.classList.add('scale-105', 'shadow-lg');
    });

    card.addEventListener('mouseleave', () => {
        card.classList.remove('scale-105', 'shadow-lg');
    });
});


function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {

        sidebar.classList.toggle('-translate-x-full');
    }
}
