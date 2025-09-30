*** Variables ***
&{TAG_CREATE_PAYLOAD}              name=Robot Test Tag    description=Test Tag Description
${EXPECTED_TAG_NAME}               Robot Test Tag

&{TAG_UPDATE_PAYLOAD}              name=Updated Robot Test Tag    description=Updated Tag Description
${EXPECTED_UPDATED_TAG_NAME}       Updated Robot Test Tag
${UPDATE_TAG_EXPECTED_RESPONSE}    Updated Robot Test Tag

${DELETE_TAG_EXPECTED_RESPONSE}    Tag deleted