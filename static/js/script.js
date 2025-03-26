// compression app js codes 
document.addEventListener("DOMContentLoaded", function () {
    console.log("Website Loaded Successfully!");

    // Single Image Compression with no quality loss
    document.getElementById("singleUploadForm")?.addEventListener("submit", function (e) {
        e.preventDefault();
        const formData = new FormData();
        formData.append("image", document.getElementById("singleImage").files[0]);

        fetch("/compress/single", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById("downloadSingle").href = data.url;
                document.getElementById("singleResult").classList.remove("hidden");
            }
        })
        .catch(error => console.error("Error:", error));
    });

    document.addEventListener("DOMContentLoaded", function () {
    const dropdown = document.querySelector(".dropdown");

    dropdown.addEventListener("mouseover", function () {
        this.querySelector(".dropdown-menu").style.display = "block";
    });

    dropdown.addEventListener("mouseleave", function () {
        this.querySelector(".dropdown-menu").style.display = "none";
    });
});


    // Multiple Images Compression with no quality loss
    document.getElementById("multiUploadForm")?.addEventListener("submit", function (e) {
        e.preventDefault();
        const formData = new FormData();
        const files = document.getElementById("multiImages").files;
        for (let i = 0; i < files.length; i++) {
            formData.append("images", files[i]);
        }

        fetch("/compress/multiple", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById("downloadMulti").href = data.url;
                document.getElementById("multiResult").classList.remove("hidden");
            }
        })
        .catch(error => console.error("Error:", error));
    });

    // Video Compression
    document.getElementById("videoUploadForm")?.addEventListener("submit", function (e) {
        e.preventDefault();
        const formData = new FormData();
        formData.append("video", document.getElementById("videoFile").files[0]);

        fetch("/compress/video", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById("downloadVideo").href = data.url;
                document.getElementById("videoResult").classList.remove("hidden");
            }
        })
        .catch(error => console.error("Error:", error));
    });
});
<script>
document.addEventListener("DOMContentLoaded", function () {
    const cards = document.querySelectorAll(".about-card");

    function revealOnScroll() {
        cards.forEach(card => {
            const rect = card.getBoundingClientRect();
            if (rect.top < window.innerHeight * 0.9) {
                card.classList.add("fade-in");
            }
        });
    }

    window.addEventListener("scroll", revealOnScroll);
    revealOnScroll(); // Run on page load
});
</script>


