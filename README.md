# Estate Planning Software

## Project Name

EstateTrust

## Project Description

EstateTrust is a specialized tool designed to help individuals and professionals create and manage their estate plans. It involves making arrangements for the distribution of assets, care of dependents, and other important decisions after a person passes away or becomes incapacitated. It can simplify the process and ensure that your wishes are documented correctly.

## Objectives

Our main objectives of the developing estate planning management system software (EPS) are:

- Address issues that arise during reading of wills after the person passes away or becomes incapacitated.
- Distribution of assets.
- Care of dependents.

## Technologies Used

- Programming Language: Python
- Web Framework: FastAPI
- Frontend Technologies: CSS3, HTML5, JavaScript and ReactJs
- Database Technology: PostgreSQL
- Deployment And Hosting: Docker, Ubuntu linux machine and Nginx for web server
- Logging And Monitoring: Prometheus
- Version Control: Git
- CI/CD Pipeline: GitLab

## Challenges

- Legal And Regulatory Complexity
- Documents Accuracy
- Assets Valuation
- Beneficiary Designations

## How To Run EstateTrust Application

Running a FastAPI application involves a few steps, including setting up the environment, defining your application, and starting the development server. Here are the steps to run a FastAPI application:

1. **Set Up Your Environment:**

   Before running a FastAPI application, ensure you have Python and the required dependencies installed. You can use a virtual environment to manage dependencies to avoid conflicts with other projects. Here's how to create and activate a virtual environment using Python's built-in `venv` module:

   ```bash
   # Create a virtual environment
   python -m venv myenv

   # Activate the virtual environment (on Windows)
   myenv\Scripts\activate

   # Activate the virtual environment (on macOS/Linux)
   source myenv/bin/activate
   ```

   Replace `myenv` with the name you prefer for your virtual environment.

2. **Install FastAPI and Dependencies:**

   Inside your activated virtual environment, you should install FastAPI and any additional dependencies your application requires. You can use `pip` to install them:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Development Server:**

   FastAPI provides a built-in development server, but you can also use ASGI servers like Uvicorn for production. To run your FastAPI application using the development server, use the following command inside the EstateTrust directory:

   ```bash
   uvicorn api.v1.main:app --reload
   ```

   The `--reload` flag enables automatic code reloading during development, making it easier to see changes immediately.

4. **Access EstateTrust Application:**

   Once your FastAPI application is running, you can access it by opening a web browser or making HTTP requests to the specified endpoints. By default, the development server runs on `http://localhost:8000`.

5. **Stopping the Development Server:**

   To stop the development server, you can use `Ctrl+C` in the terminal where the server is running.

6. **Production Deployment:**

   For production deployment, it's recommended to use ASGI servers like Uvicorn, Hypercorn, or Gunicorn. These servers provide better performance and reliability. You can refer to the documentation of these servers for deployment instructions specific to your environment.

## APIs Routes And Documentation

## Users API Documentation

This API documentation provides information about the Users API routes for the "Estate Trust" application. The API allows users to create accounts, log in, access their dashboards, update their accounts, and delete their accounts.

## Base URL

All endpoints are relative to the base URL: `/grantors`.

## Authentication

Authentication is required for certain endpoints. The API uses OAuth for user authentication. Users must obtain an access token to access authenticated endpoints. To obtain an access token, users should log in using the `/account/login` endpoint.

## Create Grantor Account

### `POST /account/create`

Create a grantor account.

**Request Body**

- `grantor` (object): An object that contains the account information, including:
  - `first_name` (string): The first name for the account.
  - `last_name` (string): The last name for the account.
  - `middle_name` (string): The middle name for the account.
  - `username` (string): The username for the account.
  - `password` (string): The password for the account.
  - `email`: (string): The email address for the account,
  - `phone_number` (string): The phone number for the account.
  - `date_of_birth` (date): The date of birth for the account.
  - `gender` (string): The gender for the account.

**Response**

- `201 Created`: The account was created successfully.
  - `status_code` (integer): 201
  - `message` (string): "Account created successfully"

