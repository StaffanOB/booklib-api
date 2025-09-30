*** Settings ***
Library           RequestsLibrary
Library           Collections

*** Variables ***
${BASE_URL}       http://127.0.0.1:5000
${TOKEN}          None

*** Test Cases ***
Create And Get Book
    [Tags]    books
    Create Session    bookapi    ${BASE_URL}
    &{book}=    Create Dictionary    title=Robot Test Book    author=Robot Author    description=Robot Description    publish_year=2025    series=Robot Series
    ${resp}=    POST    bookapi    /books    json=${book}    headers=    Authorization=Bearer ${TOKEN}
    Should Be Equal As Integers    ${resp.status_code}    201
    ${book_id}=    Set Variable    ${resp.json()['id']}
    ${resp}=    GET    bookapi    /books/${book_id}
    Should Be Equal As Integers    ${resp.status_code}    200
    Dictionary Should Contain Key    ${resp.json()}    title
    # Cleanup
    DELETE    bookapi    /books/${book_id}    headers=    Authorization=Bearer ${TOKEN}

Create And Get Book Full Info
    [Tags]    books
    Create Session    bookapi    ${BASE_URL}
    &{book}=    Create Dictionary    title=Robot Test Book    author=Robot Author
    ${resp}=    POST    bookapi    /books    json=${book}    headers=    Authorization=Bearer ${TOKEN}
    ${book_id}=    Set Variable    ${resp.json()['id']}
    ${resp}=    GET    bookapi    /books/${book_id}/full
    Should Be Equal As Integers    ${resp.status_code}    200
    Dictionary Should Contain Key    ${resp.json()}    ratings
    Dictionary Should Contain Key    ${resp.json()}    comments
    # Cleanup
    DELETE    bookapi    /books/${book_id}    headers=    Authorization=Bearer ${TOKEN}

Create And Get Tag
    [Tags]    tags
    Create Session    bookapi    ${BASE_URL}
    &{tag}=    Create Dictionary    name=RobotTag
    ${resp}=    POST    bookapi    /tags    json=${tag}    headers=    Authorization=Bearer ${TOKEN}
    Should Be Equal As Integers    ${resp.status_code}    201
    ${tag_id}=    Set Variable    ${resp.json()['id']}
    ${resp}=    GET    bookapi    /tags
    Should Be Equal As Integers    ${resp.status_code}    200
    # Cleanup
    DELETE    bookapi    /tags/${tag_id}    headers=    Authorization=Bearer ${TOKEN}

Create And Get User
    [Tags]    users
    Create Session    bookapi    ${BASE_URL}
    &{user}=    Create Dictionary    username=robotuser    email=robotuser@example.com    password=robotpw
    ${resp}=    POST    bookapi    /users/register    json=${user}
    Should Be Equal As Integers    ${resp.status_code}    201
    ${resp}=    GET    bookapi    /users
    Should Be Equal As Integers    ${resp.status_code}    200

Create And Get Rating
    [Tags]    ratings
    Create Session    bookapi    ${BASE_URL}
    &{book}=    Create Dictionary    title=Rating Book    author=Rating Author
    ${resp}=    POST    bookapi    /books    json=${book}    headers=    Authorization=Bearer ${TOKEN}
    ${book_id}=    Set Variable    ${resp.json()['id']}
    &{rating}=    Create Dictionary    rating=5
    ${resp}=    POST    bookapi    /books/${book_id}/ratings    json=${rating}    headers=    Authorization=Bearer ${TOKEN}
    Should Be Equal As Integers    ${resp.status_code}    201
    ${resp}=    GET    bookapi    /books/${book_id}/ratings
    Should Be Equal As Integers    ${resp.status_code}    200
    # Cleanup
    DELETE    bookapi    /books/${book_id}    headers=    Authorization=Bearer ${TOKEN}

Create And Get Comment
    [Tags]    comments
    Create Session    bookapi    ${BASE_URL}
    &{book}=    Create Dictionary    title=Comment Book    author=Comment Author
    ${resp}=    POST    bookapi    /books    json=${book}    headers=    Authorization=Bearer ${TOKEN}
    ${book_id}=    Set Variable    ${resp.json()['id']}
    &{comment}=    Create Dictionary    content=Robot comment
    ${resp}=    POST    bookapi    /books/${book_id}/comments    json=${comment}    headers=    Authorization=Bearer ${TOKEN}
    Should Be Equal As Integers    ${resp.status_code}    201
    ${resp}=    GET    bookapi    /books/${book_id}/comments
    Should Be Equal As Integers    ${resp.status_code}    200
    # Cleanup
    DELETE    bookapi    /books/${book_id}    headers=    Authorization=Bearer ${TOKEN}
