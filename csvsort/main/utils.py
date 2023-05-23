import io
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
