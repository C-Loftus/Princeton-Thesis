#!/bin/bash

#  focus a window by its title
focus() {
    local title=$1
    local window_id=$(xdotool search --onlyvisible --name "${title}")
    
    if [[ -n "${window_id}" ]]; then
        xdotool windowactivate "${window_id}"
    else
        echo "No window found with title ${title}"
    fi
}

#  execute the rest of the code block only if the argument passed in is in the title of the focused window
window() {
    
    # Get the current title of the focused application
    local title=$(xdotool getwindowfocus getwindowname)
    # last_arg="${!#}"
    local last_arg=$(echo "${!#}" | tr '[:upper:]' '[:lower:]')
    
    # Convert the title to lowercase for case-insensitive comparison
    local title_lower=$(echo "$title" | tr '[:upper:]' '[:lower:]')
    
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

# execute the rest of the code block only if the variable is set
scope() {
    #  exit if the first argument is not set
    local var=$1
    if [ -z ${!var+x} ]; then
        exit 1
    fi
}

# change the working directory to a path relative to the home directory
relative(){
    
    
    local path=$(printf "%s/" "$@")
    
    # the path is relative to the home directory
    local path="$HOME/$path"
    
    # Change the working directory to the new path
    cd "$path"
}

# execute a command n times
loop(){
    local n=$1
    shift
    
    for ((i=1; i<=n; i++))
    do
        # execute the code block
        "$@"
    done
}

# close an application by its name
close() {
    local title=$1
    local window_id=$(xdotool search --onlyvisible --name "${title}")
    
    if [[ -n "${window_id}" ]]; then
        xdotool windowclose "${window_id}"
    else
        echo "No window found with title ${title}"
    fi
}

#  recursively check if a file exists in the current directory
search(){
    local query=$1
    grep -ri "$query" .
    
    if [[ $? -eq 0 ]]; then
        return 0

    else
        return 1
    fi
}

# exit if the command fails, otherwise continue
assert(){
    local command=$1
    eval "$command" &> /dev/null
    if [ $? -eq 0 ]; then
        echo "Succeeded"
    else
        echo "Failed"
        exit 1
    fi
}

# exit if the command succeeds, otherwise catch the error and   continue
catch(){
    local command=$1
    eval "$command" &> /dev/null
    if [ $? -eq 0 ]; then
        exit 1
    fi
}

launch() {
    $@
}

press() {
    local key=$@
    xdotool keydown $key; xdotool keyup $key
}