#!/bin/bash

while getopts ":b" opt; do
    case $opt in
        b)
            echo "rm -rf lib\nmkdir -p lib"
            sudo rm -rf lib
            sudo mkdir -p lib

            sudo pip2 install -r requirements.txt -t lib
            sudo pip2 install -r requirements.txt
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            ;;
    esac
done

echo "dev_appserver.py ./"
dev_appserver.py ./
