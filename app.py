import os
from flask import Flask, request, render_template_string, send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = "/tmp"  # Use /tmp for writable space on Vercel

FLAG = "ctf{basic_python_shell_upload_challenge}"

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    message = ''
    if request.method == 'POST':
        if 'file' not in request.files:
            message = "No file part"
        else:
            file = request.files['file']
            if file.filename == '':
                message = "No selected file"
            else:
                filename = file.filename
                save_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(save_path)
                message = f"File uploaded: {filename}"
    return render_template_string('''
    <h2>Upload your file</h2>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file"/>
        <input type="submit" value="Upload"/>
    </form>
    <p>{{ message }}</p>
    <p>Hint: Upload a Python script that reads the flag from <code>/tmp/flag.txt</code> and execute it.</p>
    ''', message=message)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.before_first_request
def write_flag():
    with open("/tmp/flag.txt", "w") as f:
        f.write(FLAG)

if __name__ == "__main__":
    app.run()
