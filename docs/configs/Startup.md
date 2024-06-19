# Start up

Frameworks and tools used in this project:
- Backend: Flask
- Frontend: Vue.js
- Sending request: axios
- Database: MariaDB
- ORM (use with Flask and MariaDB): SQLAlchemy

# How to run (backend, development)

- Install MariaDB and follow the guide in 'How to connect to MariaDB.docx'
- Go to the project directory, check for the .venv folder. 
- If .venv directory does not exists, use <code>python -m venv .venv</code> to create a directory called .venv and create the virtual environment. Source <a href="https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/">FreeCodeCamp guide</a>
- Activate virtual environment: <code>. .\.venv\Scripts\activate</code> or <code>. ./.venv/bin/activate</code> if you use MacOS or Linux.
- Now install all required packages: <code>pip install -r requirements.txt</code>
- Run "npm run build" to build static files from Vue templates and files
- Now run Flask development server: <code>python ./backend/server.py</code>


# API structure

All APIs through the backend follow this structure:

<pre>
<code>
    {
        success: true,
        result: "['JSON object string']",
        error: "Error string"
    }
</code>
</pre>

Note that success is a boolean, result and error can be either a string (for result it must be a valid JSON object string) or null. 

### Import data for testing

If you use DBeaver or some management software for MariaDB, just connect to the database, open database-dump-library.sql and click on 'Run'