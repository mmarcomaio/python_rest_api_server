# python_rest_api_server
## Requirements
* [python 3.5+](https://www.python.org/downloads/release/python-350/)

### Clone the repository and enter it

### Once checked out the repository (first time)
* python virtual environment with the last "pip" version
```
python3 -m venv server_env
# linux
. server_env/bin/activate
# windows
. server_env/bin/activate.bat

pip install –-upgrade pip
```
* flask installed in the virtual environment
```
pip install flask
```

### How to start the backend
```
python rest_api_server.py
```

### How to launch the unit tests
```
python -m unittest db_manager_test.py -v
```
