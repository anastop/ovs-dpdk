#!/bin/bash

curl -v --upload-file $1 https://storage.googleapis.com/incoming-lab/images/$1
