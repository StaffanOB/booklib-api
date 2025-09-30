*** Settings ***
Library           RequestsLibrary
Resource          ./variables.robot

*** Keywords ***
Register User
    ${payload}=    Create Dictionary    username=${TEST_USER}    email=${TEST_EMAIL}    password=${TEST_PASS}
    ${headers}=    Create Dictionary    Content-Type=application/json
    ${resp}=    POST    ${BASE_URL}/users/register    headers=${headers}    json=${payload}
    Should Be Equal As Integers    ${resp.status_code}    201

Login User
    ${payload}=    Create Dictionary    username=${TEST_USER}    password=${TEST_PASS}
    ${resp}=    POST    ${BASE_URL}/users/login    json=${payload}
    Should Be Equal As Integers    ${resp.status_code}    200
    Set Global Variable    ${TOKEN}    ${resp.json()['access_token']}
    Set User Id From Api

Delete User
    ${headers}=    Create Dictionary    Authorization=Bearer ${TOKEN}
    ${resp}=    DELETE    ${BASE_URL}/users/${USER_ID}    headers=${headers}
    Should Be Equal As Integers    ${resp.status_code}    200
    Should Contain    ${resp.text}    User deleted


Set User Id From Api
    ${headers}=    Create Dictionary    Authorization=Bearer ${TOKEN}
    ${resp}=    GET    ${BASE_URL}/users    headers=${headers}
    ${users}=    Evaluate    [u for u in ${resp.json()} if u['username']=='${TEST_USER}']
    IF    not ${users}
        Fail    User testuser not found for id lookup
    END
    Set Global Variable    ${USER_ID}    ${users[0]['id']}