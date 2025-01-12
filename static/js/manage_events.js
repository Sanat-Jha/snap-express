document.addEventListener('DOMContentLoaded', function() {
    const currenteventdropdown = document.getElementById('current-event');

    currenteventdropdown.addEventListener('change', function() {
        const selectedValue = currenteventdropdown.value;

        fetch('/change_current_event', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ event: selectedValue })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Event changed successfully!');
            } else {
                alert('Failed to change event.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while changing the event.');
        });
    });

    const imageGalleryDropdown = document.getElementById('image-gallery');

    imageGalleryDropdown.addEventListener('change', function() {
        const selectedValue = imageGalleryDropdown.value;

        fetch('/fetch_event_images', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ event: selectedValue })
        })
        .then(response => response.json())
        .then(data => {
            const grid = document.getElementsByClassName('grid')[0];
            grid.innerHTML = '';
// Update this part in your existing JavaScript
data.images.forEach(imageurl => {
    const gridItem = document.createElement('div');
    gridItem.className = 'grid-item';
    
    const img = document.createElement('img');
    img.src = imageurl;
    
    gridItem.appendChild(img);
    gridItem.addEventListener('click', () => {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/result';

        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'image_url';
        input.value = imageurl;
        form.appendChild(input);

        document.body.appendChild(form);
        form.submit();
    });

    grid.appendChild(gridItem);
});

        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while changing the image gallery.');
        });
            });
});