#!/bin/bash
# Init development environment
# YOU SHOULD TO ACTIVATE ENV
grep_res=$(conda info | grep "active environment")

# Change it in case of diff env name
ENV_NAME=fluffy-video-playground

my_array=($(echo ${grep_res} | tr ":" "\n"))
current_env=${my_array[-1]}

if [[ "${current_env}" == "${ENV_NAME}" ]];
then
    echo "Success!"
    echo "ENVIRONMENT INFO ${current_env}"
    conda install opencv > /dev/null
    conda install numpy > /dev/null
    conda install pip > /dev/null
    conda install sanic > /dev/null
    pip install opencv-python > /dev/null
    pip install -r requirements.txt > /dev/null
    echo "All required packages have been installed to the env - ${current_env}"
else
    echo "YOU MUST ACTIVATE ${ENV_NAME} ENV!"
    echo ${current_env} ${ENV_NAME}
fi