- `422 Unprocessable Entity`: An error occurred while creating the account.

## Login

### `POST /account/login`

Log in a user.

**Request Body**

- `data` (object): An object that contains the login information, including:
  - `username` (string): The username of the user.
  - `password` (string): The password of the user.

**Response**

- `200 OK`: The user was successfully logged in.
  - `access_token` (string): The access token for the user.
  - `token_type` (string): "bearer"

- `401 Unauthorized`: Invalid credentials provided.

## Retrieve Grantor's Dashboard

### `GET /account/dashboard/{uuid_pk}`

Retrieve the grantor's dashboard.

**Path Parameters**

- `uuid_pk` (string): The UUID unique identification of the user's account.

**Request Headers**

- `Authorization` (string): The access token obtained during login.

**Response**

- `200 OK`: The grantor's dashboard information.
  - `uuid_pk` (string): The UUID of the grantor.
  - Other user information.

- `404 Not Found`: User not found.
- `403 Forbidden`: Access denied if the requested UUID does not match the authenticated user's UUID.

**Response Example**

```json
{
  "uuid_pk": "43725e17-72d5-4def-be70-91accfe2009a",
  "username": "cBolton",
  "first_name": "Who",
  "middle_name": "Emmanuel",
  "last_name": "Ejobe",
  "email": "triplee12@gmail.com",
  "phone_number": "+2348153836253",
  "date_of_birth": "2000-07-18",
  "gender": "male",
  "created_at": "2023-10-03T11:49:29.118054+01:00",
  "beneficiaries": [],
  "executors": [
    {
      "uuid_pk": "d55b069e-dda1-4732-b110-8fcfdc3b10ec",
      "username": "username",
      "first_name": "Trustee1",
      "middle_name": "Mytrustee",
      "last_name": "Trustee",
      "email": "mytrustee@gmail.com",
      "phone_number": "12345678901",
      "relation": "lawyer",
      "added_by": "43725e17-72d5-4def-be70-91accfe2009a",
      "created_at": "2023-10-03T11:52:27.286994+01:00"
    }
  ],
  "assets": [],
  "monetaries": []
}
```

## Update Grantor Account

### `PUT /account/dashboard/{uuid_pk}/update`

Update the grantor's account.

**Path Parameters**

- `uuid_pk` (string): The UUID of the user's account.

**Request Headers**

- `Authorization` (string): The access token obtained during login.

**Request Body**

- `data` (object): An object that contains the account information to be updated.

**Response**

- `200 OK`: The updated grantor account information.
  - User information with changes applied.

- `422 Unprocessable Entity`: Error updating the account.
- `403 Forbidden`: Access denied if the requested UUID does not match the authenticated user's UUID.

## Delete User Account

### `DELETE /account/dashboard/{uuid_pk}/delete`

Delete a user account.

**Path Parameters**

- `uuid_pk` (string): The UUID of the user's account.

**Request Headers**

- `Authorization` (string): The access token obtained during login.

**Response**

- `204 No Content`: The account was successfully deleted.

- `422 Unprocessable Entity`: Error deleting the account.
- `403 Forbidden`: Access denied if the requested UUID does not match the authenticated user's UUID.

## Estate Trust Trustees API Documentation

This API documentation provides information about the endpoints and functionality of the Estate Trust Trustees API. This API allows users to manage trustees associated with an estate trust account. Users can create, retrieve, update, and delete trustees, as well as login as a trustee and access the trustee's dashboard.

## Table of Contents

