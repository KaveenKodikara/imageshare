function uploadImage() {
    const input = document.getElementById('imageInput');
    const file = input.files[0];

    if (file) {
        const formData = new FormData();
        formData.append('image', file);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                alert('Image uploaded successfully!');
            } else {
                alert('Error uploading image.');
            }
        })
        .catch(error => console.error('Error:', error));
    } else {
        alert('Please select an image to upload.');
    }
}
