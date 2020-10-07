# python_rest_api_server
## Requirements
* [python 3.5+](https://www.python.org/downloads/release/python-350/)

## Installation
### Clone the repository and enter it

<details>
<summary>Click to expand</summary>

```
git clone https://github.com/mmarcomaio/python_rest_api_server.git
cd python_rest_api_server
```
</details>

### Once checked out the repository (first time)

<details>
<summary>Click to expand</summary>

* python virtual environment with the last "pip" version

```shell
python -m venv server_env
# linux
. server_env/bin/activate
# windows
server_env\Scripts\activate.bat

pip install –-upgrade pip
```

* python flask module installed in the virtual environment

```shell
pip install flask
```

* python kafka-python module installed in the virtual environment

```shell
pip install kafka-python
```

</details>

## Execution
### How to start the backend
```shell
python -m venv server_env
# linux
. server_env/bin/activate
# windows
server_env\Scripts\activate.bat

python rest_api_server.py
```

## Testing
### How to launch the unit tests

<details>
<summary>Click to expand</summary>

```python
python -m unittest discover -p "*_test.py" -v
```

</details>

### How to launch the system tests

<details>
<summary>Click to expand</summary>

* Install Postman (https://www.postman.com/downloads/)
* Import the environment configuration file
![Config import in Postman](img/import_config_postman.png?raw=true "Config_import")
* from the following path

```shell
./postman_tests/rest_api_postman_environment.postman_environment.json
```

* Import the collection, containing the system tests
![Collection import in Postman](img/import_collection_postman.png?raw=true "Collection_import")
* and now you are ready to run the tests
    * Select them from the right column
    * Click on "Send" to run the tests
    * Check the result by clicking on "Test Results"
![Run tests in Postman](img/run_tests.png?raw=true "Run_tests")

</details>

## API Usage
