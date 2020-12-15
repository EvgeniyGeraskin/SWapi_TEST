# SWapi_TEST

This is the test task. The description of the task is in file Test_task.docx

## Preparation:
- Python3 is required to run:
    - apt-get -y update
    - apt-get install -y python3
    - apt-get install -y python3-pip
    
- Installing libraries:
    - pip3 install -r requirements.txt
    
- Installing Allure (for generating reports):
    - https://github.com/allure-framework/allure2#download
    
## Executing:
- Script start_tests.sh is used to run tests and generate Allure report.

## TASK 11:
Abstract task: try to suggest and implement any other meaningful and suitable tests for "get /people" request. I suggested and implemented the following tests:
- Test that checks if every page contains 10 people objects except for the last page (the last page may contain <= 10 people objects).
- Test that checks if max person ID for /people/:id/ request equals "count" field + 1 from http://swapi.dev/api/people/ request.
- Test thst checks if every "next" and "previous" field from http://swapi.dev/api/people/?page=... request matches the pattern http://swapi.dev/api/people/?page=*number* or null.

## TASK 12:
Abstract task: try to suggest (and implement if possible) any meaningful and suitable tests for "get/people" requests with parameter ?format=wookiee. I suggested the following test: 
- Test that checks if every http://swapi.dev/api/people/:id/ request structurally matches corresponding http://swapi.dev/api/people/:id/?format=wookiee request (the number of fields and type of its content are the same in both queries).
