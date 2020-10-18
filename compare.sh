#!/bin/bash

usage() {
	echo "usage: ${0} file1 file2"
	exit 1
}

container_msg() {
	echo "The container doesn't appear to be running."
	echo "See the README for building and running the container"
	exit 1
}

# Check that we have 2 arguments
[[ $2 ]] || usage "toast"

# Check that the container is up and running
[[ $(docker ps -a | grep fetch | grep 5000) ]] || container_msg

# Check that the 2 files exist
[[ ! -f ${1} ]] && echo "${1} not found" && exit 1
[[ ! -f ${2} ]] && echo "${2} not found" && exit 1

curl --data-urlencode doc_a@${1}  --data-urlencode doc_b@${2} http://localhost:5000/score
