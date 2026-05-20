// Gym Management System Front-end Utilities

document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Mobile Sidebar Toggle Drawer
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function(e) {
            e.preventDefault();
            sidebar.classList.toggle('show');
        });
        
        // Close sidebar when clicking outside on mobile screens
        document.addEventListener('click', function(event) {
            const isClickInside = sidebar.contains(event.target) || sidebarToggle.contains(event.target);
            if (!isClickInside && sidebar.classList.contains('show')) {
                sidebar.classList.remove('show');
            }
        });
    }

    // 2. Automagic Flash Alert Dismissals
    const flashAlerts = document.querySelectorAll('.alert-dismissible');
    flashAlerts.forEach(function(alert) {
        setTimeout(function() {
            // Using Bootstrap's built-in transition fade
            alert.classList.add('fade');
            setTimeout(function() {
                alert.remove();
            }, 300); // Wait for transition to finish
        }, 4000); // Trigger auto-hide after 4 seconds
    });

    // 3. Live Image Upload Profile Photo Previews
    const photoInput = document.querySelector('input[type="file"]');
    const photoPreview = document.getElementById('uploadPreview');
    
    if (photoInput && photoPreview) {
        photoInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                // Ensure it is an image
                if (file.type.match('image.*')) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        photoPreview.src = e.target.result;
                        photoPreview.classList.add('glow-active');
                    };
                    reader.readAsDataURL(file);
                } else {
                    alert('Please select an image file (PNG, JPG, JPEG, GIF, WEBP).');
                    this.value = '';
                }
            }
        });
    }

    // 4. Unified Delete Confirmation Modal Handler
    const confirmDeleteModal = document.getElementById('confirmDeleteModal');
    if (confirmDeleteModal) {
        confirmDeleteModal.addEventListener('show.bs.modal', function(event) {
            // Button that triggered the modal
            const button = event.relatedTarget;
            // Extract attributes from button
            const deleteUrl = button.getAttribute('data-action');
            const itemName = button.getAttribute('data-name');
            
            // Update modal text content
            const modalBodySpan = confirmDeleteModal.querySelector('#deleteItemName');
            if (modalBodySpan && itemName) {
                modalBodySpan.textContent = itemName;
            }
            
            // Set form submission action
            const deleteForm = confirmDeleteModal.querySelector('#deleteForm');
            if (deleteForm && deleteUrl) {
                deleteForm.setAttribute('action', deleteUrl);
            }
        });
    }
});
