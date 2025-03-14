document.addEventListener("DOMContentLoaded", function () {
    console.log("Website Loaded Successfully!");

    // Single Image Compression
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

    // Multiple Images Compression
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
