from flask import Flask, render_template, request, jsonify, redirect
from xml.etree import ElementTree


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

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/')
def index():
    return redirect("/home")

@app.route('/news')
def news():
    data_in, s = loadData()

    return render_template('news.html', data=data_in, length=s)




@app.route('/admin',  methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        data = request.get_data();
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
        return render_template('admin.html', item_added = True);
    return render_template('admin.html')


@app.route('/delete/<id>')
def delete(id):
    index = int(id)
    elem = root.getchildren()[index]
    root.remove(elem)
    tree.write(path, "UTF-8")
    return redirect("/news")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
