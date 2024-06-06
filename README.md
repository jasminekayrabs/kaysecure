# Kaysecure
Computing Final Project
Jasmine Kabir Rabiu

# Project Title: 
KaySecure

# Description: 
KaySecure is a webapplication platform that offers cybersecurity courses and simulations for users interested in learning or building their knowedge on cybersecurity.

# Requirements: 
- [Python3.9](https://www.python.org)
- [Django](https://docs.djangoproject.com/en/4.2/)
- Virtual Environment

# Project Installation:

## Set up the environment 
First, you need to create a folder, cd into the folder and install a virtual environment by running the following command in your terminal; 
```bash
pip install virtualenv
```
## Create a virtual environment
```bash
virtualenv myenv
```
## Activate your virtual environment
#### For Windows
```bash
myenv\Scripts\activate
```
#### For macOS and Linux
```bash
source myenv/bin/activate
```
## Clone this repository; 
```bash
git clone https://github.com/jasminekayrabs/kaysecure
```
## Install Project Dependencies (Skip this step if using the existing virtual environment)
After cloning the repository, cd into kaysecure and install dependencies;

### Install Dependencies/ Requirements from requirements.txt
```bash
cd kaysecure
pip install -r requirements.txt
```
## Running the server
## Collect static files 
```bash
python manage.py collectstatic
```
## Access the project
To access the project on your local server; 
```bash
python manage.py runserver
```
### Create Superuser (admin)
To access the admin site, run the command below and add the '/admin' route to the url in your browser e.g. 'localhost:127.0.0.1:8000/admin';
```bash
>>> python manage.py createsuperuser
``` 
## Run Test Files
```bash
>>> python manage.py test
``` 

# License:
Copyright © 2023 Jasmine Kabir

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

