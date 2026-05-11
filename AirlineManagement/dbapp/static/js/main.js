/**
 * BOUNDLESS AIR - Premium Unified JavaScript
 * Handles Global UI/UX Interactions
 */

console.log("✈️ Boundless Air Systems: Operational");

// 1. Password Visibility Toggle (Enhanced)
// Used in Login & Registration pages
function togglePassword(inputId, iconId) {
    const pInput = document.getElementById(inputId);
    const icon = document.getElementById(iconId);
    
    if (pInput && icon) {
        const isPassword = pInput.type === "password";
        pInput.type = isPassword ? "text" : "password";
        
        // Toggle Bootstrap Icons
        if (isPassword) {
            icon.classList.remove("bi-eye");
            icon.classList.add("bi-eye-slash");
        } else {
            icon.classList.remove("bi-eye-slash");
            icon.classList.add("bi-eye");
        }
    }
}

// 2. City Swap Logic (Dashboard & Search)
// Swaps the values of "From" and "To" selects
function swapCities() {
    const srcSelect = document.getElementById('src');
    const dstSelect = document.getElementById('dst');
    const swapBtn = document.querySelector('.swap-btn');

    if (srcSelect && dstSelect) {
        // Swap values
        const temp = srcSelect.value;
        srcSelect.value = dstSelect.value;
        dstSelect.value = temp;

        // Visual feedback: Rotate the button
        if (swapBtn) {
            const currentRotation = swapBtn.style.transform === 'rotate(180deg)' ? '0deg' : '180deg';
            swapBtn.style.transform = `rotate(${currentRotation})`;
        }
    }
}

// 3. Initialize UI Components on Load
document.addEventListener('DOMContentLoaded', function() {
    
    // A. Auto-hide Flash Messages (Alerts)
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            // Check if element still exists before trying to close
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    });

    // B. Initialize Bootstrap Tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // C. Source/Destination Validation
    // Prevents user from searching for a flight to the same city
    const searchForms = document.querySelectorAll('form[action*="search"]');
    searchForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const src = form.querySelector('[name="source"]').value;
            const dst = form.querySelector('[name="dest"]').value;
            
            if (src === dst && src !== "") {
                e.preventDefault();
                alert("Destination cannot be the same as Origin. Please select a different city.");
            }
        });
    });

    // D. Navbar Scroll Effect
    // Adds a shadow and changes opacity when user scrolls down
    window.addEventListener('scroll', function() {
        const nav = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            nav.classList.add('shadow-lg');
            nav.style.opacity = "0.98";
        } else {
            nav.classList.remove('shadow-lg');
            nav.style.opacity = "1";
        }
    });
});

// 4. Booking Step Helpers
// Used to format currency dynamically in JS if needed
const formatINR = (amount) => {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        maximumFractionDigits: 0
    }).format(amount);
};