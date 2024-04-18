# Basic backend structures

All API response has the same structure as follow:

<code>
    {
        "success": true,
        "result": "some_json_string",
        "error": "some error string"
    }
</code>

with "success" indicates if the action is successful or not, "result" is a JSON string of the return object, and error is a string indicates any error when sending request to the API (null if there is none). 

The only exception is there's an unexpected error from Flask that raise an uncaught