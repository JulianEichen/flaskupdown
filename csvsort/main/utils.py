import io
import os
import pandas as pd
from flask import current_app


def allowed_file(filename):
    '''
    simple file extension check
    '''
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in \
        current_app.config['ALLOWED_EXTENSIONS']


def validate_content(uploaded_file):
    '''
    Try to read a csv file into a pandas data frame and return the frame.
    If it fails, return an empty data frame.
    We use pandas to avoid storing the file before checking its validity.
    '''
    data = uploaded_file.read()

    file_object = io.BytesIO(data)

    try:
        return pd.read_csv(file_object, dtype='str')
    except UnicodeDecodeError:
        return pd.DataFrame()


def get_csv_path():
    '''
    get the path of the csv  file
    '''
    if os.path.exists(os.path.join(current_app.root_path,
                                   current_app.config['UPLOAD_FOLDER'],
                                   'upload.csv')):
        csv_path = os.path.join(current_app.root_path,
                                current_app.config['UPLOAD_FOLDER'],
                                'upload.csv')
    else:
        csv_path = os.path.join(current_app.root_path, 'static', 'persons.csv')

    return csv_path


def save_csv_df(df):
    '''
    save a pandas dataframe as a csv
    - save as 'upload.csv'
    - overwrite any existing files
    '''
    upload_path = os.path.join(current_app.root_path,
                               current_app.config['UPLOAD_FOLDER'],
                               'upload.csv')

    if os.path.exists(upload_path):  # (3) remove existing file
        os.remove(upload_path)
    df.to_csv(path_or_buf=upload_path,
              sep=',',
              index=False)
