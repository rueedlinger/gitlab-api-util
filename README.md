# Gitlab Vars CLI
Gitlab Vars CLI is a simple Docker image which can be used to create, update and read Gitlab 
project variables in your Gitlab build pipeline.


## How to use Gitlab Vars CLI
### Tokens
The Gitlab personal access token can be changed with env variable `GITLAB_VARS_PERSONAL_TOKEN`.  
```
export GITLAB_VARS_PERSONAL_TOKEN="*******************"
```
If the personal 
access token is not set the cli will look for a Gitlab job token (`CI_JOB_TOKEN`).

### API
As default teh Gitlab API url is set to `https://gitlab.com/api/v4` or the CI/CD variable `CI_API_V4_URL`. 
If you want to use another URL you can change it with the env variable `GITLAB_VARS_API_URL`. 


```
export GITLAB_VARS_API_URL="https://gitlab.com/api/v4"
```

### Project ID
For most of the command you can specify the Gitlab project id (`--project 4xxxxxxx`) as an option.
If you do not set the project id the cli will check if the env variable `CI_PROJECT_ID` or `GITLAB_VARS_PROJECT_ID` 
is set adn use this value as project id.

```
gitlab-vars get FOO --project 4xxxxxxx
```

### CLI Commands
This will create the variable `FOO` for project id `4xxxxxxx` and store the value `bar 123`. 

```
gitlab-vars create FOO "bar 123" --project 4xxxxxxx
```


The following command will get the variable value from variable `FOO`.
```
gitlab-vars get FOO
```

The following command will increment and decrement the variable  `BUILD`. The variable
has to be an integer.
```
gitlab-vars incr BUILD
gitlab-vars decr BUILD
```

This will store the current timestamp in the project variable BUILD for project id `4xxxxxxx`.
When you want to use a custom format you can pass the argument `--format %Y-%m-%d-% H:%M:%S`. 
The default format is `%Y%m%d%H%M%S`

```
gitlab-vars timestamp BUILD
```

### Gitlab CI/CD Pipeline
The following Gitalb CI/CD pipeline will update the project variables `BUILD_COUNTER` and `BUILD_TIME`.
In this example the job token `CI_JOB_TOKEN`, project id `$CI_PROJECT_ID` and API URL `CI_API_V4_URL` 
from Gitlab are used when running the cli commands.

```
update-build-counter:
  image: rueedlinger/gitlab-vars-cli
  script: 
    - echo $CI_PROJECT_ID
    - echo $CI_API_V4_URL
    - gitlab-vars incr BUILD_COUNTER
    - gitlab-vars timestamp BUILD_TIME
```


> **Note**: The variables `BUILD_COUNTER` and `BUILD_TIME` must already exist.

# Development
## Docker
The following command wil build the and run the docker image.
```
docker build -t gitlab-vars .
docker run -ti gitlab-vars /bin/sh 
```

## Python
```
pyenv install 3.10.6
pyenv virtualenv 3.10.6 gitlab
pyenv activate gitlab
pip install -r requirements.txt
```

