document.addEventListener('DOMContentLoaded', function () {
    var purchaseButtons = document.querySelectorAll('.purchase-button');

    purchaseButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            var itemId = this.getAttribute('data-item-id');
            button.disabled = true;

            fetch(`/purchase/${itemId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': CSRF_TOKEN
                },
                body: JSON.stringify({ 'item_id': itemId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // document.getElementById('points-display').textContent = `Current Points: ${data.new_points_total}`;
                    // button.textContent = 'Item Owned';
                    document.location.reload();
                } else {
                    button.disabled = false; 
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                button.disabled = false; 
            });
        });
    });
});