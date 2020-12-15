import pytest
import requests
import json
import string
import re
import allure


numbers_letters = list(string.ascii_lowercase + string.ascii_uppercase + '0123456789')


# TASK_1
# Fixture which return the array of all people
@pytest.fixture()
def all_people_array():
    people = []
    query = 'http://swapi.dev/api/people/?page=1'
    next = True
    while next:
        response = requests.get(query)
        json_data = json.loads(response.content)
        for resource in json_data['results']:
            people.append(resource)
        if bool(json_data['next']):
            query = json_data['next']
        else:
            next = False
    return people


# TASK_2
# Test which checks length of array of all people with "count" field in response of simple get/people request
def test_length_of_people_array(all_people_array):
    with allure.step("Execute the request http://swapi.dev/api/people/?page=1"):
        all_people = requests.get('http://swapi.dev/api/people/?page=1').json()
    count = all_people['count']
    length = len(all_people_array)
    print("\nCount field from request:", count)
    print("Length of the all_people_array:", length)
    with allure.step("Checking the equality of the length of an array of people and field COUNT"):
        if length == count:
            assert True
        else:
            assert False, 'Length of the all_people_array does not equal count field from request'


# TASK_3
# Test which checks that names of all people are unique
def test_all_names_are_unique(all_people_array):
    names_arr = []
    with allure.step("Creating an array of people's names"):
        for i in all_people_array:
            names_arr.append(i['name'])
    with allure.step("Creating a set of people's names"):
        unique_names = set(names_arr)
    print("\nSet of the unique names:", str(unique_names))
    print("Length of the set:", len(unique_names))
    print("Length of the all_people_array:", len(all_people_array))
    with allure.step("Checking the equality of the length of an array of people and length of a set of people's names"):
        if len(unique_names) == len(all_people_array):
            assert True
        else:
            assert False, 'Not all names are unique'


# TASK_4
# Test for validation that search for people is case insensitive
def test_search_is_case_insensitive_1():
    with allure.step("Execute the request https://swapi.dev/api/people/?search=LUKE"):
        query1 = requests.get('https://swapi.dev/api/people/?search=LUKE').json()
    with allure.step("Execute the request https://swapi.dev/api/people/?search=luke"):
        query2 = requests.get('https://swapi.dev/api/people/?search=luke').json()
    print("\nThis is first search result:", query1)
    print("This is second search result:", query2)
    with allure.step("Checking the equality of the result of two queries"):
        if query1 == query2:
            assert True
        else:
            assert False, 'Search is case sensitive'


# TASK_4
# One more test for validation that search for people is case insensitive
def test_search_is_case_insensitive_2():
    with allure.step("Execute the request https://swapi.dev/api/people/?search=R2-D2"):
        query1 = requests.get('https://swapi.dev/api/people/?search=R2-D2').json()
    with allure.step("Execute the request https://swapi.dev/api/people/?search=r2-d2"):
        query2 = requests.get('https://swapi.dev/api/people/?search=r2-d2').json()
    print("\nThis is first search result:", query1)
    print("This is second search result:", query2)
    with allure.step("Checking the equality of the result of two queries"):
        if query1 == query2:
            assert True
        else:
            assert False, 'Search is case sensitive'


# TASK_5
# Test which validate that there is no page with number 0 for people request
def test_no_page_with_number_0():
    with allure.step("Execute the request http://swapi.dev/api/people/?page=0"):
        query = requests.get('http://swapi.dev/api/people/?page=0')
    print("\nStatus code:", query.status_code)
    with allure.step("Checking that the status code is 404"):
        if query.status_code == 404:
            assert True
        else:
            assert False, 'There is page with number 0'


# TASK_6
# Parametrized test which will check that there are 3 Skywalker's, 1 Vader, 2 Darth's
@pytest.mark.parametrize('search, number', [('Skywalker', 3), ('Vader', 1), ('Darth', 2)])
def test_Skywalker_Vader_Darth(search, number):
    with allure.step("Execute the request https://swapi.dev/api/people/?search=" + str(search)):
        query = requests.get('https://swapi.dev/api/people/?search=' + str(search)).json()
    print("\nSearch result:", query)
    with allure.step("Checking that the COUNT field equals to " + str(number)):
        if query['count'] == number:
            assert True
        else:
            assert False, 'The number of people with this name does not match the expected number'


# TASK_7
# Fixture which return schema of people object
@pytest.fixture()
def people_schema():
    schema = requests.get('https://swapi.dev/api/people/schema').json()
    return schema


