from flask import Flask, render_template
from xml.etree import ElementTree

app = Flask(__name__)


path = 'app_data.xml'

root = ElementTree.parse(path).getroot()


image_url = [c.attrib["image"] for c in root.iter('news')]
headers = [c.find('headline').text for c in root.iter('news')]
descriptions = [c.find('description').text for c in root.iter('news')]


d = {"url":image_url,"header":headers,"desc":descriptions}

size = len(d["header"])

@app.route('/')
def hello_world():
    return render_template('index.html', data=d, length=size)





if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
