document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.wishlist-btn').forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            
            let itemId = this.dataset.itemId;
            let icon = this.querySelector("i");
            
            fetch(`/toggle-wishlist/${itemId}`, {
                method: "POST",
                headers: { "X-Requested-With": "XMLHttpRequest" }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "added") {
                    icon.classList.remove("far", "text-muted");
                    icon.classList.add("fas", "text-danger");
                } else if (data.status === "removed") {
                    icon.classList.remove("fas", "text-danger");
                    icon.classList.add("far", "text-muted");
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });
});
