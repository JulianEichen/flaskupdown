import os
import pandas as pd
from io import BytesIO

def test_home_page(test_client):
    '''
    GIVEN an app configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that response is valid
    '''
    response = test_client.get('/')

    default_csv_name = 'persons.csv'
    test_dir = os.path.join(os.path.dirname(__file__), 'test_input')
    default_csv_path = os.path.join(test_dir, default_csv_name)

    assert response.status_code == 200
    assert validate_order(default_csv_path, response.data)


def test_sort(test_client):
    '''
    GIVEN an app configured for testing, with default csv data
    WHEN the '/?sort_choice=Vorname' page is requested (GET)
    THEN check that response is valid
    '''

    response = test_client.get('/?sort_choice=Vorname')

    sorted_csv_name = 'persons_sorted_vorname.csv'
    test_dir = os.path.join(os.path.dirname(__file__), 'test_input')
    sorted_csv_path = os.path.join(test_dir, sorted_csv_name)

    assert response.status_code == 200
    assert validate_order(sorted_csv_path, response.data)


def test_csv_upload(test_client):
    '''
    GIVEN an app configured for testing
    WHEN the '/upload' page is posted to, with a new CSV file
    THEN check that response is valid
    '''
    new_csv_name = 'persons_copy.csv'
    test_dir = os.path.join(os.path.dirname(__file__), 'test_input')
    new_csv_path = os.path.join(test_dir, new_csv_name)

    data = {'uploaded_file': (open(new_csv_path, 'rb'), 'upload.csv')}

    response = test_client.post('/upload', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert validate_order(new_csv_path, response.data)


def test_csv_double_upload(test_client):
    '''
    GIVEN an app configured for testing, with default csv data
    WHEN the '/upload' page is posted to, with a new CSV file 2 times
    THEN check that response is valid
    '''
    new_csv_name = 'persons_copy.csv'
    test_dir = os.path.join(os.path.dirname(__file__), 'test_input')
    new_csv_path = os.path.join(test_dir, new_csv_name)

    data_1 = {'uploaded_file': (open(new_csv_path, 'rb'), 'upload.csv')}
    data_2 = {'uploaded_file': (open(new_csv_path, 'rb'), 'upload.csv')}

    response_1 = test_client.post('/upload', data=data_1, follow_redirects=True)
    response_2 = test_client.post('/upload', data=data_2, follow_redirects=True)

    assert response_1.status_code == 200
    assert validate_order(new_csv_path, response_1.data)
    assert b"Upload Successful" in response_1.data
    assert response_2.status_code == 200
    assert validate_order(new_csv_path, response_2.data)
    assert b"Upload Successful" in response_2.data


def test_empty_upload(test_client):
    '''
    GIVEN an app configured for testing
    WHEN the '/upload' page is posted to, with no file selected
    THEN check that response is valid
    '''

    response = test_client.post('/upload', follow_redirects=True)

    default_csv_name = 'persons.csv'
    test_dir = os.path.join(os.path.dirname(__file__), 'test_input')
    default_csv_path = os.path.join(test_dir, default_csv_name)

    assert response.status_code == 200
    assert validate_order(default_csv_path, response.data)
    assert b"Please Select A File" in response.data


def test_corrupted_upload(test_client):
    '''
    GIVEN an app configured for testing
    WHEN the '/upload' page is posted to, with an image file that bypasses the .csv check
    THEN check that response is valid
    '''
    new_csv_name = "frog.csv"
    test_dir = os.path.join(os.path.dirname(__file__), 'test_input')
    new_csv_path = os.path.join(test_dir, new_csv_name)

    data = {'uploaded_file': (open(new_csv_path, 'rb'), 'upload.csv')}

    response = test_client.post('/upload', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b"There Is Something Wrong With Your File" in response.data


def test_download(test_client):
    '''
    GIVEN an app configured for testing
    WHEN the '/download' page is requested
    THEN check that the reponse is valid
    '''
    screen_data = test_client.get('/').data
    screen_df = pd.read_html(screen_data, converters={'Telefonnummer': str})
    response = test_client.get('download')
    out_df = pd.read_csv(BytesIO(response.data), dtype='str')

    assert response.status_code == 200
    assert out_df.equals(screen_df[0].astype(str))


def validate_order(csv_path, response_data):
    '''
    check equality of datafram from a csv and response data
    '''
    data_frame = pd.read_html(response_data, converters={'Telefonnummer': str})
    input_frame = pd.read_csv(csv_path, dtype='str')

    return input_frame.equals(data_frame[0].astype(str))
