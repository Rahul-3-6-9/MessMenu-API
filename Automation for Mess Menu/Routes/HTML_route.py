from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Menu File Processor</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 600px; margin: auto; }
        .drop-zone { border: 2px dashed #ccc; padding: 20px; text-align: center; }
        .drop-zone.dragover { background-color: #e1e1e1; }
        button { margin-top: 10px; padding: 10px 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Upload Menu Files</h1>
        <form id="uploadForm" enctype="multipart/form-data">
            <label for="file_type">File Type:</label>
            <select name="file_type" id="file_type">
                <option value="pdf">PDF</option>
                <option value="excel">Excel</option>
                <option value="gsheet">Google Sheet (as Excel)</option>
            </select><br><br>
            <label>Upload Files (select multiple or drag and drop):</label><br>
            <div class="drop-zone" id="dropZone">Drag files here or click to select</div>
            <input type="file" id="files" name="files" multiple accept=".pdf,.xlsx,.xls" style="display: none;">
            <br>
            <button type="submit">Process Files</button>
        </form>
        <div id="response"></div>
    </div>
    <script>
        const fileTypeSelect = document.getElementById('file_type');
        const dropZone = document.getElementById('dropZone');
        const fileInput = document.getElementById('files');
        const form = document.getElementById('uploadForm');
        const responseDiv = document.getElementById('response');

        dropZone.addEventListener('click', () => fileInput.click());
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        });
        dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
            fileInput.files = e.dataTransfer.files;
            dropZone.textContent = `${fileInput.files.length} file(s) selected`;
        });
        fileInput.addEventListener('change', () => {
            dropZone.textContent = `${fileInput.files.length} file(s) selected`;
        });

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            if (fileInput.files.length === 0) {
                responseDiv.textContent = 'Error: At least one file is required';
                return;
            }

            const formData = new FormData();
            formData.append('file_type', fileTypeSelect.value);
            for (const file of fileInput.files) {
                formData.append('files', file);
            }

            responseDiv.textContent = 'Processing...';
            try {
                const response = await fetch('/process', {
                    method: 'POST',
                    body: formData
                });
                if (!response.ok) {
                    const errorData = await response.json();
                    responseDiv.textContent = `Error: ${errorData.error || errorData.detail}`;
                    return;
                }
                const result = await response.json();
                responseDiv.innerHTML = `<pre>${JSON.stringify(result, null, 2)}</pre>`;
            } catch (error) {
                responseDiv.textContent = `Error: ${error.message}`;
            }
        });
    </script>
</body>
</html>
"""

@router.get("/", response_class=HTMLResponse)
async def get_upload_form():
    return HTML_FORM