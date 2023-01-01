# SWE574 Group 5 Project Report
## Project Information
- Name: Group 5
- Course: SWE574
- Date: 2022-01-02
- Project name: LetsColearn
- git repository: https://github.com/fatihcirakoglu/bounswe574-2022/
- git tag: https://github.com/fatihcirakoglu/bounswe574-2022/releases/tag/v0.9
- Version: v0.9
- Deployment URL: http://ec2-52-55-155-229.compute-1.amazonaws.com/

### Contributors: 
- Fatih Cirakoglu 
- Omer Ege Ozkaya
- Berat Sert
- Baris Karapinar

## User IDs for Testing Purpose
- Test User 1: (username: uskudarli, password:testuser1)
- Test User 2: (username: uskudarli1, password:testuser2)

## HONOR CODE
Related to the submission of all the project deliverables for the Swe574 2022-2023
Fall semester project reported in this report, we Group 5 declare
that:
- We are students in the Sofware Engineering MS program at Bogazici University
and are registered for SWE574 course during the 2022-2023 Fall semester.
- All the material that we are submitting related to our project (including but
not limited to the project repository, the final project report, and
supplementary documents)
have been exclusively prepared by ourselves.
- We have prepared this material individually without the assistance of anyone
else with the exception of permitted peer assistance which we have explicitly
disclosed in this report.

## Project Details
### Overview
LetsColearn application is a web platform which creates a co-learning
platform that connects the people who wants to teach anything to the people who
like learning new things. LetsColearn also includes 2 important features, which are recommendation engine supported by WikiData, and 
annotation creation support for all content by the help of W3C annotation data model. Within the recommendation engine, the learning space engage with the related Q-Codes while the creation of the learning spaces and creates a WikiData entity pool for each learning space in the application database model. With using these entity pools, recommendation engine recommends related (joined and created) learning spaces for each user according to associated Q-codes of learning spaces.
Annotation feature enables the user to create, modify, delete annotation on the content of the website. The annotations are stored on Elasticsearch via a stand-alone backend application.
This platform will completely have an organic process
that means there will be no assessment of the content that is being teached by some
body, in other means, users of the platform will determine the quality of content
that is shared on the platform. So, users will score the content and provide useful
feedbacks. So, the main aim of this application is to gain best information from one
user to other users and inspire people to share valuable information on any topic.
Creating co-learning platform for users, who wants to share information and drive
personal improvements on web.
The platform has main features for the users like:
- Users can create learning spaces
- Users can join learning spaces that they interested in
- In these learning spaces, they are able to share posts and ask questions to each
- User get recommendation from the recommendation engine
- Users can create annotations
other or other users.
For developing such kind of platform, python knowledge, Django framework
knowledge, experience on usage of MySQL database and usage of Github, WikiData and W3C Annotation data model.

