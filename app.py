from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from datetime import datetime
import os

app = Flask(__name__, template_folder = "templates")

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
        path = path.replace(f"/{splpiter[-1]}","")
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
                timestamp = os.path.getmtime(path+"/"+content)    
                directories.append([content, datetime.fromtimestamp(timestamp).ctime()])
            else:
                if ".py" in content:
                    size = os.path.getsize(content)
                    timestamp = os.path.getmtime(path+"/"+content)  
                    files.append([content, "Python", format_size(size), datetime.fromtimestamp(timestamp).ctime()])
                else:
                    size = os.path.getsize(content)
                    timestamp = os.path.getmtime(path+"/"+content)  
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
            opening = open(f"{path}{input_value_t}.txt","w+")
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

@app.route('/editor', methods=['GET'])
def editor():
    global path_2, data
    if 'txt_name' in request.args:
        path_2 = request.args.get('txt_name')
    try:
        with open(path_2 , "r") as file:
            data = file.read()
    except:
        pass
    return render_template('index2.html', path_2=path_2, data=data) 

@app.route('/editor', methods=['POST'])
def save():
    if request.method == 'POST':
        try:
            textarea_value = request.form['s_txt']
            while True:
                if "\r" in textarea_value:
                    textarea_value = textarea_value.replace("\r","")
                else:
                    break
            with open(path_2, "w") as file:
                file.truncate(0)
                file.write(textarea_value)
        except:
            print("ppp")
        return redirect(url_for('editor'))

if __name__ == '__main__':
    app.run()