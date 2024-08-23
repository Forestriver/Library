Library API for Book Management

This project is a Django-based API for managing book information, including CRUD operations and pagination. The API uses PostgreSQL as the database backend.


1. Clone the Repository the repository to your local machine:
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name

2. Create and Activate a Virtual Environment

On Windows:
python -m venv venv
.\venv\Scripts\activate

On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Configure PostgreSQL (create .env file with creadentials)
Install python decouple:
pip install python-decouple


5. Apply migrations:
python manage.py makemigrations
python manage.py migrate

6. Run tests:
python manage.py test

7. Start Django server
python manage.py runserver





