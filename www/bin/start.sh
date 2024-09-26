#!/bin/bash

cd `dirname $0`/..
ls
ssh-add id_rsa_github

php -S localhost:3000 >> /tmp/aaa 2>&1
