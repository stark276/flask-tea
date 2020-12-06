from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os


host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Teas_tore')


client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
teas = db.teas

app = Flask(__name__)

# teas = [
#     { 'title': 'mango', 'description': 'bellisimo' },
#     { 'title': '80\'s Music', 'description': 'Stop believing!' }

@app.route('/')
def teas_index():
    """Show all lists."""
    return render_template('teas_index.html', teas=teas.find())

"""Creates new item"""

@app.route('/teas/new')
def teas_new():
    """Create a new tea list."""
    return render_template('teas_new.html',  tea ={}, title ="create new")

"""Shows the item"""
@app.route('/teas/<tea_id>')
def teas_show(tea_id):
    
    tea = teas.find_one({'_id': ObjectId(tea_id)})
    return render_template('teas_show.html', tea=tea)


"""Creates new item (form action) """
@app.route('/teas', methods=['POST'])
def teas_submit():

    tea = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        "price": request.form.get("price"),
        "domain": request.form.get("domain")
    }

    teas.insert_one(tea).inserted_id
    return redirect(url_for('teas_index'))
"""user can update"""
@app.route("/teas/<tea_id>/edit")
def teas_edit(tea_id):
	tea = teas.find_one({"_id" : ObjectId(tea_id)})
	return render_template("teas_edit.html", tea = tea, title = "Edit Your Product")


@app.route("/teas/<tea_id>", methods = ['POST'])
def teas_update(tea_id):
	updated_tea = {
		"tea_name": request.form.get("tea_name"),
		"description": request.form.get("description"),
		"price": request.form.get("price"),
        "domain": request.form.get("domain")

	}

	teas.update_one( {"_id" : ObjectId(tea_id)}, {"$set" : updated_tea})
	return redirect(url_for("teas_show", tea_id = tea_id))

"""user can delete item"""
@app.route("/teas/<tea_id>/delete", methods=["POST"])
def teas_delete(tea_id):
	teas.delete_one({"_id" : ObjectId(tea_id)})
	return redirect(url_for("teas_index"))


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')











if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
