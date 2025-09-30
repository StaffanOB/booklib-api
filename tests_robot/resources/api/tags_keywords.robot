*** Variables ***
${TAG_ID}    None

*** Keywords ***
Set Tag Id
    [Arguments]    ${tag_id}
    Set Global Variable    ${TAG_ID}    ${tag_id}
