*** Settings ***
Resource          ../resources/api/variables.robot
Resource          ../resources/api/books_variables.robot
Resource          ../resources/api/books_keywords.robot
Resource          ../resources/api/keywords.robot

Suite Setup       Setup User
Suite Teardown    Cleanup User

*** Test Cases ***
Get All Books
    [Tags]    books    get
    ${headers}=    Create Dictionary    Authorization=Bearer ${TOKEN}
    ${resp}=    GET    ${BASE_URL}/books    headers=${headers}
    Should Be Equal As Integers    ${resp.status_code}    200
    ${books}=    Set Variable    ${resp.json()}
    Should Be True    isinstance(${books}, list)

Create Book
    [Tags]    books    create
    ${headers}=    Create Dictionary    Authorization=Bearer ${TOKEN}    Content-Type=application/json
    ${resp}=    POST    ${BASE_URL}/books    headers=${headers}    json=&{BOOK_CREATE_PAYLOAD}
    Should Be Equal As Integers    ${resp.status_code}    201
    ${book_id}=    Set Variable    ${resp.json()['id']}
    Set Global Variable    ${BOOK_ID}    ${book_id}

Get Book By Id
    [Tags]    books    get
    ${headers}=    Create Dictionary    Authorization=Bearer ${TOKEN}
    ${resp}=    GET    ${BASE_URL}/books/${BOOK_ID}    headers=${headers}
    Should Be Equal As Integers    ${resp.status_code}    200
    ${book}=    Set Variable    ${resp.json()}
    Should Be Equal    ${book['id']}    ${BOOK_ID}
    Should Be Equal    ${book['title']}    ${GET_BOOK_EXPECTED_TITLE}

Update Book
    [Tags]    books    update
    ${headers}=    Create Dictionary    Authorization=Bearer ${TOKEN}    Content-Type=application/json
    ${resp}=    PUT    ${BASE_URL}/books/${BOOK_ID}    headers=${headers}    json=&{BOOK_UPDATE_PAYLOAD}
    Should Be Equal As Integers    ${resp.status_code}    200
    ${resp_json}=    Set Variable    ${resp.json()}
    Should Be Equal    ${resp_json['msg']}    ${UPDATE_BOOK_EXPECTED_RESPONSE}

Get Book Full Info
    [Tags]    books    get    full
    ${headers}=    Create Dictionary    Authorization=Bearer ${TOKEN}
    ${resp}=    GET    ${BASE_URL}/books/${BOOK_ID}/full    headers=${headers}
    Should Be Equal As Integers    ${resp.status_code}    200
    ${book}=    Set Variable    ${resp.json()}
    Should Be Equal    ${book['id']}    ${BOOK_ID}
    Should Contain    ${book}    title
    Should Contain    ${book}    authors
    Should Contain    ${book}    cover_url
    Should Contain    ${book}    ratings
    Should Contain    ${book}    comments

Delete Book
    [Tags]    books    delete
    ${headers}=    Create Dictionary    Authorization=Bearer ${TOKEN}
    ${resp}=    DELETE    ${BASE_URL}/books/${BOOK_ID}    headers=${headers}
    Should Be Equal As Integers    ${resp.status_code}    200
    Should Contain    ${resp.text}    ${DELETE_BOOK_EXPECTED_RESPONSE}
