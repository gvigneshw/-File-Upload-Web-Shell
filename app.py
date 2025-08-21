import os
from flask import Flask, request, render_template_string, send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = "/tmp"  # writable temporary space on Vercel

FLAG = "ctf{basic_python_shell_upload_challenge}"

# Write the flag file at startup
try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
except:
    pass

flag_path = os.path.join(UPLOAD_FOLDER, "flag.txt")
with open(flag_path, "w") as f:
    f.write(FLAG)

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

# Do NOT call app.run() when deploying serverlessly

# Export app to be used by Vercel
