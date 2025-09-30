*** Settings ***
Library           RequestsLibrary
Library           Collections

*** Variables ***
${BASE_URL}       http://127.0.0.1:5000
${TOKEN}          None

*** Test Cases ***
Book Info Schema Is Complete
    [Tags]    books
    Create Session    bookapi    ${BASE_URL}
    &{book}=    Create Dictionary    title=Robot Test Book    author=Robot Author    description=Robot Description    publish_year=2025    series=Robot Series
    ${resp}=    POST    bookapi    /books    json=${book}    headers=    Authorization=Bearer ${TOKEN}
    Should Be Equal As Integers    ${resp.status_code}    201
    ${book_id}=    Set Variable    ${resp.json()['id']}
    ${resp}=    GET    bookapi    /books
    Should Be Equal As Integers    ${resp.status_code}    200
    ${books}=    Evaluate    [b for b in ${resp.json()} if b['id'] == ${book_id}]
    Length Should Be    ${books}    1
    ${book}=    Get From List    ${books}    0
    Dictionary Should Contain Key    ${book}    id
    Dictionary Should Contain Key    ${book}    title
    Dictionary Should Contain Key    ${book}    author
    Dictionary Should Contain Key    ${book}    description
    Dictionary Should Contain Key    ${book}    publish_year
    Dictionary Should Contain Key    ${book}    series
    Dictionary Should Contain Key    ${book}    is_active
    Should Be Equal    ${book['title']}    Robot Test Book
    Should Be Equal    ${book['author']}    Robot Author
    Should Be Equal    ${book['description']}    Robot Description
    Should Be Equal As Integers    ${book['publish_year']}    2025
    Should Be Equal    ${book['series']}    Robot Series
    Should Be True    ${book['is_active']}
    # Cleanup
    DELETE    bookapi    /books/${book_id}    headers=    Authorization=Bearer ${TOKEN}
