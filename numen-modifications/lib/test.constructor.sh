#!/bin/bash

source ./constructor.sh

test_equivalence() {
    local cmd=$1
    local expected_output=$2
    local actual_output=$(eval $cmd)
    
    if [ "$actual_output" != "$expected_output" ]; then
        echo "Failure for '$cmd'"
        echo "Expected output: '$expected_output'"
        echo -e "Actual output: '$actual_output'\n"
    else
        echo -e "Success for cmd: '$cmd'\n"
    fi
}

test_equivalence "loop 5 echo test" "test
test
test
test
test"

test_equivalence 'relative Videos; echo $PWD' "$HOME/Videos"

test_equivalence "set test && scope test && echo 'test is set'" "test is set"

test_equivalence 'catch search junkjunkjunk && echo caught error" "caught error'
