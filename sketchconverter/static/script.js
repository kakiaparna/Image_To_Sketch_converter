document.addEventListener('DOMContentLoaded', function() {
    // Update file name display when a file is selected
    const fileInput = document.getElementById('file');
    const fileNameDisplay = document.getElementById('file-name');
    const filePreview = document.getElementById('filePreview');
    
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                fileNameDisplay.textContent = this.files[0].name;

                // Clear previous preview
                filePreview.innerHTML = '';

                // Create image element for preview
                const img = document.createElement('img');
                img.src = URL.createObjectURL(this.files[0]);
                img.alt = 'Selected Image Preview';
                img.style.maxWidth = '100%';
                img.style.maxHeight = '200px';
                img.onload = function() {
                    URL.revokeObjectURL(this.src); // Free memory
                }

                filePreview.appendChild(img);
            } else {
                fileNameDisplay.textContent = 'No file chosen';
                filePreview.innerHTML = '';
            }
        });
    }
    
    // Add drag and drop functionality
    const dropSection = document.querySelector('.drop-section');
    if (dropSection) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropSection.addEventListener(eventName, preventDefaults, false);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        ['dragenter', 'dragover'].forEach(eventName => {
            dropSection.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            dropSection.addEventListener(eventName, unhighlight, false);
        });
        
        function highlight() {
            dropSection.classList.add('highlight');
        }
        
        function unhighlight() {
            dropSection.classList.remove('highlight');
        }
        
        dropSection.addEventListener('drop', handleDrop, false);
        
        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            
            if (files && files.length) {
                fileInput.files = files;
                fileNameDisplay.textContent = files[0].name;

                // Clear previous preview
                filePreview.innerHTML = '';

                // Create image element for preview
                const img = document.createElement('img');
                img.src = URL.createObjectURL(files[0]);
                img.alt = 'Selected Image Preview';
                img.style.maxWidth = '100%';
                img.style.maxHeight = '200px';
                img.onload = function() {
                    URL.revokeObjectURL(this.src); // Free memory
                }

                filePreview.appendChild(img);
            }
        }
    }
});
