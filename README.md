# Group Chat
A simple application which provides web services to facilitate group chat and manage data.

### Objective
Admin APIs (only admin can add users)
- Manage Users (create user, edit user)

Any User (normal user, admin user) –
- Authentication APIs (login, logout)

Groups (Normal User) –
- Manage groups (create, delete, search and add members, etc). All users are visible to all users.

Group Messages (Normal User)
- Send messages in group
- Likes message, etc

Simple e2e functional tests with python to prove APIs are working.

## Installation Instruction:
- Prerequisites
  - Install Python3 to your system.
  - Install Virtual environment and activate the Virtual environment.
- Install Requirements:
  - `pip3 install -r requirements` 

## How to execute?
- Clone the repository
- Inside the project folder, open terminal
- Run the following command in the terminal:

`python3 manage.py runserver`
- It will run the application on your localhost.
- Open the browser with the localhost address and enjoy the application. 

## Executing test cases:
- Move to the root folder and hit `python manage.py test`. It will execute all the test cases written.

## Accessing the data:
- Django provides the functionality of admin panel where we can manage the data tables and data we created.

The admin panel can be accessed over http://127.0.0.1:8000/admin with the user_id/password as admin/admin@1234.
- Under this panel there will be tables as:
  - User: Table containing user details. Token based authentication is used all over the APIs to authenticate users.
  - Group: Table to create Group with non admin users.
  - GroupMember: This table contains details Group Members. Representing as OneToMany Relationship between Group -> Members 
  - Message: This table contains details about the message send to a group.
  - Like: This table contains details about the messages liked.

The Postman collection can be referred over the link: https://www.getpostman.com/collections/b9b0a28e065bf72a410a

