#!/bin/bash
PkgName='backend'

Dockerfile='./Dockerfile.backend'
DockerContext=../

echo "Start build image..."
docker build -f $Dockerfile -t $PkgName $DockerContext
if [ $? -eq 0 ]
then
    echo "Build docker image success"
else
    echo "Build docker image failed"
fi
echo "Start run image..."
docker run -p 8000:80 $PkgName