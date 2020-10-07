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
server_env\Scripts\activate.bat

pip install –-upgrade pip
```
* python flask module installed in the virtual environment
```
pip install flask
```
* python kafka-python module installed in the virtual environment
```
pip install kafka-python
```

### How to start the backend
```
python rest_api_server.py
```

### How to launch the unit tests
```
python -m unittest discover -p "*_test.py" -v
```

### How to launch the system tests
* Install Postman (https://www.postman.com/downloads/)
* Import the environment configuration file
![Config import in Postman](img/import_config_postman.png?raw=true "Config_import")
* from the following path
```
./postman_tests/rest_api_postman_environment.postman_environment.json
```
* Import the collection, containing the system tests
![Collection import in Postman](img/import_collection_postman.png?raw=true "Collection_import")
* and now you are ready to run the tests
  * Select them from the right column
  * Click on "Send" to run the tests
  * Check the result by clicking on "Test Results"
![Run tests in Postman](img/run_tests.png?raw=true "Run_tests")