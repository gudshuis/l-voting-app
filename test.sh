#!/bin/bash

# Define test function
test_app_title() {
    expected_title="Azure Voting App"
    app_title=$(grep "TITLE =" azure-vote/azure-vote/config_file.cfg | awk -F "'" '{print $2}')
    
    if [[ "$app_title" == "$expected_title" ]]; then
        echo "Test Passed: TITLE matches expected value."
        return 0
    else
        echo "Test Failed: Expected '$expected_title', got '$app_title'."
        return 1
    fi
}

test_dockerfile_port() {
    expected_port=80
    dockerfile_port=$(grep "ENV PORT=" azure-vote/Dockerfile | awk -F "=" '{print $2}')
    
    if [[ "$dockerfile_port" == "$expected_port" ]]; then
        echo "Test Passed: Dockerfile PORT matches expected value."
        return 0
    else
        echo "Test Failed: Expected '$expected_port', got '$dockerfile_port'."
        return 1
    fi
}

# Execute tests
echo "Running tests..."
test_app_title
test_result_1=$?

test_dockerfile_port
test_result_2=$?

# Return overall test result
if [[ $test_result_1 -eq 0 && $test_result_2 -eq 0 ]]; then
    echo "All tests passed."
    exit 0
else
    echo "Some tests failed."
    exit 1
fi
