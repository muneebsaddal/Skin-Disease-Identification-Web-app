import os
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('home.html')

@app.route('/about')
def about_page():
	return render_template('about.html')

@app.route('/result')
def result():
	from keras.optimizers import SGD
	from keras.models import load_model
	from keras.preprocessing import image
	from keras.models import Sequential
	from keras.layers import Dense, Dropout, Flatten
	import efficientnet.keras as efn
	import numpy as np


	img_width, img_height = 224, 224
	img = image.load_img('images/0.jpg', target_size=(img_width, img_height))	
	model = load_model('model_1.h5')
	model.compile(optimizer=SGD(lr=0.001, nesterov=True),
		loss="categorical_crossentropy",metrics=["accuracy"])
	x = image.img_to_array(img)
	x = np.expand_dims(x, axis=0)
	images = np.vstack([x])
	classes = model.predict_classes(images, batch_size=10)
	
	return render_template("result.html", img=img, result=classes)

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.filename = "0.jpg"
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
			flash('File successfully uploaded')
			return redirect('/result')
		else:
			flash('Allowed file types are png, jpg, jpeg, gif')
			return redirect(request.url)

if __name__ == "__main__":
    app.run()
