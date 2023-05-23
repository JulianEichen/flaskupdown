import csv
import operator
import os
from csvsort.main.utils import allowed_file, validate_content
from flask import (Blueprint,
                   current_app,
                   flash,
                   redirect,
                   render_template,
                   request,
                   url_for)

main = Blueprint('main', __name__)


@main.route("/", methods=['GET'])
def home():
    '''
    base route to show the table and use sort buttons
    '''
    if os.path.exists(os.path.join(current_app.root_path,
                                   current_app.config['UPLOAD_FOLDER'],
                                   'upload.csv')):
        csv_path = os.path.join(current_app.root_path,
                                current_app.config['UPLOAD_FOLDER'],
                                'upload.csv')
    else:
        csv_path = os.path.join(current_app.root_path, 'static', 'persons.csv')

    with open(csv_path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        col_ind = {header[i]: i for i in range(0, len(header))}
        srt_choice = request.args.get('sort_choice')

        if srt_choice in header:
            reader = sorted(reader,
                            key=operator.itemgetter(col_ind[srt_choice]))

        return render_template('home.html',
                               header=header,
                               lines=reader)


@main.route('/', methods=(['POST']))
def upload_file():
    '''
    CSV upload route
    - we want to avoid (1) empty and (2) not readable files
    - we want to (3) only ever have a single uploaded file
    '''
    uploaded_file = request.files.get('uploaded_file')

    # (1)
    if not (uploaded_file):
        flash('Please Select A File')
        return redirect(url_for('main.home'))

    # (2)
    # check whether the file is convertible into a pd-frame
    uploaded_df = validate_content(uploaded_file)

    # validate_content() returned empty frame -> file is not readable
    if uploaded_df.empty:
        flash('There Is Something Wrong With Your File')
        return redirect(url_for('main.home'))

    upload_path = os.path.join(current_app.root_path,
                               current_app.config['UPLOAD_FOLDER'],
                               'upload.csv')

    if not uploaded_df.empty and allowed_file(uploaded_file.filename):
        if os.path.exists(upload_path):  # (3) remove existing file
            os.remove(upload_path)
        uploaded_df.to_csv(path_or_buf=upload_path,
                           sep=',',
                           index=False)
        flash('Upload Successful')

    return redirect(url_for('main.home'))
