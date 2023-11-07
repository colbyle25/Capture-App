document.addEventListener('DOMContentLoaded', function () {
    var selectionButtons = document.querySelectorAll('.select-button');

    selectionButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            var category = this.getAttribute('data-category');
            document.querySelectorAll(`.select-button[data-category="${category}"]`).forEach(btn => {
                btn.classList.remove('selected');
            });

            this.classList.add('selected');

            var itemId = this.getAttribute('data-item-id');
            fetch(`/apply/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': CSRF_TOKEN
                },
                body: JSON.stringify({
                    'item_id': itemId,
                    'category': category
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                } else {
                    this.classList.remove('selected');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                this.classList.remove('selected');
            });
        });
    });
});
