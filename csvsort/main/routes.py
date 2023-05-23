import pandas as pd
from csvsort.main.utils import (allowed_file,
                                get_csv_path,
                                save_csv_df,
                                validate_content)
from flask import (Blueprint,
                   current_app,
                   flash,
                   redirect,
                   render_template,
                   request,
                   send_file,
                   url_for)

main = Blueprint('main', __name__)


@main.route("/", methods=['GET'])
def home():
    '''
    base route to show the table and use sort buttons
    '''
    csv_path = get_csv_path()

    df = pd.read_csv(csv_path, dtype='str')
    header = df.columns

    sort_choice = request.args.get('sort_choice')
    if sort_choice:
        sorted_df = df.sort_values(by=sort_choice)
        save_csv_df(sorted_df)
        lines = sorted_df.values.tolist()
    else:
        lines = df.values.tolist()

    return render_template('home.html',
                           header=header,
                           lines=lines)


@main.route('/upload', methods=['POST'])
def upload_file():
    '''
    CSV upload route
    - we want to avoid (1) empty and (2) not readable files
    - we want to (3) only ever have a single uploaded file
    '''
    uploaded_file = request.files.get('uploaded_file')

    # (1)
    if not uploaded_file:
        flash('Please Select A File')
        return redirect(url_for('main.home'))

    # (2)
    # check whether the file is convertible into a pd-frame
    uploaded_df = validate_content(uploaded_file)

    # validate_content() returned empty frame -> file is not readable
    if uploaded_df.empty:
        flash('There Is Something Wrong With Your File')
        return redirect(url_for('main.home'))

    if allowed_file(uploaded_file.filename):
        save_csv_df(uploaded_df)    # (3)
        flash('Upload Successful')

    return redirect(url_for('main.home'))


@main.route('/download', methods=['GET'])
def download_file():
    '''
    CSV download route
    - click button
    - get file
    '''
    file_path = get_csv_path()
    return send_file(file_path, as_attachment=True)
