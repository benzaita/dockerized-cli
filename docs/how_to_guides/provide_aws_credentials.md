# Provide AWS Credentials

Your dockerized development environment may need AWS credentials. There are a few options to provide these:

## Option 1: Pass environment variables

Configure the dockerized environment to use the AWS_* variables from the host environment. Add this to the `.dockerized/docker-compose.dockerized.yml` file:

```yml
dockerized:
  environment:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_SESSION_TOKEN
```

## Option 2: Mount the credentials file

If you use multiple AWS profiles, you need to mount the AWS credentials file. Add this to the `.dockerized/docker-compose.dockerized.yml` file:

```yml
dockerized:
  volumes:
    - ~/.aws/credentials:/root/.aws/credentials:ro
```
