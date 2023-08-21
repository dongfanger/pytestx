#!/bin/bash
PkgName='frontend'

Dockerfile='./deploy/Dockerfile.frontend'
DockerContext=./

BUILDER_IMAGE='node:latest'
echo "Start compiling code..."
docker run --rm -v $(pwd)/$PkgName/:/data/src -w /data/src/ $BUILDER_IMAGE  /bin/sh -c "npm install && npm run build"
[ $? -ne 0 ] && exit 2
echo "Compile complete"

echo "Start building image..."
docker build -f $Dockerfile -t $PkgName $DockerContext
if [ $? -eq 0 ]
then
    echo "Build docker image success"
    echo "Start run image..."
    docker run -p 8080:80 $PkgName
else
    echo "Build docker image failed"
fi