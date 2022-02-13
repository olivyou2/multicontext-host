docker kill multicontext
docker stop multicontext

docker build -t "toolscomfact/multicontext-python:latest" .
docker run -d -p 8888:8888 --name multicontext toolscomfact/multicontext-python:latest