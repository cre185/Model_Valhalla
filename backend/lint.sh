#!/usr/bin/bash

# TODO: add flake8 here.
# finished
function getdir(){
    for element in `ls $1`
    do  
        dir_or_file=$1"/"$element
        if [ -d $dir_or_file ]
        then 
            getdir $dir_or_file
        else 
            if [ "${dir_or_file##*.}"x = "py"x ]
            then
                echo "treating $dir_or_file"
                $pep8 $dir_or_file
                $flake $dir_or_file
            fi
        fi  
    done
}
pep8="autopep8 --in-place --aggressive --aggressive"
flake="autoflake --in-place --remove-all-unused-imports --remove-unused-variables"
getdir "./"

isort .
flake8 .