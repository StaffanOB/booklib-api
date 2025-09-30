*** Variables ***
&{BOOK_CREATE_PAYLOAD}                title=Robot Test Book    authors=[Test Author]    description=Test Description    cover_url=http://example.com/cover.jpg
${GET_BOOK_EXPECTED_TITLE}            Robot Test Book

&{BOOK_UPDATE_PAYLOAD}                title=Updated Robot Test Book    authors=[Updated Author]    description=Updated Description    cover_url=http://example.com/cover2.jpg
${UPDATE_BOOK_EXPECTED_TITLE}         Updated Robot Test Book
${UPDATE_BOOK_EXPECTED_RESPONSE}      Book updated

${DELETE_BOOK_EXPECTED_RESPONSE}      Book deleted