### Software Requirements Specification
|Category|Requirement ID|Requirement Type|Requirement Pattern  |Requirement Definiton|Status(%)|
|-|----------|-------|---------------|-----------------|-------------|
Admin| REQ-1 | FR | Ubiquitous | LetsColearn application shall have an admin user|100|
Admin| REQ-2 | FR | Ubiquitous | LetsColearn shall have an admin page for configuring settings of application|100|
Admin| REQ-3 | NFR | Ubiquitous | Users shall be able to report inconvenient content on the system|0|
Admin| REQ-4 | NFR | Ubiquitous | Admin user shall have rights for removing inconvenient content|100|
Auth| REQ-5 | FR | Ubiquitous | LetsColearn shall enable users to register on the system via email|100|
Auth| REQ-6 | NFR | Ubiquitous | LetsColearn shall request password twice during registration|100|
Auth| REQ-7 | NFR | Ubiquitous | LetsColearn shall request topics of interest during registration|0|
Auth| REQ-8 | FR | Ubiquitous | LetsColearn shall enable users to login on the system via email|100|
Content| REQ-9 | FR | Ubiquitous | Users shall be able to create a learning space to share some content on the system|100|
Content| REQ-10 | FR | Ubiquitous | New course content creation page shall display a drop-down menu for topic selection|100|
Content| REQ-11 | FR | Ubiquitous | New course content creation page shall display a form on the page for content creation|100|
Content| REQ-12 | FR | Ubiquitous | Content creation page shall include image upload, hashtag entry and submit button|100|
Content| REQ-13 | FR | Ubiquitous | External videos shall be embeddable in content page|100|
Content| REQ-14 | FR | Ubiquitous | LetsColearn shall enable users to share text content on the pages|100|
Content| REQ-15 | FR | Ubiquitous | Users shall be able to ask questions on created resources in the system|50|
Content| REQ-16 | FR | Ubiquitous | Users shall be able to create annotations for the content of courses and learning spaces|0|
Content| REQ-17 | FR | Ubiquitous | Users shall be able to delete his/her created learning spaces|0|
Content| REQ-18 | FR | Ubiquitous | Users shall be able to delete his/her created courses|0|
Gdpr| REQ-19 | NFR | Ubiquitous | LetsColearn shall not violate GDPR compliances|100|
Infra| REQ-20 | NFR | Ubiquitous | LetsColearn shall be available in worldwide|100|
Infra| REQ-21 | NFR | Ubiquitous | LetsColearn shall be available 7/24|100|
Language| REQ-22 | NFR | Ubiquitous | LetsColearn shall support interface in only English language|100|
Language| REQ-23 | NFR | Ubiquitous | LetsColearn shall support content in only English language|100|
Main Page| REQ-24 | FR | Ubiquitous | LetsColearn shall include a search box on top of main page|100|
Main Page| REQ-25 | FR | Ubiquitous | LetsColearn shall display trending topics |0|
Main Page| REQ-26 | FR | Ubiquitous | LetsColearn shall display login, register, FAQs and help buttons on top right side|100|
Main Page| REQ-27 | FR | Ubiquitous | LetsColearn shall display a footer at the bottom of main page|0|
Main Page| REQ-28 | FR | Ubiquitous | Main page shall display most popular hashtags|0|
Main Page| REQ-29 | FR | Ubiquitous | Main page shall display learning spaces according to topics of interest of logged in user |0|
Main Page| REQ-30 | FR | Ubiquitous | Main page shall display learning spaces with highest scores for guest user|0|
Profile Page| REQ-31 | FR | Ubiquitous | LetsColearn shall show favorite learning spaces of user on profile page after|0|
Profile Page| REQ-32 | FR | State Driven| LetsColearn shall navigate user to profile page when user clicks profile page|100|
Profile Page| REQ-33 | FR | Ubiquitous | LetsColearn shall create a user profile on the system for each user|100|
Profile Page| REQ-34 | FR | Ubiquitous | User profiles shall include badge, name, photo, his/her created learning spaces, joined learning spaces, topics of interest|30|
Profile Page| REQ-35 | NFR | Ubiquitous | Users shall be able to configure their topics of interest on their profiles|0|
Profile Page| REQ-36 | NFR | Ubiquitous | Users shall be able to delete his/her membership on the system|0|
Rating| REQ-37 | FR | Ubiquitous | Users who created contents shall be scored by other users that will define user's badge|0|
Rating| REQ-38 | FR | Ubiquitous | Users shall be able to rate contents and users on the system|0|

### Design (Software & Mockups) – UML diagrams and images
Below scenarios describes the new requirements and their use cases.

Purpose: A scenario describing the use of an online Colearning system.

Equipment: Any computer with a supported browser.

#### Individual 1: Jessica is a curious learner and willing to investigate platforms where she can learn anything by herself with a high quality content. She is not a member of the site.

##### Scenario 1: Jessica visits the platform.
1. Jessica enters the main page of the platform.
2. Main page displays the most popular hashtags and learning spaces.

