import io
import sys
from flask import Flask, request, render_template_string

app = Flask(__name__)
FLAG = "ctf{basic_python_shell_upload_challenge}"

@app.route('/', methods=['GET', 'POST'])
def upload_and_execute():
    output = None
    error = None
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename:
            code = file.read().decode()
            try:
                # Redirect stdout to capture print output
                old_stdout = sys.stdout
                sys.stdout = io.StringIO()
                
                # Provide flag variable in exec environment
                exec_globals = {'open': open, 'FLAG': FLAG}
                exec(code, exec_globals)
                
                output = sys.stdout.getvalue()
            except Exception as e:
                error = str(e)
            finally:
                sys.stdout = old_stdout

    return render_template_string('''
    <h2>Upload your Python script</h2>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file"/>
        <input type="submit" value="Run"/>
    </form>
    {% if output %}
        <h3>Output:</h3>
        <pre>{{ output }}</pre>
    {% endif %}
    {% if error %}
        <h3>Error:</h3>
        <pre>{{ error }}</pre>
    {% endif %}
    <p>Hint: Your script can read the flag variable <code>FLAG</code> or the file <code>/tmp/flag.txt</code></p>
    ''', output=output, error=error)

if __name__ == '__main__':
    app.run()
