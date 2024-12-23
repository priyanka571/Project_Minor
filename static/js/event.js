function openCreateEventPopup() {
    document.getElementById('create-event-popup').style.display = 'block';
}

function closePopup(popupId) {
    document.getElementById(popupId + '-popup').style.display = 'none';
}




// this is designing part
// Open the Create Event Popup
function openCreateEventPopup() {
    const popup = document.getElementById('create-event-popup');
    popup.style.display = 'block';
}

// Close the Create Event Popup
function closePopup(popupId) {
    const popup = document.getElementById(`${popupId}-popup`);
    popup.style.display = 'none';
}

// Close popup when clicking outside of it
window.onclick = function(event) {
    const popup = document.getElementById('create-event-popup');
    if (event.target === popup) {
        popup.style.display = 'none';
    }
};

