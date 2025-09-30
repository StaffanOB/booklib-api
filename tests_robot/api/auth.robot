*** Settings ***
Resource          ../resources/api/auth_keywords.robot

#Suite Setup       Setup User
#Suite Teardown    Cleanup User


*** Test Cases ***
Register User
    [Tags]    user    register
    ${payload}=    Create Dictionary    username=${TEST_USER}    email=${TEST_EMAIL}    password=${TEST_PASS}
    ${headers}=    Create Dictionary    Content-Type=application/json
    ${resp}=    POST    ${BASE_URL}/users/register    headers=${headers}    json=${payload}
    Should Be Equal As Integers    ${resp.status_code}    201

Login User
    [Tags]    user    login
    ${payload}=    Create Dictionary    username=${TEST_USER}    password=${TEST_PASS}
    ${resp}=    POST    ${BASE_URL}/users/login    json=${payload}
    Should Be Equal As Integers    ${resp.status_code}    200
    Set Global Variable    ${TOKEN}    ${resp.json()['access_token']}
    Set User Id From Api

Get All Users
    [Tags]    user  login
    ${headers}=    Create Dictionary    Authorization=Bearer ${TOKEN}
    ${resp}=    GET    ${BASE_URL}/users    headers=${headers}
    Should Be Equal As Integers    ${resp.status_code}    200
    ${users}=    Set Variable    ${resp.json()}
    Should Be True    isinstance(${users}, list)

Delete User
    [Tags]    user
    ${headers}=    Create Dictionary    Authorization=Bearer ${TOKEN}

    # Get user id after login to ensure token is set
    ${resp}=    GET    ${BASE_URL}/users    headers=${headers}
    ${users}=    Evaluate    [u for u in ${resp.json()} if u['username']=='${TEST_USER}']
    IF    not ${users}
        Fail    User ${TEST_USER} not found for deletion
    END
    ${USER_ID}=    Set Variable    ${users[0]['id']}
    ${resp}=    DELETE    ${BASE_URL}/users/${USER_ID}    headers=${headers}
    Should Be Equal As Integers    ${resp.status_code}    200
    Should Contain    ${resp.text}    User deleted


