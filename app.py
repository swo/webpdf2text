from __future__ import print_function
import os, urllib, subprocess, re

from flask import Flask, render_template, request, url_for, redirect
#from wtforms import Form, TextField, StringField, validators, SubmitField

DEBUG = True
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('convert') + '?pdf=' + request.form['pdf'])

    return render_template('home.html')
    
@app.route('/convert')
def convert():
    pdf = request.args.get('pdf', '')
    
    target = os.path.join('scratch', 'tmp.pdf')
    
    try:
        urllib.urlretrieve(pdf, target)
    except IOError as e:
        print('IO error({0}): {1}'.format(e.errno, e.strerror))
        return render_template('convert.html', pdf=pdf, pdf_content='IO error')
        
    res = subprocess.check_output(['pdftotext', target, '-'])
    pdf_content = res.decode('utf-8')
    
    return render_template('convert.html', pdf=pdf, pdf_content=pdf_content)
    
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
    app.debug = True