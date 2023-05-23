# flaskupdown
## Purpose
Little exercise project, to implement upload, representation, manipulation and download of a CSV-file.

## Understanding The App
### Important Frameworks

- Flask: main framework
- Jinja2: template engine
- pandas: CSV manipulation
- pytest: testing framework

## Structure

Absolute basic flask packaging structure, to use the blueprint feature and ease testing.

## Usage
### Running The App Locally 

Assuming we are using Linux and Python 3.10+ is installed, we can use the following commands in a terminal to download the repository, install the dependencies. 

```
git clone git@github.com:JulianEichen/flaskupdown.git
cd flaskupdown
pip install -r requirements.txt
```

We can now use
```
python3 run.py
```
and access the app in a browser under http://localhost:5000/

### Navigation

The homepage shows a default table, which can be sported by clicking the buttons above it or downloaded by using the button below. It is also possible to upload a new file with the options to the right. 
