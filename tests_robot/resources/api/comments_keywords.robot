*** Settings ***
Resource          ./variables.robot
Resource          ./keywords.robot
Resource          ./comments_variables.robot
Resource          ./books_variables.robot

*** Variables ***
${COMMENT_ID}    None

*** Keywords ***
Set Comment Id
    [Arguments]    ${comment_id}
    Set Global Variable    ${COMMENT_ID}    ${comment_id}

Setup Book For Comments
    Setup User
    ${headers}=    Create Dictionary    Authorization=Bearer ${TOKEN}    Content-Type=application/json
    ${resp}=    POST    ${BASE_URL}/books    headers=${headers}    json=&{BOOK_CREATE_PAYLOAD}
    Should Be Equal As Integers    ${resp.status_code}    201
    ${book_id}=    Set Variable    ${resp.json()['id']}
    Set Global Variable    ${BOOK_ID}    ${book_id}
