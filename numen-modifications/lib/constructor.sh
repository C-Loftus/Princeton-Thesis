#!/bin/bash


window() {
    
    # Get the current title of the focused application
    title=$(xdotool getwindowfocus getwindowname)
    # last_arg="${!#}"
    last_arg=$(echo "${!#}" | tr '[:upper:]' '[:lower:]')
    
    # Convert the title to lowercase for case-insensitive comparison
    title_lower=$(echo "$title" | tr '[:upper:]' '[:lower:]')
    
    # Check if the last argument is in the title
    if [[ $title_lower == *"$last_arg"* ]]; then
        :
    else
        exit 1
    fi
}

set() {
    #  creating new variable with the name as the first argument
    #  and the value as the second argument
    local var=$1
    export "$var"=1
    
}

unset() {
    #  unsetting the variable with the name as the first argument
    local var=$1
    unset "$var"
}

iff() {
    #  exit if the first argument is not set
    local var=$1
    if [ -z ${!var+x} ]; then
        exit 1
    fi
}

relative(){
    
    
    path=$(printf "%s/" "$@")
    
    # the path is relative to the home directory
    path="$HOME/$path"
    
    # Change the working directory to the new path
    cd "$path"
}

loop(){
    local n=$1
    shift
    
    for ((i=1; i<=n; i++))
    do
        # execute the code block
        "$@"
    done
}

# loop 5 echo "hello"
relative Projects && pwd
# && pwd | cat

# echo "test is set" and echo test is set

# eval set test && iff test && window code && echo "test is set"
# eval '(set test && iff test && echo "test is set")'

