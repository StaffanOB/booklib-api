````rst
BookLib API Use Cases
======================

Use Case: Add a Book
--------------------

Actors
~~~~~~
- User (authenticated)
- API Server

Pre-Conditions
~~~~~~~~~~~~~~
- User is registered and logged in
- User has a valid JWT token

Basic Flow
~~~~~~~~~~
1. User sends a POST request to `/books` with book data (title, authors, description, etc.) and JWT token in the header.
2. API validates the request and checks for required fields.
3. API creates a new book record in the database.
4. API returns the new book's ID and details in the response.

Alternative/Exception Flows
~~~~~~~~~~~~~~~~~~~~~~~~~~~
- If required fields are missing, API returns a 400 error with a message.
- If the book already exists (same title and authors), API returns a 400 error.
- If the JWT token is invalid or missing, API returns a 401 error.

Post Conditions
~~~~~~~~~~~~~~~
- New book is stored in the database and linked to the user (if applicable).
- Book is available for further actions (enrichment, comments, ratings).

Supplemental Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~
- All input must be validated and sanitized.
- Book must be unique by title and authors.
- API must log the creation event for audit purposes.

Visual Model
~~~~~~~~~~~~
::

   User -> API: POST /books
   API -> DB: Create Book
   API -> User: Return Book ID

---

Use Case: Enrich Book Info
--------------------------

Actors
~~~~~~
- User (authenticated)
- API Server
- External Plugin (Google Books, Open Library)

Pre-Conditions
~~~~~~~~~~~~~~
- Book exists in the database
- User is authenticated

Basic Flow
~~~~~~~~~~
1. User sends a POST request to `/books/{id}/recheck` with plugin selection and JWT token.
2. API calls the selected plugin to fetch external book data.
3. API updates the book record with enriched info (title, authors, cover, genres).
4. API adds new genres as tags if not already present.
5. API returns updated book info.

Alternative/Exception Flows
~~~~~~~~~~~~~~~~~~~~~~~~~~~
- If plugin fails or rate limit is hit, API returns an error message.
- If book does not exist, API returns a 404 error.

Post Conditions
~~~~~~~~~~~~~~~
- Book info is updated and genres are reflected as tags.

Supplemental Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~
- API must handle plugin errors gracefully.
- All enriched data must be validated before updating the database.

Visual Model
~~~~~~~~~~~~
::

   User -> API: POST /books/{id}/recheck
   API -> Plugin: Fetch Data
   API -> DB: Update Book
   API -> User: Return Updated Info
````