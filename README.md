# kaysecure

# Setting Up Virtual Environment, Installing Requirements, and Running the Project

## 1. Set Up Virtual Environment
Once you are in the 'finalroject2/' directory, there is an existing virtual environment you can go ahead to activate it and run the project immediately. However, if there is a need to create another one, delete the existing virtual environment 'myenv' and create a new one following these steps;

### Install Virtualenv 
```bash
pip install virtualenv
```

### Create and Activate Virtual Environment
#### For Windows
```bash
virtualenv venv && venv\Scripts\activate
```
#### For macOS and Linux
```bash
virtualenv venv && source venv/bin/activate
```

## 2. Install Project Dependencies
After creating and activating the virtual environment, cd into kaysecure and install dependencies;

### Install Dependencies/ Requirements from requirements.txt
```bash
cd kaysecure
pip install -r requirements.txt
```

## 3. Run the Project

### Run the Project
```bash
python manage.py runserver
```
### Create Superuser (admin)
To access the admin site, run;
Run the following command on your terminal:
```bash
>>> python manage.py createsuperuser
``` 
Now to access the admin site, run the server and add the '/admin' route to the url in your browser e.g. 'localhost:127.0.0.1:8000/admin'

## 4. Run Test Files
```bash
>>> python manage.py test
``` 

## 5. Deactivate Virtual Environment

### Deactivate the Virtual Environment
```bash
deactivate
```
