*** Variables ***
${BOOK_ID}    None

*** Keywords ***
Set Book Id
    [Arguments]    ${book_id}
    Set Global Variable    ${BOOK_ID}    ${book_id}
