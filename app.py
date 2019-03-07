from flask import Flask, render_template
from xml.etree import ElementTree

app = Flask(__name__)


path = 'app_data.xml'
tree = ElementTree.parse(path)
root = tree.getroot()

#creat new xml data
def newXMLElem(title, des, url):
    news_element = ElementTree.SubElement(root, "news")
    news_element.set('img',url)
    headline_element = ElementTree.SubElement(news_element, "headline")
    headline_element.text = title
    description__element= ElementTree.SubElement(news_element, "description")
    description__element.text = des


#get xml data
#get list of image urls
image_url = [c.attrib["image"] for c in root.iter('news')]
#get list of headlines
headers = [c.find('headline').text for c in root.iter('news')]
#get list of description
descriptions = [c.find('description').text for c in root.iter('news')]

#organize data into dictionary
data_dictionary = {"url":image_url,"header":headers,"desc":descriptions}

#size of data
size = len(d["header"])

@app.route('/')
def home():
    return render_template('index.html', data=data_dictionary, length=size)

@app.route('/insert', methods=['GET', 'POST'])
def insert_data():
    return '''<form method="POST">
                  Language: <input type="text" name="language"><br>
                  Framework: <input type="text" name="framework"><br>
                  <input type="submit" value="Submit"><br>
              </form>
          '''




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
