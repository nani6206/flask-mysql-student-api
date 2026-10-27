# Flask MySQL Student API

A small Flask app I made while learning how REST APIs work with Python and MySQL.

The API uses a `students` table with an ID, name and email. It has routes for the five HTTP methods I practised: GET, POST, PUT, PATCH and DELETE.

## What I used

- Python
- Flask
- MySQL
- mysql-connector-python
- Postman for testing

## Run it locally

1. Create the database and table by running `schema.sql` in MySQL Workbench.
2. Install the packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Open `app.py` and replace `YOUR_MYSQL_PASSWORD` with your local MySQL password. Don't commit your real password.
4. Start the app:

   ```bash
   python app.py
   ```

5. The API runs at `http://127.0.0.1:5000`.

## Routes

| Method | URL | What it does |
|---|---|---|
| GET | `/students` | Get all students |
| GET | `/students/1` | Get one student by ID |
| POST | `/students` | Add a student |
| PUT | `/students/1` | Update the name and email |
| PATCH | `/students/1` | Update the student's name |
| DELETE | `/students/1` | Delete a student |

Replace `1` with the ID you want to work with.

## Example POST body

In Postman, choose **Body → raw → JSON**:

```json
{
  "name": "Nag",
  "email": "nag@gmail.com"
}
```

For PUT, send both `name` and `email`. For PATCH, send the field you want to change, for example:

```json
{
  "name": "Nagarjuna"
}
```

This is a beginner learning project. The database connection settings are local, so update them for your own MySQL setup before running it.