![JessicaS1](https://user-images.githubusercontent.com/33651899/200187247-f98588c9-d592-4fe1-bd7a-287ac66e3d01.JPG)

##### Scenario 2: Jessica decide to sign up for the platform.
1. Jessica enters the website.
2. Jessica clicks on the Sign up button.
3. Jessica fills out credentials and topics of interest information.
4. System navigates to confirmation page and sends an email.
5. Jessica clicks the confirmation link in the email.
6. System display confirmation sucessfull message.
7. Jessica logins by entering credentials.
8. Main page displays the most popular hashtags and related learning spaces according to the topics of interests for Jessica.

![JessicaS2](https://user-images.githubusercontent.com/33651899/200187250-211c852e-1f06-46f0-a80e-e2a48bb0d897.JPG)
![JessicaS22](https://user-images.githubusercontent.com/33651899/200187253-d94e49bd-26af-4f5f-9727-c6edb13c4452.JPG)
![JessicaS23](https://user-images.githubusercontent.com/33651899/200187255-0231eb22-128c-4609-8d61-ddfe9e9fd81e.JPG)
![JessicaS24](https://user-images.githubusercontent.com/33651899/200187256-e960edc8-c5c8-4415-8d8b-4c74c7547bf1.JPG)
##### Scenario 3: Jessica searchs her interested topics.
1. Jessica writes a keyword in search box and click search button.
2. Search page displays learning space titles that includes the keyword.
3. Jessica clicks the detailed search button.
4. Jessica is able to search in specific areas as: Learning Space Titles, Course Content, Hashtags

![JessicaS3](https://user-images.githubusercontent.com/33651899/200187251-84688878-7e35-47af-8f44-59b5e2487f5d.JPG)

#### Individual 2: Thomas is a logged in user of this site. He loves contributing to learning spaces about sports. He learns better with peers.

##### Scenario 1: Thomas is willing to create annotation inside the learning spaces that he is interested in.
1. Thomas logins to the website.
2. Thomas navigates to one of his interested learning space.
3. Thomas starts reading the content of the courses inside learning space. 
4. While reading the content, Thomas creates an annotation for the familiar information for him, which he knows the source of this information.

![ThomasS1](https://user-images.githubusercontent.com/33651899/200189487-96a9b743-7e06-4e0d-a19d-5f9f0619f2f2.JPG)
#### Scenario 2: Thomas visits the home page.
1. Thomas enters the website.
2. Main page displays the most popular hashtags and related learning spaces according to the topics of interests with highest scores for Thomas.

<img width="922" alt="scenario2" src="https://user-images.githubusercontent.com/75334593/202932067-38b0fcc0-b473-4ed0-86a3-55883be90132.png">


##### Scenario 3: Thomas changes his topics of interest.
1. Thomas navigates to the Profile Page.
2. Thomas requests to change the topics of interest.
3. Thomas navigates to the main page.
4. Main page displays updated content according to the new topics of interest.

![ThomasS3](https://user-images.githubusercontent.com/33651899/200187257-d7c3ccab-1adf-4af1-99d7-6805fc877ef9.JPG)
##### Scenario 4: Thomas visits his profile page.
1. Thomas navigates to the Profile Page.
2. Thomas will see his own user badge.
3. Thomas will see his own user name.
4. Thomas will see his own user photo.
5. Thomas will see his created learning spaces
6. Thomas will see his own joined learning spaces.
7. Thomas will see his topics of interests.

![ThomasS4](https://user-images.githubusercontent.com/33651899/200190892-fa65bf1f-1487-4ada-a88a-e8511d19d629.JPG)

##### Scenario 5: Thomas rates content.
1. Thomas navigates a learning space.
2. Thomas gives a score(1-5) for learning space or course under learning space. 
3. System updates the score of this learning space.

![ThomasS5](https://user-images.githubusercontent.com/33651899/200187258-00ede25e-0432-4d3c-9a80-af0232331f03.JPG)
##### Scenario 6: Thomas rates author.
1. Thomas navigates a learning space.
2. Thomas gives a score(1-5) for the author of learning space or author of courses under learning space. 
3. System updates the score of the author.

![ThomasS6](https://user-images.githubusercontent.com/33651899/200187259-0f1c2d00-c718-40ef-9691-cce1b017d521.JPG)

##### Scenario 7: Thomas gets rating from other users.
1. A Thomas receives some score from different users.
2. System will update the score of Thomas. 
3. If his score is above some threshold, system updates the badge of him.

![ThomasS7](https://user-images.githubusercontent.com/33651899/200190893-bfe369f8-58c3-4197-907a-d62184ebaf82.JPG)

##### Scenario 8: Thomas reports a content.
1. Thomas reports a content as inconvenient. 
2. Admin user checks the content of reported course or learning space. 
3. Admin user removes the content if necessary. 

![ThomasS8](https://user-images.githubusercontent.com/33651899/200190895-de213c53-7b7f-45ac-a0d5-4ba83d0a311d.JPG)

##### Scenario 9: Thomas cancel his membership.
1. Thomas navigates to his profile page. 
2. Thomas clicks cancel membership button. 
3. System logouts him and deactivates his membership.

<img width="807" alt="scenario9_1" src="https://user-images.githubusercontent.com/75334593/202932088-b02f0211-84e5-4c31-923b-9d82db3d2427.png">
<img width="805" alt="scenario9_2" src="https://user-images.githubusercontent.com/75334593/202932092-06f2c7db-7404-480e-acdf-58cc34f7620c.png">
<img width="805" alt="scenario9_3" src="https://user-images.githubusercontent.com/75334593/202932100-6621f083-a64c-43aa-95d8-69fab56b5bc7.png">


##### Scenario 10: Thomas creates questionnaire in the learning space.
1. Thomas navigates to a learning space.
2. Thomas lists some questions about the content.
3. Thomas posts those questions under learning space.
4. Thomas receives answers for this question from other users.

![ThomasS10](https://user-images.githubusercontent.com/33651899/200187261-174a28de-eb41-4932-bdad-8ee3184f2d37.JPG)
##### Scenario 11: Thomas deletes the learning space that he created.
1. Thomas navigates to one his learning spaces.
2. Thomas clicks delete button.
3. Thomas clicks confirm button.
4. Platform deletes the learning space.

<img width="796" alt="scenario11_1" src="https://user-images.githubusercontent.com/75334593/202932112-d94a8df6-1000-488c-8f7d-16013b20b5c3.png">
<img width="807" alt="scenario11_2" src="https://user-images.githubusercontent.com/75334593/202932165-d6261e75-c7da-40da-8c64-1574bd58bc89.png">


##### Scenario 12: Thomas deletes the courses under learning space that he created.
1. Thomas navigates to one his courses.
2. Thomas clicks delete button.
3. Thomas clicks confirm button.
4. Platform deletes the course.

![ThomasS12](https://user-images.githubusercontent.com/33651899/200190897-a22e9e64-fdaa-47d3-a47c-845a40683990.JPG)


#### Overall System Architecture
![image](https://user-images.githubusercontent.com/75334593/210184125-72e33fde-635b-40c8-a548-9b9fbb1752b5.png)

### Status of your project

ColearnApp has functionality to engage learning spaces with multiple Wikidata Entity.
While creation of learningspaces, the Colearnapp demands keywords that defines the learning space. 
Then, ColearnApp gathers the related Wikidata Entities with demanded keywords.
Users need to select the most related Wikidata Entity for each keyword that user typed before.
After the selection, Entity Manager saves the engaged Wikidata entities' qcode and related wikidata entities 
(which is a pool which generated by gathering all instances and subclasses of engaged Wikidata entity.)
When the recommendation engine triggered, the recommendation engine unions the pools of the created and joined learning spaces. 
Then, recommendation engine searchs over the other (not joined or not created by intended user.) learning spaces'
pool to find the unioned wikidata entity qcodes. Finally, ColearnApp forms a list with recommended learningspaces and displays it to the user by ordering their creation date.

For annotation, a Javascipt script embedded on the web-pages is triggered upon several events including loading of DOM contents or at the end of a selection. Then this script prepares an HTTP request according to the needs of the current operation, such as POST request for creating a new annotation, GET request to get a specific annotation. Then this request is sent to the annotator store backend through 5000 port. The annotator store backend evaluates the request and fetches, saves, modifies or deletes the related documents under the annotations index of Elasticsearch with a REST API call through 9200 port.

### Status of Deployment: include the URL
Deployment URL: http://ec2-52-55-155-229.compute-1.amazonaws.com/

### Dockerization status
There are 3 application which are dockerized and running on the platform and communicates via REST API calls. The relation between these docker application are shown below:
```
version: '3'
services:
  elasticsearch:
    image: elasticsearch:1.7.6
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - 9200:9200
      - 9300:9300
    healthcheck:
      test: curl --fail http://127.0.0.1:9200 || exit 1
      interval: 5s
      retries: 5
      start_period: 5s
      timeout: 10s
  web:
    image: coelarnapp:1.0
    build: .
    command: >
      sh -c "python manage.py makemigrations && \
             python manage.py migrate && \
             python manage.py runserver 0.0.0.0:8000"
    environment:
      - SECRETKEY=&w!-%qsbcb_7kdo^)roirk)evgkhu1vn(e8tztam-*+n1b#)=2
      - ALLOWEDHOST=*
      - DB_NAME=colearnappdb
      - DB_USER=iotappdbuser
      - DB_PASSWORD=sweswe599.
      - DB_HOST=iotappdb.cxj0nj6y8us5.us-east-1.rds.amazonaws.com
      - DB_PORT=3306
      - EMAIL_HOST_USER=fatihcirak@gmail.com
      - EMAIL_HOST_PASSWORD=IHJvrNcO6jYPZqGn
    ports:
      - "80:8000"

    volumes:
      - ./src:/app
      - /var/lib/mysql/mysql.sock:/run/mysqld/mysqld.sock
  annotator-store:
    image: annotator-store:1.0.0
    build: ./annotator-store-service
    #command: >
    #  sh -c "apk --no-cache add curl && curl http://elasticsearch:9200/ && python ./run.py"
    command: >
      sh -c "python ./run.py"
    ports:
      - "5000:5000"
    depends_on:
      elasticsearch:
        condition: service_healthy
    volumes:
      - ./annotator-store-service:/app
```

### System manual - what are the requirements to run this system and installation instructions (docker)

The 3 Docker applications in our platform uses below packages: 
```
asgiref==3.5.0
backports.zoneinfo==0.2.1
certifi==2022.9.24
charset-normalizer==2.1.1
Django==4.0.3
django-ckeditor==6.4.1
django-cors-headers==3.13.0
django-cors-middleware==1.5.0
django-crispy-forms==1.10.0
django-environ==0.8.1
django-js-asset==2.0.0
django-mysql==4.8.0
django-taggit==3.0.0
djangorestframework==3.12.2
idna==3.4
mysqlclient==2.1.0
Pillow==9.0.0
pytz==2020.1
requests==2.28.1
sqlparse==0.4.2
tzdata==2022.1
urllib3==1.26.13
Wikidata==0.7.0
```

For deploying the application the command below should be used.
```
docker-compose -f docker-compose-production.yml up
```


### User manual - A description of how to use your system
The URL of the platform: http://ec2-52-55-155-229.compute-1.amazonaws.com/
You will be directed to home page of LetsColearn application and you can view
contents freely without logging in.
You need to login to join space, create post, ask question about content and like
posts/spaces.
Before logging in, you need to signup via sign-up page, you need to provide
username, password and email. You will use username and password information
during further logins.
After login, you will see extra “ColearnSpaces” section, this page shows the
colearn spaces that you created and joined.
Also “CreateWorkspace” link will be active, and when you click it you will be asked for keywords which might be up to 3 words seperated with a comma. Then, you will be
directed to form page for creating colearn space. At the top you are to select the related WikiData entities. There are four parameters which
are title, content, image and tags. Category is requested for only DB
query purposes, so it is not being shown to users. All colearn space and post
contents are being grouped under tags. Tags could be entered by comma separated.
Inside content, pictures, links, vidoes could be embedded via text editor.
After creation of CoLearn space, you will be able to see users that are joined to
space, like counts, view counts etc. Also post creation will be activated.
Each logged in user can join colearn spaces freely and create posts under these
spaces. Also, every user can ask questions under posts.
To annotate on the web page, you can select the content that you want to annotate and as the end of your selection the system will show you a dialog box to save your annotations. You might hover over the annotations to to see, edit or delete them.

### External Resources:
http://annotatorjs.org/
https://github.com/openannotation/annotator/
https://github.com/openannotation/annotator-store
https://www.wikidata.org/
https://www.w3.org/TR/annotation-model/
https://github.com/dahlia/wikidata

