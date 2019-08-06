# Item Catalog WebApp - (UDACITY)

A Web Application that displays a catalog of items a and allows a user to view the items, as well as creating, editing, and deleting them when signed in with a google account, as well as providing a Restful api for developers to retrieve information (Udacity's Full Stack Nano Degree [Item Catalog Project](https://classroom.udacity.com/nanodegrees/nd004/parts/4dcefa2a-fb54-4909-9708-9ef2839e5340/modules/eca024ee-b994-4b67-9e22-3b9fc8deb226/lessons/027ef2ad-8005-42e7-8005-b193065df1c3/project))

## What The Program Does:

the web app connects to a database and allows the user to:

1. view items in the catalog.
2. when logged in: create items and edit and delete items they have created.
3. send a request to a restful api to get a json representation of the data.

## Requirements

- [python version 3](https://www.python.org/downloads/release/python-374/)
- [vagrant](https://www.vagrantup.com/downloads.html)
- [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
- [Git](https://git-scm.com/downloads)
- you need to have the following python3 libraries: `flask`, `google oauth2`, `flask_httpauth` and `sqlalchemy` installed on your machine
- Google OAuth Credentials [Google Dev Console](https://console.developers.google.com).
  - Create a project then web application credentials
  - set "Authorized JavaScript origins" to "http://localhost:5000"
  - set "Authorized redirect URIs" to "http://localhost:5000/oauthcallback"
  - download the credentials json file

## Setup

1. Download any of the Requirments you are missing.

2. Download [this](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip) Udacity folder with preconfigured vagrant settings.
   or `clone https://github.com/udacity/fullstack-nanodegree-vm`

3. Clone this repository `clone https://github.com/nicolash92/item-catalog--udacity-.git`.

4. Navigate to the Udacity Virtual Machine folder in **git bash** and cd into vagrant.

5. using **git bash** and launch the virtual machine with `vagrant up`, then `vagrant ssh` to connect to the preconfigured linux instance.

6. to run the program, while in the vm, navigate to the repo that you cloned, and run `sudo pip3 install --upgrade -r requirements.txt` on linux based systems or `sudo pip install --upgrade -r requirements.txt`

7. make a client_secrets.json file and copy your google credentials to it, and add `flask_secret` key after the `web` key and set the value to a random string.

8. follow instructions in Running The Project

## Running The Project

on mac and linux based systems:
`> python3 application.py`

#####admin tool
the database file is already in the repo, but if it gets deleted you can run `python3 setup.py` and go to your browser and go to the following addresses `http://localhost:5000`

- `/gencat` to generate categories
- `/deler` to delete all users
- `/list-users` to get a list of all registered users
- `/addDefItem` generate an item. (RUN ONLY ONCE) (must have an account registered for this to work)
