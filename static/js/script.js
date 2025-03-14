document.getElementById("uploadForm").addEventListener("submit", function(event) {
	    event.preventDefault();
	    let formData = new FormData();
	    let fileInput = document.getElementById("imageInput").files[0];
	    let quality = document.getElementById("quality").value;
	    let format = document.getElementById("format").value;

	    if (!fileInput) {
		            alert("Please select an image.");
		            return;
		        }

	    formData.append("image", fileInput);
	    formData.append("quality", quality);
	    formData.append("format", format);

	    fetch("/upload", {
		            method: "POST",
		            body: formData
		        })
	    .then(response => response.blob())
	    .then(blob => {
		            let url = URL.createObjectURL(blob);
		            let downloadLink = document.getElementById("downloadLink");
		            downloadLink.href = url;
		            downloadLink.style.display = "block";
		        })
	    .catch(error => console.error("Error:", error));
});

