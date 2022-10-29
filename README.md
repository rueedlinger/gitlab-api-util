# Gitlab Vars CLI
Gitlab Vars is a simple Docker image which can be used to create, update and read Gitlab 
project variables in your build pipeline.


### How to use Gitlab Vars CLI
## CLI
The Gitlab token can be changed with env variable `GITLAB_TOKEN`. 
```
export GITLAB_TOKEN="*******************"
```

As default teh Gitlab API url is set to `https://gitlab.com/api/v4` 
if you want to use another URL you can change it with the env variable `GITLAB_URL_API`. 

```
export GITLAB_URL_API="https://gitlab.com/api/v4"
```

This will create the variable `FOO` for project id `4xxxxxxx` and store the value `bar 123`.

```
gitlab-vars create 4xxxxxxx FOO "bar 123"
```

The following command will get the variable value from variable `FOO`.
```
gitlab-vars get 4xxxxxxx FOO
```

The following command will increment and decrement the variable  `BUILD`. The variable
has to be an integer.
```
gitlab-vars incr 4xxxxxxx BUILD
gitlab-vars decr 4xxxxxxx BUILD
```

This will store the current timestamp in the project variable BUILD for project id `4xxxxxxx`.
When you want to use a custom format you can pass the argument `--format %Y-%m-%d-% H:%M:%S`. 
The default format is `%Y%m%d%H%M%S`

```
gitlab-vars timestamp 4xxxxxxx BUILD
```
### Gitlab CI/CD

```
gitlab-vars timestamp 4xxxxxxx BUILD
```



## Development
### Docker
The following command wil build the and run the docker image.
```
docker build -t gitlab-vars .
docker run -ti gitlab-vars /bin/sh 
```

### Python
```
pyenv install 3.10.6
pyenv virtualenv 3.10.6 gitlab
pyenv activate gitlab
pip install -r requirements.txt
```

