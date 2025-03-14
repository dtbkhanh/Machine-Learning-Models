#!/bin/bash

set -e

cd $(dirname $0)

# JOJO

while [[ "$1" != "" ]]
    do
        case $1 in
            server)
                export PYTHONPATH=.
                ./env/bin/python ./app/web.py

                shift
                ;;
            setup)

                virtualenv -p python3.7 env
                . env/bin/activate
                pip3 install --upgrade pip
                pip3 install -q -r requirements.txt

                shift
                ;;
            *)
                export PYTHONPATH=.
                echo $1
                echo $2
                ./env/bin/python ./app/cli.py $1 $2
                shift
                ;;
    esac
done