# TASK_8
# Test which validate that all people objects contain required schema fields
def test_all_people_contain_required_schema_fields(all_people_array, people_schema):
    for person in all_people_array:
        print("Test person:", person)
        for attribute in people_schema['required']:
            with allure.step("Checking that the " + str(person["name"]) + " object contains " + str(attribute)):
                if attribute in person:
                    assert True
                else:
                    assert False, 'Person does not contain required schema field'


# TASK_9
# Factory fixture which return search people results
@pytest.fixture()
def search_people():
    def _search_people(search):
        return requests.get('https://swapi.dev/api/people/?search=' + str(search)).json()
    return _search_people


# TASK_10
# Test which check that search for any char in English alphabet or any number from 0 to 9 will return number
# of results >0 except cases of search by 6, 9 and 0.
@pytest.mark.parametrize('numbersletters', numbers_letters)
def test_search_any_char_number(search_people, numbersletters):
    print(search_people(numbersletters))
    if numbersletters == '0' or numbersletters == '6' or numbersletters == '9':
        with allure.step("Checking that the search result COUNT field equals to 0"):
            if search_people(numbersletters)['count'] == 0:
                assert True
            else:
                assert False, 'Count parameter does not equal to 0'
    else:
        with allure.step("Checking that the search result COUNT field more than 0"):
            if search_people(numbersletters)['count'] > 0:
                assert True
            else:
                assert False, 'Count parameter does not more than 0'


# TASK_11
# Test which check that every page contain 10 people objects except the last page
# (the last page may contain <= 10 people objects)
def test_every_page_contain_10_people():
    query = 'http://swapi.dev/api/people/?page=1'
    next = True
    while next:
        with allure.step("Execute the request " + str(query)):
            response = requests.get(query)
        json_data = json.loads(response.content)
        print("This is request data:", json_data)
        with allure.step("Checking that page contain 10 people objects except the last page "
                         "(the last page may contain <= 10 people objects)"):
            if bool(json_data['next']) and len(json_data['results']) == 10:
                assert True
            elif not bool(json_data['next']) and len(json_data['results']) <= 10:
                assert True
            else:
                assert False, 'The page contains an incorrect number of people objects'
        if bool(json_data['next']):
            query = json_data['next']
        else:
            next = False


# TASK_11
# Test which check that max person ID for /people/:id/ request = "count" field + 1
# from http://swapi.dev/api/people/ request
def test_max_person_id():
    query = 'http://swapi.dev/api/people/'
    with allure.step("Get COUNT field from http://swapi.dev/api/people/ request"):
        count = requests.get(query).json()['count']
    with allure.step("Get status code of http://swapi.dev/api/people/" + str(count+1) + " request"):
        valid_max_id_status_code = requests.get('http://swapi.dev/api/people/' + str(count+1)).status_code
    print("\nStatus code of id = count+1:", valid_max_id_status_code)
    with allure.step("Get status code of http://swapi.dev/api/people/" + str(count + 2) + " request"):
        invalid_max_id_status_code = requests.get('http://swapi.dev/api/people/' + str(count+2)).status_code
    print("Status code of id = count+2:", invalid_max_id_status_code)
    with allure.step("Check that first status code is 200 and second is 404"):
        if valid_max_id_status_code == 200 and invalid_max_id_status_code == 404:
            assert True
        else:
            assert False, 'The max person ID != "count" field + 1 from http://swapi.dev/api/people/ request'


# TASK_11
# Test which check that every "next" and "previous" fields from http://swapi.dev/api/people/?page=... request
# matches the pattern http://swapi.dev/api/people/?page=<number> or null
def test_next_previous_matches_the_pattern():
    query = 'http://swapi.dev/api/people/?page=1'
    next = True
    while next:
        with allure.step("Execute the request " + str(query)):
            response = requests.get(query)
        json_data = json.loads(response.content)
        print("This is request data:", json_data)
        pattern = r"http://swapi\.dev/api/people/\?page=[0-9]+"
        if bool(json_data['next']):
            result = re.findall(pattern, json_data['next'])
            with allure.step("Check that NEXT field matches the pattern"):
                if bool(result):
                    assert True
                else:
                    assert False, 'Next field does not matches the pattern'
        if bool(json_data['previous']):
            result = re.findall(pattern, json_data['previous'])
            with allure.step("Check that PREVIOUS field matches the pattern"):
                if bool(result):
                    assert True
                else:
                    assert False, 'Previous field does not matches the pattern'
        if bool(json_data['next']):
            query = json_data['next']
        else:
            next = False
