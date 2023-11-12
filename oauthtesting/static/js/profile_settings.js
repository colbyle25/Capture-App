document.addEventListener('DOMContentLoaded', function () {
    var applyButton = document.getElementById('apply-button');
    var selectionButtons = document.querySelectorAll('.select-button');

    selectionButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            var category = this.getAttribute('data-category');
            document.querySelectorAll(`.select-button[data-category="${category}"]`).forEach(btn => {
                btn.parentElement.classList.remove('selected');
                btn.classList.remove('selected');
                btn.disabled = false;
            });

            this.classList.add('selected');
            this.parentElement.classList.add('selected');
            this.disabled = true;
        });
    });

    applyButton.addEventListener('click', function() {
        var selected_items = {};
        selectionButtons.forEach(function (button) {
            if (button.classList.contains('selected')) {
                var category = button.getAttribute('data-category');
                var itemId = button.getAttribute('data-item-id');
                selected_items[category] = itemId;
            }
        });

        fetch(`/profile/settings/apply/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRF_TOKEN
            },
            body: JSON.stringify(selected_items)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // https://stackoverflow.com/questions/61929987/redirect-django-url-with-javascript
                window.location.href = '/profile/settings/'
            } else {
                console.error('Error applying selections: ', data)
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    })
});
