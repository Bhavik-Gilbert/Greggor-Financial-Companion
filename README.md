# Greggor-Financial-Companion

## Team Members
The members of the team are:
- RESHMA DHILLON
- BHAVIK GILBERT
- MICHAEL (Misha) HIGHAM
- KUSHAAGRA KAPOOR
- MATTHEW PALMER
- SAHITYA SAKTHIVEL
- LOUISA SCOTT
- CHARLES (Charles) SUDDENS-SPIERS

## Badges
![GitHub last commit](https://img.shields.io/github/last-commit/Bhavik-Gilbert/Greggor-Financial-Companion)
![GitHub contributors](https://img.shields.io/github/contributors/Bhavik-Gilbert/Greggor-Financial-Companion)
![Github build](https://img.shields.io/github/actions/workflow/status/Bhavik-Gilbert/Greggor-Financial-Companion/django.yml)

![Lines of code](https://img.shields.io/tokei/lines/github/Bhavik-Gilbert/Greggor-Financial-Companion)
![GitHub repo size](https://img.shields.io/github/repo-size/Bhavik-Gilbert/Greggor-Financial-Companion)
![GitHub top language](https://img.shields.io/github/languages/top/Bhavik-Gilbert/Greggor-Financial-Companion)
![GitHub language count](https://img.shields.io/github/languages/count/Bhavik-Gilbert/Greggor-Financial-Companion)

## About
This project aims to produce an application that allows users to track their expenditures. The expenditure can belong to different categories. The user should be able to create, edit and delete these categories. When adding new spending, there should be a functionality to add a title, a short description, and an optional photo or file for the receipt. Moreover, the user should be able to set spending limits for each category as well as for the overall spending in a selected timeframe. When approaching and exceeding the set limits, the user should get a warning from the system. The app should motivate the user to stick to the set goals through gamification. Lastly, the user should be able to get reports and charts for their spending in a given timeframe.

## Project structure
The project is called `gfc` (Greggor Financial Companion).  It currently consists of a single app `financial_companion` where all functionality resides.

## Deployed application
This application is deployed using python anywhere
### [Live Site](http://greggorfinancialcompanion.pythonanywhere.com/) - http://greggorfinancialcompanion.pythonanywhere.com/

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Navigate into the django root directory:

```
$ cd gfc
```

Migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

Use the following accounts when testing the seeded database:

Format (username, password)
```
ADMINS:
@michaelkolling, Password123
@adminuser, Password123

NORMAL USER:
@johndoe, Password123
```


Unseed the development database with:

```
$ python3 manage.py unseed
```

Run all tests with:
```
$ python3 manage.py test
```

## Sources
The packages used by this application are specified in `requirements.txt`

<br />

### Tabula
Usage under the The MIT License (MIT): https://github.com/tabulapdf/tabula-java/blob/master/LICENSE 
<br />
Information about tabula-py: https://tabula-py.readthedocs.io/en/latest/
<br />
Information about tabula-java: https://github.com/tabulapdf/tabula-java

