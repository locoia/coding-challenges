## Dependencies
- Docker
- Docker Compose
- Make

## Installation
1. Clone the repository
2. Go to the project root directory
3. Create **.env** file with the variables which are specified in the **.env.example** file
4. Run `make run` command in the terminal to spin up the application
5. To stop the application run `make stop` command
6. To execute tests run `make tests` command

## API Doc
Base URL = http://{HOST_FROM_ENV_FILE}:{PORT_FROM_ENV_FILE}

### Available endpoints

_Method_ GET <br>
_Endpoint_ /ping <br>

_Method_ POST <br>
_Endpoint_ /api/v1/search <br>
_Body_ { <br>
        "username": "{username}", <br>
        "pattern": "{pattern}" <br>
    } <br>
