import subprocess
import os
from datetime import datetime
from subprocess import Popen
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/getAll", methods = ["GET","POST"])
def getAll():
    category = request.form.get("category")
    startPage = int(request.form.get("startPage"))
    endPage = int(request.form.get("endPage"))

    now = datetime.now()
    date_time = now.strftime("%m-%d-%Y_%H-%M-%S")
    # /scrape?filename=jsonfilename
    filename = request.args.get('filename', default=f'{category}-{startPage}-{endPage}', type=str)
    output_json = filename + '.json'
    spider_name = "pyscrapy2"
    try:
        subprocess.check_output(['scrapy', 'crawl', spider_name, "-a", f"category={category}", "-a", f"start={startPage}", "-a", f"end={endPage}", "-o", 'output/' + output_json])
        return render_template("scrape.html", output=output_json)
    except:
        return "Komut satirinda scrapy calistirilirken hata olustu."

@app.route('/output-json')
def output_json():
    files = os.listdir('output')
    files = [file for file in files]
    return render_template('output-json.html', files=files)


@app.route('/output-json/<filenamejson>')
def read_json(filenamejson, static_folder="output"):
    output_path = os.path.join(static_folder, filenamejson)
    json_file= open(output_path, encoding="utf8")
    text = json_file.read()
    return text


if __name__ == '__main__':
    app.run(debug=True)