*** Settings ***
Resource          ../resources/api/variables.robot
Resource          ../resources/api/tags_keywords.robot
Resource          ../resources/api/tags_variables.robot
Resource          ../resources/api/keywords.robot

Suite Setup       Setup User
Suite Teardown    Cleanup User

*** Test Cases ***
Get All Tags
    [Tags]    tags    get
    ${headers}=    Create Dictionary    Authorization=Bearer ${TOKEN}
    ${resp}=    GET    ${BASE_URL}/tags    headers=${headers}
    Should Be Equal As Integers    ${resp.status_code}    200
    ${tags}=    Set Variable    ${resp.json()}
    Should Be True    isinstance(${tags}, list)

Create Tag
    [Tags]    tags    create
    ${headers}=    Create Dictionary    Authorization=Bearer ${TOKEN}    Content-Type=application/json
    ${resp}=    POST    ${BASE_URL}/tags    headers=${headers}    json=&{TAG_CREATE_PAYLOAD}
    Should Be Equal As Integers    ${resp.status_code}    201
    ${tag_id}=    Set Variable    ${resp.json()['id']}
    Set Tag Id    ${tag_id}


Update Tag
    [Tags]    tags    update
    ${headers}=    Create Dictionary    Authorization=Bearer ${TOKEN}    Content-Type=application/json
    ${resp}=    PUT    ${BASE_URL}/tags/${TAG_ID}    headers=${headers}    json=&{TAG_UPDATE_PAYLOAD}
    Should Be Equal As Integers    ${resp.status_code}    200
    ${resp_json}=    Set Variable    ${resp.json()}
    Should Be Equal    ${resp_json['name']}    ${UPDATE_TAG_EXPECTED_RESPONSE}

Delete Tag
    [Tags]    tags    delete
    ${headers}=    Create Dictionary    Authorization=Bearer ${TOKEN}
    ${resp}=    DELETE    ${BASE_URL}/tags/${TAG_ID}    headers=${headers}
    Should Be Equal As Integers    ${resp.status_code}    200
    Should Contain    ${resp.text}    ${DELETE_TAG_EXPECTED_RESPONSE}
