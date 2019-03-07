from flask import Flask, render_template, request
from xml.etree import ElementTree
import json

app = Flask(__name__)


path = 'app_data.xml'
tree = ElementTree.parse(path)
root = tree.getroot()

#creat new xml data
def newXMLElem(title, des, url):
    news_element = ElementTree.SubElement(root, "news")
    news_element.set('image',url)
    headline_element = ElementTree.SubElement(news_element, "headline")
    headline_element.text = title
    description__element= ElementTree.SubElement(news_element, "description")
    description__element.text = des
    tree.write(path, "UTF-8")
    print("Done writing")


#get xml data
def loadData():
    #get list of image urls
    image_url = [c.attrib["image"] for c in root.iter('news')]
    #get list of headlines
    headers = [c.find('headline').text for c in root.iter('news')]
    #get list of description
    descriptions = [c.find('description').text for c in root.iter('news')]

    #organize data into dictionary
    data_dictionary = {"url":image_url,"header":headers,"desc":descriptions}

    #size of data
    size = len(data_dictionary["header"])

    return data_dictionary, size

@app.route('/')
def home():
    data_in, s = loadData()

    return render_template('index.html', data=data_in, length=s)

@app.route('/insert', methods=['GET', 'POST'])
def insert_data():
    #this block is only entered when the form is submitted
    if request.method == 'POST':
        req_data = request.get_data();
        print(" *"*50, end="")
        print("Posted data", end="")
        print(" *"*50)
        print(req_data)
        print(" *"*100)
        head = request.form['headline']
        des = request.form['des']
        image = request.form['url']
        newXMLElem(head, des,image)
        return '''<h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>
                  <h1>The framework value is: {}</h1>'''.format(head,des, image)


    return '''<form method="POST">
                  Headline: <input type="text" name="headline"><br>
                  Image: <input type="url" name="url"><br>
                  Description: <input type="text" name="des"><br>
                  <input type="submit" value="Submit"><br>
              </form>
          '''




if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
