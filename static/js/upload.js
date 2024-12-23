// Open the upload popup for the selected event
function openUploadPopup(eventId) {
    // Set the action URL dynamically for the form
    const form = document.querySelector(`#upload-popup form`);
    form.action = `/upload_images/${eventId}`;
    // form.action = "/upload_images/" + eventId; 

    // Display the popup
    const popup = document.getElementById('upload-popup');
    popup.style.display = 'block';
}

// Close the upload popup
function closePopup() {
    const popup = document.getElementById('upload-popup');
    popup.style.display = 'none';
}

// Close the popup when the user clicks anywhere outside of it
window.onclick = function(event) {
    const popup = document.getElementById('upload-popup');
    if (event.target === popup) {
        closePopup();
    }
}
