BookLib API Use Cases
=====================

Add a Book
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

Enrich Book Info
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

---

Register a New User
-----------------------------
Actors
~~~~~~
- Visitor
- API Server

Pre-Conditions
~~~~~~~~~~~~~~
- Visitor is not registered

Basic Flow
~~~~~~~~~~
1. Visitor sends a POST request to `/users/register` with registration data.
2. API validates input and checks for existing user.
3. API creates a new user record and hashes the password.
4. API returns success message or JWT token.

Alternative/Exception Flows
~~~~~~~~~~~~~~~~~~~~~~~~~~~
- If user already exists, API returns a 400 error.
- If input is invalid, API returns a 400 error.

Post Conditions
~~~~~~~~~~~~~~~
- New user is registered and can log in.

---

Authenticate and Login
-------------------------------
Actors
~~~~~~
- User
- API Server

Pre-Conditions
~~~~~~~~~~~~~~
- User is registered

Basic Flow
~~~~~~~~~~
1. User sends a POST request to `/users/login` with credentials.
2. API validates credentials.
3. API issues a JWT token on success.

Alternative/Exception Flows
~~~~~~~~~~~~~~~~~~~~~~~~~~~
- If credentials are invalid, API returns a 401 error.

Post Conditions
~~~~~~~~~~~~~~~
- User receives JWT token for authenticated requests.

---

Update Book Information
---------------------------------
Actors
~~~~~~
- User (authenticated)
- API Server

Pre-Conditions
~~~~~~~~~~~~~~
- Book exists
- User is authenticated

Basic Flow
~~~~~~~~~~
1. User sends a PATCH/PUT request to `/books/{id}` with updated data.
2. API validates and applies changes.
3. API returns updated book info.

Alternative/Exception Flows
~~~~~~~~~~~~~~~~~~~~~~~~~~~
- If book does not exist, API returns a 404 error.
- If input is invalid, API returns a 400 error.

Post Conditions
~~~~~~~~~~~~~~~
- Book info is updated in the database.

---

Delete a Book
-----------------------
Actors
~~~~~~
- User (authenticated)
- API Server

Pre-Conditions
~~~~~~~~~~~~~~
- Book exists
- User is authenticated and authorized

Basic Flow
~~~~~~~~~~
1. User sends a DELETE request to `/books/{id}`.
2. API validates authorization and deletes the book.
3. API returns success message.

Alternative/Exception Flows
~~~~~~~~~~~~~~~~~~~~~~~~~~~
- If book does not exist, API returns a 404 error.
- If user is not authorized, API returns a 403 error.

Post Conditions
~~~~~~~~~~~~~~~
- Book and related data are removed from the database.

---

Add/Remove Tags to a Book
------------------------------------
Actors
~~~~~~
- User (authenticated)
- API Server

Pre-Conditions
~~~~~~~~~~~~~~
- Book exists
- User is authenticated

Basic Flow
~~~~~~~~~~
1. User sends a POST/DELETE request to `/books/{id}/tags` with tag data.
2. API adds or removes tags from the book.
3. API returns updated book info.

Alternative/Exception Flows
~~~~~~~~~~~~~~~~~~~~~~~~~~~
- If tag does not exist, API creates it.
- If book does not exist, API returns a 404 error.

Post Conditions
~~~~~~~~~~~~~~~
- Book's tags are updated in the database.

---

Add a Comment or Rating
----------------------------------
Actors
~~~~~~
- User (authenticated)
- API Server

Pre-Conditions
~~~~~~~~~~~~~~
- Book exists
- User is authenticated

Basic Flow
~~~~~~~~~~
1. User sends a POST request to `/books/{id}/comments` or `/books/{id}/ratings`.
2. API validates and stores the comment or rating.
3. API returns updated list of comments/ratings.

Alternative/Exception Flows
~~~~~~~~~~~~~~~~~~~~~~~~~~~
- If book does not exist, API returns a 404 error.
- If input is invalid, API returns a 400 error.

Post Conditions
~~~~~~~~~~~~~~~
- Comment or rating is stored and visible to other users.

---

Search for Books
--------------------------
Actors
~~~~~~
- User
- API Server

Pre-Conditions
~~~~~~~~~~~~~~
- Books exist in the database

Basic Flow
~~~~~~~~~~
1. User sends a GET request to `/books` with search parameters (title, author, tag).
2. API filters and returns matching books.

Alternative/Exception Flows
~~~~~~~~~~~~~~~~~~~~~~~~~~~
- If no books match, API returns an empty list.

Post Conditions
~~~~~~~~~~~~~~~
- User receives a list of matching books.

---

List Books by Tag/Genre
----------------------------------
Actors
~~~~~~
- User
- API Server

Pre-Conditions
~~~~~~~~~~~~~~
- Tags/genres exist

Basic Flow
~~~~~~~~~~
1. User sends a GET request to `/tags/{tag}/books`.
2. API returns books with the specified tag/genre.

Alternative/Exception Flows
~~~~~~~~~~~~~~~~~~~~~~~~~~~
- If tag does not exist, API returns a 404 error.

Post Conditions
~~~~~~~~~~~~~~~
- User receives a list of books for the tag/genre.

---

Plugin Management
---------------------------
Actors
~~~~~~
- Admin User
- API Server

Pre-Conditions
~~~~~~~~~~~~~~
- Admin is authenticated

Basic Flow
~~~~~~~~~~
1. Admin sends a POST/DELETE request to `/plugins` to add or remove plugins.
2. API updates plugin configuration.
3. API returns updated plugin list.

Alternative/Exception Flows
~~~~~~~~~~~~~~~~~~~~~~~~~~~
- If plugin is invalid, API returns a 400 error.

Post Conditions
~~~~~~~~~~~~~~~
- Plugin configuration is updated.

---

View Book Cover
-------------------------
Actors
~~~~~~
- User
- API Server

Pre-Conditions
~~~~~~~~~~~~~~
- Book has a cover image

Basic Flow
~~~~~~~~~~
1. User sends a GET request to `/books/{id}/cover`.
2. API returns the book cover image URL or binary data.

Alternative/Exception Flows
~~~~~~~~~~~~~~~~~~~~~~~~~~~
- If cover is missing, API returns a placeholder or error.

Post Conditions
~~~~~~~~~~~~~~~
- User can view the book cover image.

---

Admin Operations
--------------------------
Actors
~~~~~~
- Admin User
- API Server

Pre-Conditions
~~~~~~~~~~~~~~
- Admin is authenticated

Basic Flow
~~~~~~~~~~
1. Admin sends requests to manage users, books, tags, and plugins.
2. API validates permissions and performs requested operations.
3. API returns results or error messages.

Alternative/Exception Flows
~~~~~~~~~~~~~~~~~~~~~~~~~~~
- If admin is not authorized, API returns a 403 error.

Post Conditions
~~~~~~~~~~~~~~~
- Admin can manage all aspects of the system.