1. [Create a New Trustee](#create-a-new-trustee)
2. [Retrieve a Specific Trustee](#retrieve-a-specific-trustee)
3. [Retrieve List of Trustees](#retrieve-list-of-trustees)
4. [Update Trustee Account](#update-trustee-account)
5. [Delete Trustee Account](#delete-trustee-account)
6. [Login as a Trustee](#login-as-a-trustee)
7. [Trustee Dashboard](#trustee-dashboard)

### Base URL

The base URL for all API endpoints is `/trustees`.

### Authentication

Some endpoints require authentication using OAuth 2.0. Authentication tokens should be included in the request headers for those endpoints. Refer to the OAuth 2.0 documentation for details on obtaining and using authentication tokens.

---

### 1. Create a New Trustee <a name="create-a-new-trustee"></a>

Create a new trustee associated with a grantor (estate owner).

- **HTTP Method:** POST
- **Endpoint:** `/account/{grantor_id}/create/trustees`
- **Request Body:** [AddTrustee](#addtrustee-request-body)
- **Response:** HTTP 201 Created on success, with a success message.

#### Request Body (AddTrustee) <a name="addtrustee-request-body"></a>

```json
{
  "first_name": "string",
  "last_name": "string",
  "middle_name": "string",
  "phone_number": "string",
  "email": "string",
  "username": "string",
  "password": "string",
  "relation": "string",
  "note": "string"
}
```

- `first_name` (string): The first name of the new trustee.
- `last_name` (string): The last name of the new trustee.
- `middle_name` (string): The middle name of the new trustee.
- `username` (string): The username of the new trustee.
- `password` (string): The password of the new trustee.
- `email`: (string): The email address of the new trustee.
- `phone_number` (string): The phone number of the new trustee.
- `relation` (string): The relationship between grantor and the new trustee.
- `note` (string): The note that shows the grantor's intake on the new trustee.

#### Example Request

```http
POST /trustees/account/{grantor_id}/create/trustees
```

#### Example Response

```json
{
  "message": "Trustee added successfully"
}
```

---

### 2. Retrieve a Specific Trustee <a name="retrieve-a-specific-trustee"></a>

Retrieve information about a specific trustee associated with a grantor.

- **HTTP Method:** GET
- **Endpoint:** `/account/{grantor_id}/trustees/{trustee_id}`
- **Response:** [TrusteeRes](#trusteerres-response-model) on success.

#### Example Request

```http
GET /trustees/account/{grantor_id}/trustees/{trustee_id}
```

#### Example Response

```json
{
  "uuid_pk": "string",
  "username": "string",
  ...
}
```

#### Response Model (TrusteeRes) <a name="trusteerres-response-model"></a>

```json
{
  "uuid_pk": "string",
  "username": "string",
  ...
}
```

---

### 3. Retrieve List of Trustees <a name="retrieve-list-of-trustees"></a>

Retrieve a list of trustees associated with a grantor.

- **HTTP Method:** GET
- **Endpoint:** `/account/{grantor_id}/trustees`
- **Response:** List of [TrusteeRes](#trusteerres-response-model) on success.

#### Example Request

```http
GET /trustees/account/{grantor_id}/trustees
```

#### Example Response

```json
[
  {
    "uuid_pk": "string",
    "username": "string",
    ...
  },
  ...
]
```

---

### 4. Update Trustee Account <a name="update-trustee-account"></a>

Update the information of a specific trustee associated with a grantor.

- **HTTP Method:** PUT
- **Endpoint:** `/account/{grantor_id}/trustees/{trustee_id}/update`
- **Request Body:** [UpdateTrustee](#updatetrustee-request-body)
- **Response:** [TrusteeRes](#trusteerres-response-model) on success.

#### Request Body (UpdateTrustee) <a name="updatetrustee-request-body"></a>

```json
{
  "username": "string",
  ...
}
```

- `username` (string, optional): The updated username for the trustee.

#### Example Request

```http
PUT /trustees/account/{grantor_id}/trustees/{trustee_id}/update
```

#### Example Response

```json
{
  "uuid_pk": "string",
  "username": "string",
  ...
}
```

---

### 5. Delete Trustee Account <a name="delete-trustee-account"></a>

Delete a trustee account associated with a grantor.

- **HTTP Method:** DELETE
- **Endpoint:** `/account/{grantor_id}/trustees/{trustee_id}/delete`
- **Response:** HTTP 204 No Content on successful deletion.

#### Example Request

```http
DELETE /trustees/account/{grantor_id}/trustees/{trustee_id}/delete
```

---

### 6. Login as a Trustee <a name="login-as-a-trustee"></a>

Login as a trustee to obtain an access token for authentication.

- **HTTP Method:** POST
- **Endpoint:** `/account/trustee/login`
- **Request Body:** [SignInUser](#signinuser-request-body)
- **Response:** Access token and token type on successful login.

#### Request Body (SignInUser) <a name="signinuser-request-body"></a>

```json
{
  "username": "string",
  "password": "string"
}
```

- `username` (string, required): The username of the trustee.
- `password` (string, required): The password of the trustee.

#### Example Request

```http
POST /trustees/account/trustee/login
```

#### Example Response

```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

---

### 7. Trustee Dashboard <a name="trustee-dashboard"></a>

Access the trustee dashboard with unlimited access.

- **HTTP Method:** GET
- **Endpoint:** `/account/trustee/{trustee_id}/dashboard`
- **Response:** [TrusteeRes](#trusteerres-response-model) on success.

#### Example Request

```http
GET /trustees/account/trustee/{trustee_id}/dashboard
```

#### Example Response

```json
{
  "uuid_pk": "string",
  "username": "string",
  ...
}
```

---

That concludes the documentation for the Estate Trust Trustees API. For authentication and further details, please refer to the OAuth 2.0 documentation and specific endpoint documentation above.

## API Documentation for Beneficiaries Router

This API documentation provides information on how to use the "Beneficiaries" endpoints of the Estate Trust application. These endpoints allow users to manage beneficiaries associated with their accounts.

## Table of Contents

1. [Create Beneficiary](#create-beneficiary)
2. [Retrieve Beneficiaries](#retrieve-beneficiaries)
3. [Retrieve Beneficiary](#retrieve-beneficiary)
4. [Update Beneficiary](#update-beneficiary)
5. [Delete Beneficiary](#delete-beneficiary)

### Create Beneficiary <a name="create-beneficiary"></a>

- **Endpoint**: `/beneficiaries/account/{grantor_id}/create/beneficiary`
- **HTTP Method**: POST
- **Description**: Add a new beneficiary to the database.
- **Parameters**:
  - `grantor_id` (string): ID of the grantor (account owner).
  - `data` (object): JSON object containing beneficiary's information.
- **Request Headers**:
  - `Authorization` (string): OAuth2 Bearer Token for authentication.
- **Response**:
  - **Success**:
    - **Status Code**: 201 Created
    - **Response Body**: JSON object with a success message.
      ```json
      {
          "message": "Beneficiary added successfully"
      }
      ```
  - **Failure**:
    - **Status Code**: 422 Unprocessable Entity
    - **Response Body**: Error message indicating the failure reason.

#### Example Request

  ```json
    {
      "first_name": "string",
      "last_name": "string",
      "middle_name": "string",
      "relation": "string"
    }
  ```

### Retrieve Beneficiaries <a name="retrieve-beneficiaries"></a>

- **Endpoint**: `/beneficiaries/account/{user_id}/beneficiaries`
- **HTTP Method**: GET
- **Description**: Retrieve all beneficiaries associated with a given grantor's account.
- **Parameters**:
  - `user_id` (string): ID of the grantor (account owner).
- **Request Headers**:
  - `Authorization` (string): OAuth2 Bearer Token for authentication.
- **Response**:
  - **Success**:
    - **Status Code**: 200 OK
    - **Response Body**: JSON array containing beneficiary information in the form of objects.
  - **Failure**:
    - **Status Code**: 204 No Content
    - **Response Body**: No beneficiaries found message.

### Retrieve Beneficiary <a name="retrieve-beneficiary"></a>

- **Endpoint**: `/beneficiaries/account/{user_id}/beneficiary/{bene_id}`
- **HTTP Method**: GET
- **Description**: Retrieve information about a specific beneficiary for a given grantor's account.
- **Parameters**:
  - `user_id` (string): ID of the grantor (account owner).
  - `bene_id` (string): ID of the beneficiary to retrieve.
- **Request Headers**:
  - `Authorization` (string): OAuth2 Bearer Token for authentication.
- **Response**:
  - **Success**:
    - **Status Code**: 200 OK
    - **Response Body**: JSON object containing beneficiary information.
  - **Failure**:
    - **Status Code**: 404 Not Found
    - **Response Body**: Beneficiary not found message.

### Update Beneficiary <a name="update-beneficiary"></a>

- **Endpoint**: `/beneficiaries/account/{grantor_id}/beneficiary/{bene_id}/update`
- **HTTP Method**: PUT
- **Description**: Update beneficiary data in the database.
- **Parameters**:
  - `grantor_id` (string): ID of the grantor (account owner).
  - `bene_id` (string): ID of the beneficiary to update.
  - `data` (object): JSON object containing beneficiary's data to update.
- **Request Headers**:
  - `Authorization` (string): OAuth2 Bearer Token for authentication.
- **Response**:
  - **Success**:
    - **Status Code**: 200 OK
    - **Response Body**: JSON object containing updated beneficiary information.
  - **Failure**:
    - **Status Code**: 304 Not Modified
    - **Response Body**: Error message indicating the update failure reason.

### Delete Beneficiary <a name="delete-beneficiary"></a>

- **Endpoint**: `/beneficiaries/account/{grantor_id}/beneficiary/{bene_id}/delete`
- **HTTP Method**: DELETE
- **Description**: Delete a beneficiary from the database.
- **Parameters**:
  - `grantor_id` (string): ID of the grantor (account owner).
  - `bene_id` (string): ID of the beneficiary to delete.
- **Request Headers**:
  - `Authorization` (string): OAuth2 Bearer Token for authentication.
- **Response**:
  - **Success**:
    - **Status Code**: 204 No Content
    - **Response Body**: No content.
  - **Failure**:
    - **Status Code**: 304 Not Modified
    - **Response Body**: Error message indicating the deletion failure reason.

---

This API documentation provides a guide to using the "Beneficiaries" endpoints of the Estate Trust application. Ensure you have the necessary authentication token and provide valid data when making requests to these endpoints.

## Estate Trust Assets API Documentation

This documentation provides information on how to use the Estate Trust Assets API. The API allows users to manage assets, including creating, retrieving, updating, and deleting assets for specific grantors and beneficiaries.

## Base URL

The base URL for all API endpoints is `/assets`.

## Authentication

All endpoints require authentication. Users must be authenticated to access these endpoints.

## API Endpoints

### Create Asset

- **Endpoint**: `POST /{grantor_id}/create/asset`
- **Description**: Add an asset to the database.
- **Request Parameters**:
  - `grantor_id` (string, path): The ID of the grantor for whom the asset will be created.
- **Request Body**:
  - `data` (object, JSON): Object that contains the asset information. It should follow the schema specified in the `AddAsset` model.
- **Response**:
  - Status code 201 (Created) on success.
  - Status code 422 (Unprocessable Entity) on failure.
- **Example Request**:
  ```http
  POST /assets/{grantor_id}/create/asset
  Content-Type: application/json

  {
    "name": "Asset Name",
    "description": "Asset Description",
    "value": 100000
  }
  ```
- **Example Response** (HTTP 201 Created):
  ```json
  {
    "message": "Asset added successfully"
  }
  ```

### Retrieve Assets for Grantor

- **Endpoint**: `GET /grantor/{grantor_id}/assets`
- **Description**: Retrieve all assets for a specific grantor.
- **Request Parameters**:
  - `grantor_id` (string, path): The ID of the grantor for whom assets will be retrieved.
- **Response**:
  - Status code 200 (OK) on success with a list of assets.
  - Status code 204 (No Content) if no assets are found.
- **Example Request**:
  ```http
  GET /assets/grantor/{grantor_id}/assets
  ```
- **Example Response** (HTTP 200 OK):
  ```json
  [
    {
      "name": "Asset Name 1",
      "description": "Asset Description 1",
      "value": 100000
    },
    {
      "name": "Asset Name 2",
      "description": "Asset Description 2",
      "value": 75000
    }
  ]
  ```

### Retrieve Assets for Beneficiary

- **Endpoint**: `GET /beneficiary/{bene_id}/assets`
- **Description**: Retrieve all assets for a specific beneficiary.
- **Request Parameters**:
  - `bene_id` (string, path): The ID of the beneficiary for whom assets will be retrieved.
- **Response**:
  - Status code 200 (OK) on success with a list of assets.
  - Status code 204 (No Content) if no assets are found.
- **Example Request**:
  ```http
  GET /assets/beneficiary/{bene_id}/assets
  ```
- **Example Response** (HTTP 200 OK):
  ```json
  [
    {
      "name": "Asset Name 1",
      "description": "Asset Description 1",
      "value": 100000
    },
    {
      "name": "Asset Name 2",
      "description": "Asset Description 2",
      "value": 75000
    }
  ]
  ```

### Retrieve Asset

- **Endpoint**: `GET /{grantor_id}/assets/{asset_id}`
- **Description**: Retrieve a specific asset.
- **Request Parameters**:
  - `grantor_id` (string, path): The ID of the grantor who owns the asset.
  - `asset_id` (string, path): The ID of the asset to retrieve.
- **Response**:
  - Status code 200 (OK) on success with the asset details.
  - Status code 404 (Not Found) if the asset is not found.
- **Example Request**:
  ```http
  GET /assets/{grantor_id}/assets/{asset_id}
  ```
- **Example Response** (HTTP 200 OK):
  ```json
  {
    "name": "Asset Name",
    "description": "Asset Description",
    "value": 100000
  }
  ```

### Update Asset

- **Endpoint**: `PUT /{grantor_id}/assets/{asset_id}/update`
- **Description**: Update a specific asset.
- **Request Parameters**:
  - `grantor_id` (string, path): The ID of the grantor who owns the asset.
  - `asset_id` (string, path): The ID of the asset to update.
- **Request Body**:
  - `data` (object, JSON): Object that contains the updated asset information. It should follow the schema specified in the `UpdateAsset` model.
- **Response**:
  - Status code 200 (OK) on success with the updated asset details.
  - Status code 304 (Not Modified) if the asset is not modified.
- **Example Request**:
  ```http
  PATCH /assets/{grantor_id}/assets/{asset_id}/update
  Content-Type: application/json

  {
    "name": "Updated Asset Name",
    "description": "Updated Asset Description",
    "value": 150000
  }
  ```
- **Example Response** (HTTP 200 OK):
  ```json
  {
    "name": "Updated Asset Name",
    "description": "Updated Asset Description",
    "value": 150000
  }
  ```

### Delete Asset

- **Endpoint**: `DELETE /{grantor_id}/assets/{asset_id}/delete`
- **Description**: Delete a specific asset.
- **Request Parameters**:
  - `grantor_id` (string, path): The ID of the grantor who owns the asset.
  - `asset_id` (string, path): The ID of the asset to delete.
- **Response**:
  - Status code 204 (No Content) on success.
  - Status code 304 (Not Modified) if the asset is not deleted.
- **Example Request**:
  ```http
  DELETE /assets/{grantor_id}/assets/{asset_id}/delete
  ```
- **Example Response** (HTTP 204 No Content):
  No content is returned on successful deletion.

## Error Responses

In case of an error, the API will return a JSON response with an error message and an appropriate HTTP status code.

Example Error Response (HTTP 404 Not Found):
```json
{
  "detail": "Asset not found"
}
```

## Conclusion

This documentation provides an overview of the Estate Trust Assets API and its endpoints. Users can create, retrieve, update, and delete assets for specific grantors and beneficiaries using these endpoints.

## API Documentation for the Monetaries Router

This API documentation provides information about the Monetaries Router for the "Estate Trust" application. The Monetaries Router is responsible for managing monetary assets and provides endpoints for creating, retrieving, updating, and deleting these assets.

## Base URL

The base URL for all endpoints in this API is `/monetaries`.

## Authentication

Authentication is required for most endpoints in this API. Users must obtain a valid OAuth token to access these endpoints. The `get_current_user` function is used to authenticate users.

## Error Handling

Errors in this API are communicated through HTTP status codes and JSON response bodies. Common status codes include:
- 200 OK: Successful operation
- 201 Created: Resource successfully created
- 204 No Content: Resource not found or deleted
- 304 Not Modified: Error occurred while processing the request
- 400 Bad Request: Invalid request data
- 401 Unauthorized: Authentication required
- 404 Not Found: Resource not found
- 422 Unprocessable Entity: Error occurred while processing the request

## Endpoints

### 1. Create a New Monetary Asset

- **HTTP Method:** POST
- **Endpoint:** `/monetaries/asset/{grantor_id}/create/monetary`
- **Parameters:**
  - `grantor_id` (string): ID of the grantor creating the asset.
- **Request Body (JSON):** `AddMonetary` schema
- **Authentication:** Required
- **Response:**
  - 201 Created: Asset created successfully
  - 422 Unprocessable Entity: Error occurred while adding the asset
- **Description:** This endpoint allows a grantor to create a new monetary asset. The `AddMonetary` schema defines the required data for creating the asset.

### 2. Retrieve All Monetary Assets for a Grantor

- **HTTP Method:** GET
- **Endpoint:** `/monetaries/asset/asset/{grantor_id}/assets`
- **Parameters:**
  - `grantor_id` (string): ID of the grantor to retrieve assets for.
- **Authentication:** Required
- **Response:** List of `MonetaryRes` schemas
- **Description:** This endpoint retrieves all monetary assets for a specific grantor.

### 3. Retrieve All Monetary Assets for a Beneficiary

- **HTTP Method:** GET
- **Endpoint:** `/monetaries/asset/beneficiary/{bene_id}/assets`
- **Parameters:**
  - `bene_id` (string): ID of the beneficiary to retrieve assets for.
- **Authentication:** Required
- **Response:** List of `MonetaryRes` schemas
- **Description:** This endpoint retrieves all monetary assets associated with a specific beneficiary.

### 4. Retrieve a Monetary Asset

- **HTTP Method:** GET
- **Endpoint:** `/monetaries/asset/grantor/{grantor_id}/assets/{asset_id}`
- **Parameters:**
  - `grantor_id` (string): ID of the grantor who owns the asset.
  - `asset_id` (string): ID of the asset to retrieve.
- **Authentication:** Required
- **Response:** `MonetaryRes` schema
- **Description:** This endpoint retrieves information about a specific monetary asset owned by a grantor.

### 5. Update a Monetary Asset

- **HTTP Method:** PUT
- **Endpoint:** `/monetaries/asset/grantor/{grantor_id}/assets/{asset_id}/update`
- **Parameters:**
  - `grantor_id` (string): ID of the grantor who owns the asset.
  - `asset_id` (string): ID of the asset to update.
- **Request Body (JSON):** `UpdateMonetary` schema
- **Authentication:** Required
- **Response:** `MonetaryRes` schema
- **Description:** This endpoint allows a grantor to update the information of a specific monetary asset.

### 6. Delete a Monetary Asset

- **HTTP Method:** DELETE
- **Endpoint:** `/monetaries/asset/grantor/{grantor_id}/assets/{asset_id}/delete`
- **Parameters:**
  - `grantor_id` (string): ID of the grantor who owns the asset.
  - `asset_id` (string): ID of the asset to delete.
- **Authentication:** Required
- **Response:**
  - 204 No Content: Asset deleted successfully
  - 304 Not Modified: Error occurred while deleting the asset
- **Description:** This endpoint allows a grantor to delete a specific monetary asset.

## Data Schemas

- `AddMonetary`: Schema for creating a new monetary asset.
- `MonetaryRes`: Schema for representing a monetary asset.
- `UpdateMonetary`: Schema for updating an existing monetary asset.

Please refer to the code and comments within the API for more specific details about the data schemas and their structures.

## Error Responses

The API may return other HTTP status codes and corresponding error messages in case of unexpected errors or invalid requests. These error responses will include a status code and a detailed error message.

## Authors

- Chukwuebuka Ejie (Software Engineer) <tripleeoliver@gmail.com>
- Franklin Ikeogu Chidera (Software Engineer)
