# enWrite

[![N|Solid](https://res.cloudinary.com/dvmsk482x/image/upload/v1594390496/git_icon_1_lktwla.png)](https://srvraj311.github.io)

[![]()]()
enWrite is an simple and clean web app for taking notes on the go and setting reminders for important tasks.

- Note taking and Real-Time cloud backup
- Reminders and Alarms with stylish datepicker
- Cross Browser and Platform support
  [![N|Solid](https://res.cloudinary.com/dvmsk482x/image/upload/v1597972380/Screenshot_from_2020-08-21_06-42-38_ucwtyx.png)]()

# New Features!

- Implimented a brand new Authentication api that is build over python and flask-restful for secure and continuous backend
- New intuitive login screen and Signup screen.

## Languages and Libraries used:

- Javascript , Css , And Jsx(HTML in JS) using react for rendering components on screen and content management
- Python with Flask and Flask-Restful for backend API for login and Storage requests
- MongoDB for Database using Python's PyMongo library.

Use of third party libraries are kept minimal to explore the indepth features of the frameworks itself.

### Installation

Running enWrite on local server Requires the [API](https://github.com/srvraj311/enWrite-Authentication-api) to be running too on the local server as it hasn't been deployed yet.
You need to have [Node.js](https://nodejs.org/) installed and Docker Compose setup to run this.

Install the dependencies and devDependencies and start the server for react app

```sh
$ cd notes-app
$ npm install
$ npm start
```

For api to be functional.

```sh
$ cd enWrite-api
$ sudo docker-compose buil
$ sudo docker-compose up
```

### Development

Want to contribute ? That would be great!
