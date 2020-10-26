# Ticketmaster App
## General info
App has been created for the recruitment process. App provides few endpoints:
1. *admin/events* - crud for events management, plus creating tickets for event and reservation stats
2. *events* - retrieve and list view for users
3. *orders* - retrieve/list/create view for creating orders by users (ticket reservation) plus making the payment
4. *register/* - sign up view
5. *login/* - obtaining authentication token

## Setup
To run this project, install it locally using docker:

```
$ docker-compose up --build
```