# SWE-573 Project
This project will be developed as a part of Swe-573 course and will be conducted by applying all software project life cycle steps like below. 

- Requirements elicitation
- Modelling
- Development
- Quality assurance
- Communication
- Presentation
- Documentation
- Planning & tracking
- Version management and automated processes
- Deployment.

## General Features of Application: 
Features will be listed after topic clarification.


 
## Clone

- Clone this repository to your local machine using `https://github.com/fatihcirakoglu/swe573project.git`
 
## Build
- Just clone the repo on your Linux environment and run below command in the folder.

 Debugging Application in Local Environment:  
-	Clone repository from git@github.com:fatihcirakoglu/bounswe573-2022.git
-	Install and create a MySQL database with credendials below.
  - DB_NAME=webappdb
  - DB_USER=webappdbuser
  - DB_PASSWORD=swe573.
- Go to main project folder where docker compose files reside
- Then run: $ docker-compose -f  docker-compose.yml up
-	Go to any explorer and view: http://localhost

## Setup & Deployment
Viewing Application In AWS machine: 
By using secret key that is provided during creation of machine instance, you can login with below credentials to AWS E2C machine.

$ ssh  -i  djangokey.pem  ec2-user@52.87.173.228

You will be connected to AWS E2C mahine terminal, just go to 
$ cd /home/ec2-user/production/bounswe573-2022
Then run:
$ docker-compose -f  docker-compose-production.yml up

Finally project will run and you can view project page with below link:
URI of Project:  http://ec2-52-87-173-228.compute-1.amazonaws.com/

## FAQ

```

```

## Support
Reach out to me via email!
email: fatih.cirakoglu@boun.edu.tr



## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[GNU General Public License v3.0](https://opensource.org/licenses/gpl-license)**
- Copyright 2022 © 

