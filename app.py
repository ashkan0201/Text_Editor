from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from datetime import datetime
import os
import subprocess

app = Flask(__name__, template_folder="templates")

def format_size(size):
    units = ["B", "KB", "MB", "GB"]
    index = 0
    while size >= 1024 and index < len(units) - 1:
        size /= 1024
        index += 1
    size = round(size, 2)
    formatted_size = f"{size} {units[index]}"
    return formatted_size

path = "C:/"
part_path = ""
output = ""
@app.route('/', methods=['GET'])
def index():
    global path, part_path

    directories = []
    files = []

    if 'path' in request.args:
        part_path = request.args.get('path') + "/"
        path = path + part_path
    
    if 'back' in request.args:
        splpiter = path.split("/")
        splpiter.pop()
        path = path.replace(f"/{splpiter[-1]}", "")
        splpiter.pop()
    
    try:
        os.chdir(path)
        contents = os.listdir(path)
    except:
        pass
    else:
        for content in contents:
            content_path = os.path.join(path, content)

            if os.path.isdir(content_path):
                timestamp = os.path.getmtime(path + "/" + content)    
                directories.append([content, datetime.fromtimestamp(timestamp).ctime()])
            else:
                if ".py" in content:
                    size = os.path.getsize(content)
                    timestamp = os.path.getmtime(path + "/" + content)  
                    files.append([content, "Python", format_size(size), datetime.fromtimestamp(timestamp).ctime()])
                else:
                    size = os.path.getsize(content)
                    timestamp = os.path.getmtime(path + "/" + content)  
                    files.append([content, "File", format_size(size), datetime.fromtimestamp(timestamp).ctime()])

    if len(path) <= 3:
        status = False
    else:
        status = True

    return render_template('index.html', directories=directories, files=files, status=status, path=path)

@app.route('/', methods=['POST'])
def adding():
    if request.method == 'POST':
        try:
            input_value_p = request.form['python_name']
            opening = open(f"{path}{input_value_p}.py", "w+")
            opening.write("")
            opening.close()
        except:
            pass
        try:
            input_value_t = request.form['txt_name']
            opening = open(f"{path}{input_value_t}.txt", "w+")
            opening.write("")
            opening.close()
        except:
            pass
        try:
            input_value_f = request.form['folder_name']
            mkdir_path = f"{path}{input_value_f}/"
            os.mkdir(mkdir_path)
        except:
            pass
    return redirect(url_for('index'))

@app.route('/editor/txt', methods=['GET'])
def editor_txt():
    global path_2, data
    if 'txt_name' in request.args:
        path_2 = request.args.get('txt_name')
    try:
        with open(path_2, "r") as file:
            data = file.read()
    except:
        pass
    return render_template('index2.html', path_2=path_2, data=data) 

@app.route('/editor/txt', methods=['POST'])
def save_txt():
    if request.method == 'POST':
        try:
            textarea_value = request.form['s_txt']
            while True:
                if "\r" in textarea_value:
                    textarea_value = textarea_value.replace("\r", "")
                else:
                    break
            with open(path_2, "w") as file:
                file.truncate(0)
                file.write(textarea_value)
        except:
            pass
        return redirect(url_for('editor_txt'))

@app.route('/editor/py', methods=['GET'])
def editor_py():
    global path_3, data1
    if 'py_name' in request.args:
        path_3 = request.args.get('py_name')
    try:
        with open(path_3, "r") as file:
            data1 = file.read()
    except:
        pass
    return render_template('index3.html', path_3=path_3, data1=data1, output=output)

@app.route('/editor/py', methods=['POST'])
def save_and_run():
    global output
    if request.method == 'POST':
        if 'save_button' in request.form:
            try:
                textarea_value = request.form['s_python']
                while True:
                    if "\r" in textarea_value:
                        textarea_value = textarea_value.replace("\r", "")
                    else:
                        break
                with open(path_3, "w") as file:
                    file.truncate(0)
                    file.write(textarea_value)
            except:
                pass
            else:
                return redirect(url_for('editor_py'))

        elif 'run_button' in request.form:
            try:
                textarea_value = request.form['s_python']
                while True:
                    if "\r" in textarea_value:
                        textarea_value = textarea_value.replace("\r", "")
                    else:
                        break
                with open(path_3, "w") as file:
                    file.truncate(0)
                    file.write(textarea_value)
            except:
                pass
            try:
                completed_process = subprocess.run(['python', path_3], capture_output=True, text=True)
                if completed_process.returncode == 0:
                    output = completed_process.stdout
                else:
                    output = (completed_process.stderr)
            except Exception as e:
                output = str(e)
            return redirect(url_for('editor_py'))

if __name__ == '__main__':
    app.run()
