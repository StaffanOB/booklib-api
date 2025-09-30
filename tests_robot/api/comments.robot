*** Settings ***
Resource          ../resources/api/variables.robot
Resource          ../resources/api/comments_variables.robot
Resource          ../resources/api/comments_keywords.robot

Suite Setup       Setup Book For Comments
Suite Teardown    Cleanup User


*** Test Cases ***
Get All Comments
    [Tags]    comments    get
    ${headers}=    Create Dictionary    Authorization=Bearer ${TOKEN}
    ${resp}=    GET    ${BASE_URL}/books/${BOOK_ID}/comments    headers=${headers}
    Should Be Equal As Integers    ${resp.status_code}    200
    ${comments}=    Set Variable    ${resp.json()}
    Should Be True    isinstance(${comments}, list)

Create Comment
    [Tags]    comments    create
    ${headers}=    Create Dictionary    Authorization=Bearer ${TOKEN}    Content-Type=application/json
    ${resp}=    POST    ${BASE_URL}/books/${BOOK_ID}/comments    headers=${headers}    json=&{COMMENT_CREATE_PAYLOAD}
    Should Be Equal As Integers    ${resp.status_code}    201
    ${comment_id}=    Set Variable    ${resp.json()['id']}
    Set Comment Id    ${comment_id}

Update Comment
    [Tags]    comments    update
    ${headers}=    Create Dictionary    Authorization=Bearer ${TOKEN}    Content-Type=application/json
    ${resp}=    PUT    ${BASE_URL}/books/${BOOK_ID}/comments/${COMMENT_ID}    headers=${headers}    json=&{COMMENT_UPDATE_PAYLOAD}
    Should Be Equal As Integers    ${resp.status_code}    200
    ${resp_json}=    Set Variable    ${resp.json()}
    Should Be Equal    ${resp_json['content']}    ${EXPECTED_UPDATED_COMMENT_CONTENT}

Delete Comment
    [Tags]    comments    delete
    ${headers}=    Create Dictionary    Authorization=Bearer ${TOKEN}
    ${resp}=    DELETE    ${BASE_URL}/books/${BOOK_ID}/comments/${COMMENT_ID}    headers=${headers}
    Should Be Equal As Integers    ${resp.status_code}    200
    Should Contain    ${resp.text}    ${COMMENT_DELETED_EXPECTED_RESPONSE}
