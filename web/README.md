## Run with docker compose

```
$ docker compose up
Creating network "django_default" with the default driver
Building web
Step 1/6 : FROM python:3.7-alpine
...
...
Status: Downloaded newer image for python:3.7-alpine
Creating django_web_1 ... done

```

# Build and deploy

1. Authenticate with AWS: 
  
  ```bash
  $ aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/r1s3i7n4
  ```

2. Docker build with tag

  ```bash
  $ docker build -t price-tracker-web .  
  ```

3. Docker tag

  ```bash
   $ docker tag price-tracker-web:latest public.ecr.aws/r1s3i7n4/price-tracker-web:latest
   ```

4. Push to ECR 

  ```bash
  $ docker push public.ecr.aws/r1s3i7n4/price-tracker-web:latest 
  ```

5. Force deploy in ECS