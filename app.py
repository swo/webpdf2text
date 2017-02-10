from __future__ import print_function
import os, urllib, subprocess, re

from flask import Flask, render_template, request, url_for, redirect

from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
import StringIO

DEBUG = True
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('convert') + '?pdf=' + request.form['pdf'])

    return render_template('home.html')
    
def convert_pdf(target_fn):
    ''' Convert a pdf file into a string of text '''
    laparams = LAParams()
    laparams.all_texts = True
    laparams.detect_vertical = True

    resource_manager = PDFResourceManager(caching=True)
    output_fh = StringIO.StringIO()
    device = TextConverter(resource_manager, output_fh, codec='utf-8',
        laparams=laparams, imagewriter=None)
    interpreter = PDFPageInterpreter(resource_manager, device)

    with open(target_fn, 'rb') as f:
        for page in PDFPage.get_pages(f):
            interpreter.process_page(page)

    device.close()
    output_fh.seek(0)
    content = output_fh.read().decode('utf-8')
    return content

@app.route('/convert')
def convert():
    pdf = request.args.get('pdf', '')
    target_fn = os.path.join('scratch', 'tmp.pdf')
    try:
        urllib.urlretrieve(pdf, target_fn)
    except IOError as e:
        print('IO error({0}): {1}'.format(e.errno, e.strerror))
        return render_template('convert.html', pdf=pdf, pdf_content='IO error')

    pdf_content = convert_pdf(target_fn)

    return render_template('convert.html', pdf=pdf, pdf_content=pdf_content)

if __name__ == '__main__':
    # swo> use this on c9
    #app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
    app.run()
    app.debug = True
