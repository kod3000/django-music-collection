# Music Collection Manager

(early draft, work in progress)



## Quick Overview

This Django application provides a simple web interface for inserting JSON arrays into MongoDB.
Users can input a JSON array, which is then processed and inserted into specified MongoDB collections based on the content of the array. The app is designed to handle arrays of album data, sorting them into "known albums" and "unknown data" collections based on the presence of the `numberOfTracks` field.

## Features

- Web form for inputting JSON arrays.
- Validation to ensure the input is a valid JSON array.
- Insertion of valid arrays into MongoDB collections.
- Separation of data into "known albums" and "unknown data" based on the presence of specific fields.
- Error handling for database connection issues.
- Minimalistic design for easy use.
- No multiple entry of data, just a single JSON array.

## Prerequisites

Before you start, make sure you have the following installed:
- Python (3.8 or newer)
- Django (3.x or newer)
- PyMongo
- MongoDB server running locally or accessible via a connection URI.

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/kod3000/django-music-collection.git
   cd django-music-collection
   ```

2. **Install Dependencies**

   Inside the project directory, install the required Python packages:

   ```bash
   pip install django pymongo dnspython python-dotenv
   ```
    or
    ```angular2html
    pip install -r requirements.txt
    ```


3. **Configuration**

   Setup the environment variables in a `.env` file in the folder 'music_collection'. The file should contain the following:

    ```angular2html
    MONGO_URI=your_mongodb_uri
    MONGO_DATABASE_NAME=your_database_name
    ```


4. **Run Migrations**

   Although this application primarily uses MongoDB, ensure your Django project is ready to go:

   ```bash
   python manage.py migrate
   ```

5. **Start the Development Server**

   ```bash
   python manage.py runserver
   ```

   Navigate to `http://127.0.0.1:8000/albums/insert/` to access the form.

## Usage

- **Inserting an Album**

  On the form page (`/albums/insert/`), enter a JSON array in the input field and submit the form. The array should contain objects with or without a `numberOfTracks` field to differentiate between known albums and unknown data.

  Example array input:

  ```json
  [
    {"albumName": "Sample Album 1", "numberOfTracks": 10},
    {"albumName": "Unknown Data", "someField": "someValue"}
  ]
  ```

- **Viewing Results**

  Upon submission, if the array is successfully processed and inserted, you'll see a message indicating the number of albums inserted. If the database connection fails, an error message will be displayed.

## Error Handling

- The application handles errors related to database connections and invalid input formats, displaying appropriate messages to the user.
- Ensure your MongoDB server is running and accessible to avoid connection errors.

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue if you find a bug or have a feature request.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


## Acknowledgements

This project was built using the following technologies:

- [Django](https://www.djangoproject.com/)
- [MongoDB](https://www.mongodb.com/)
- [PyMongo](https://pymongo.readthedocs.io/en/stable/)

If you find this project useful, please consider giving it a star. Thank you!



