# eDreams-Data-Engineer-test

### How to run the script:

```bash
# clone the repo
git clone the repo

# create venv --> Necessary to avoid package conflicts
python -m venv venv

# activate venv
source venv/Scripts/activate

# install packages
pip install -r requirements.txt

# run the script, before you need to go to the src folder
cd /src
python load_json_travels_into_sqlite3.py 

# In case you want to try the tests, go to the main folder of this project and run pytest
cd ..
pytest.exe
```