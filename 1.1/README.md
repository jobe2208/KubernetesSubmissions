\# Exercise 1.1 - Log Output



A Python application that generates a UUID at startup

and outputs it with a timestamp every five seconds.



\## Technologies

\- Python

\- Docker

\- Kubernetes

\- k3d



\## Run locally

python app.py



\## Build Docker image

docker build -t log-output .



\## Run Docker container

docker run log-output



\## Deploy to Kubernetes

kubectl create deployment log-output --image=log-output



\## View logs

kubectl logs -f deployment/log-output



