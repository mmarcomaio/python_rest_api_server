# python_rest_api_server
## Requirements
* [python 3.5+](https://www.python.org/downloads/release/python-350/)
* [JAVA 8 SDK](https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html) (for the Kafka Server)
* [Apache Kafka Binaries](https://kafka.apache.org/downloads)
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
### Configuration

<details>
<summary>Click to expand</summary>

As administrator of the REST API server you can customize its behavior by updating the configuration file (config.py) located at the root of the repository.

* <strong>DB schema:</strong> you can change any of the following parameters and the software will automatically benefit from it

```python
DB = {
    'name': 'users.db',
    'path': os.path.join(os.getcwd(), 'data'),
}
TABLE_NAME = 'users'
DB_PRIMARY_KEY = 'id'
DB_COLUMNS = [
    (DB_PRIMARY_KEY, 'INTEGER'),
    ('name', 'TEXT NOT NULL'),
    ('email', 'TEXT NOT NULL UNIQUE'),
    ('password', 'TEXT NOT NULL'),
    ('address', 'TEXT NOT NULL')
]
```

* <strong>User's countries allowed to insert new user:</strong> you can just update the below list

```python
WHITE_LIST_COUNTRIES = ['CH']
```

* <strong>Server(s) network data</strong> 
```python
SERVER_IP_ADDRESS = '127.0.0.1'          # YOUR_SERVER_IP_ADDRESS
SERVER_PORT_NUMBER = 4322                # YOUR_SERVER_PORT_NUMBER
KAFKA_SERVER_IP = '192.168.0.21'         # YOUR_KAFKA_SERVER_IP_ADDRESS
KAFKA_SERVER_PORT = 9092                 # YOUR_KAFKA_SERVER_PORT_NUMBER
KAFKA_TOPIC = 'my-topic-events-1'        # YOUR_KAFKA_TOPIC_NAME
```

* <strong>Local testing overriding variables</strong> 
```python
######### DATA TO BE UPDATED BY THE USER ############
WHITE_LIST_OVERRIDE = False              # To be set to True during the system tests
KAFKA_ACTIVE_SERVER = False              # True if you have a Kafka Server up and running. False otherwise.
```

</details>

### Setup and start the Kafka server

<details>
<summary>Click to expand</summary>

* Download the Kafka binaries from [this link](https://kafka.apache.org/downloads)
* Create a folder named "kafka" and copy the downloaded file in it
* Extract them from the tgz file
```
tar zxvf the_apache_kafka_binaries.tgz
```
* Create a folder named 'data' at the root of the previously created 'kafka' 
  * This will be used by Zookeeper and Apache Kafka
* Update zookeeper data directory path in “config/zookeeper.Properties” configuration file
```
dataDir=YOUR_KAFKA_DIR_PATH/data/zookeper
```
* Update Apache Kafka log file path and network settings in “config/server.properties” configuration file
```
log.dirs=YOUR_KAFKA_DIR_PATH/data/kafka
```
```
advertised.listeners=PLAINTEXT://YOUR_KAFKA_SERVER_IP:YOUR_KAFKA_SERVER_PORT
listeners=PLAINTEXT://0.0.0.0:YOUR_KAFKA_SERVER_PORT
```
* Start Zookeper

```
# Microsoft Windows
cd YOUR_KAFKA_DIR_PATH\bin\windows
.\zookeeper-server-start.bat ..\..\config\zookeeper.properties

# Unix
cd YOUR_KAFKA_DIR_PATH/bin
./zookeeper-server-start.sh ../config/zookeeper.properties
```
* And make sure zookeeper started successfully
```
in the stdout you should see something like this after few seconds:
INFO binding to port 0.0.0.0/0.0.0.0:2181 
```
* Start Apache Kafka
```
# Microsoft Windows
cd YOUR_KAFKA_DIR_PATH\bin\windows
.\kafka-server-start.bat ..\..\config\server.properties

# Unix
cd YOUR_KAFKA_DIR_PATH/bin
./kafka-server-start.sh ../config/server.properties
```
* Finally you can start a Kafka Consumer to get the topic's event created by the REST API server
```
# Microsoft Windows
cd YOUR_KAFKA_DIR_PATH\bin\windows
.\kafka-console-consumer.bat --topic YOUR_TOPIC_NAME --from-beginning --bootstrap-server KAFKA_SERVER_IP:KAFKA_SERVER_PORT

# Unix
cd YOUR_KAFKA_DIR_PATH/bin
./kafka-console-consumer.sh --topic YOUR_TOPIC_NAME --from-beginning --bootstrap-server KAFKA_SERVER_IP:KAFKA_SERVER_PORT
```
</details>

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
* Get users
  * All users
  ```
  curl --location --request GET 'SERVER_IP:SERVER_PORT/users'
  ```
  * User's matching filter
  ```
  curl --location --request GET 'SERVER_IP:SERVER_PORT/users?address=USER_ADDRESS&name=USER_NAME'
  ```
* Get specific user
```
curl --location --request GET 'SERVER_IP:SERVER_PORT/users/USER_ID'
```
* Create new user
```
curl --location --request POST 'SERVER_IP:SERVER_PORT/users' \
--header 'Content-Type: application/json' \
--data-raw '{"email": USER_EMAIL, "password": USER_PWD, "name": USER_NAME, "address": USER_ADDRESS}'
```
* Update existing user
```
curl --location --request PUT 'SERVER_IP:SERVER_PORT/users/USER_ID?email=NEW_USER_EMAIL&name=USER_NAME' \
--data-raw ''
```
* Delete existing user
```
curl --location --request DELETE 'SERVER_IP:SERVER_PORT/users/USER_ID'
```
