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

![1](https://user-images.githubusercontent.com/33651899/176979823-72abd6ca-f30c-4e60-b1f9-ffdeb75211b0.JPG)

![2](https://user-images.githubusercontent.com/33651899/176979825-a541b534-7e69-4176-9f1e-d3e09165e663.JPG)

![3](https://user-images.githubusercontent.com/33651899/176979826-886a3d6b-b136-44f3-b434-9453ddc263bc.JPG)

![4](https://user-images.githubusercontent.com/33651899/176979827-e46c8770-139d-48f9-aa14-93d2fe0d8e05.JPG)

![5](https://user-images.githubusercontent.com/33651899/176979828-d84b53a4-81b3-43fe-b4a4-09a77bd7d296.JPG)

![6](https://user-images.githubusercontent.com/33651899/176979829-56b79af7-d6b6-4bba-aff1-0c6ea67aef90.JPG)

![7](https://user-images.githubusercontent.com/33651899/176979830-e93d251d-89a5-4c77-84cc-618af4bf3bc9.JPG)

![8](https://user-images.githubusercontent.com/33651899/176979831-93a508cc-4f97-427d-bdbb-21abd6b37076.JPG)

![9](https://user-images.githubusercontent.com/33651899/176979833-bbe0b93e-e7fb-4a33-9c76-1db0a494dea1.JPG)

![10](https://user-images.githubusercontent.com/33651899/176979834-4a1c6672-0eb0-433f-8298-8d68c881ed27.JPG)

![11](https://user-images.githubusercontent.com/33651899/176979835-30ef0e4a-89ca-468f-9769-67ec87315fce.JPG)

![12](https://user-images.githubusercontent.com/33651899/176979836-018eeefd-77fd-4e38-94e8-b2e287368d1b.JPG)

![13](https://user-images.githubusercontent.com/33651899/176979837-178b15d1-84c5-426f-b200-93d6d4b6c6d4.JPG)

![14](https://user-images.githubusercontent.com/33651899/176979839-4cbf02fe-866f-4a61-b361-51e35a2b6646.JPG)

![15](https://user-images.githubusercontent.com/33651899/176979840-f33470b8-808d-48d9-91b3-fb0ccb3d585f.JPG)

![16](https://user-images.githubusercontent.com/33651899/176979841-d0619505-ab7d-4509-b637-377fa6f4e7bc.JPG)

 
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

