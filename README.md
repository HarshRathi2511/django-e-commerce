## E-Commerce App using Django/Docker/Nginx

# Overview
This is a Python-Django project that uses Docker and Nginx. Authentication is handled by Google OAuth.

# Prerequisites
1. Docker
2. Docker Compose
3. Python3
4. Django

# Getting Started
Clone the repository: 
```
git clone https://github.com/<username>/<repo_name>.git
cd <repo_name>
```

Build the Docker image:
```
docker-compose build
```

Start the container: 
```
docker-compose up
```

Visit http://localhost:8000 in your browser to access the application

# Google OAuth
To use Google OAuth for authentication, you will need to create a project on the Google Cloud Console and obtain a CLIENT_ID and CLIENT_SECRET. 
Once you have those, you can add them to the settings.py file in the project.

# Additional Resources
1. Django documentation
2. Docker documentation
3. Google OAuth documentation





# Note
Make sure you have created .env file in your root directory and added the necessary environment variables.
Make sure you have created credentials.json file in your root directory and added the necessary credentials obtained from Google Cloud Console.

# Command to run
Copy code
```
docker-compose up --build
docker-compose run --rm web python manage.py makemigrations
docker-compose run --rm web python manage.py migrate
docker-compose run --rm web python manage.py createsuperuser
```


# Addtional Note
Add your domain in settings.py file
Run and check the configurations.
```
nginx -t 
```
To restart nginx execute the following command . 
```
sudo service nginx restart
```

## Contributors
Made with 💖 by [Harsh Rathi](https://github.com/harshRathi2511)


