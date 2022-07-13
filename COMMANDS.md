# SCRIPTS
 
## Setup
```
python -m pip install --upgrade pip
pip install virtualenv
python -m venv ./venv
./venv/Scripts/activate.bat
pip install -r requirements.txt
SET FLASK_APP=index.py
SET FLASK_ENV=development
```

## Execute
```
./venv/Scripts/activate.bat
flask run
```