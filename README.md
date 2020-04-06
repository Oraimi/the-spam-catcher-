# The-Spam-Catcher
[The Spam Catcher](http://35.222.93.157:5000/)
### Setup
* __Windows__
 <br> * clone the repo
 <br> * cd SpamProject
 <br> * env\Scripts\activate.bat
 <br> * python run.py
 <br> * open your web browser - http://127.0.0.0:5000
 *  __Linux/Unix__
 <br> * clone the reop
 <br> * cd SpamProject
 <br> * source ./env/Scripts/activate
 <br> * change line 171 in SPAM_WEB_APP/routes.py 'static\\data' to 'static/data'
 <br> * change line 189 in SPAM_WEB_APP/routes.py 'file.split('\\')[-1]' to 'file.split('/')[-1]'
 <br> * python run.py
 <br> * open your web browser - http://127.0.0.0:5000
 ### This is how Naïve Bayes classifier has been built
 ### Functional requirements
### Home - displays all users latest scans <br>
 ![image](https://user-images.githubusercontent.com/20130001/71548917-2bf0cf00-29db-11ea-8f48-9e232e5a5139.png)
### Login <br>
![image](https://user-images.githubusercontent.com/20130001/71548926-42972600-29db-11ea-829a-9b7369417717.png)
![image](https://user-images.githubusercontent.com/20130001/71548929-5b9fd700-29db-11ea-9f6f-e36d45e1e753.png)
### ReSet Password <br>
![image](https://user-images.githubusercontent.com/20130001/71554177-e0bdd700-2a41-11ea-8954-e1c05975e7ab.png)
### Sign Up <br>
![image](https://user-images.githubusercontent.com/20130001/71548930-6d817a00-29db-11ea-82c4-5bf0d610e9b9.png)
### Home after logged in to the system <br>
![image](https://user-images.githubusercontent.com/20130001/71548941-99046480-29db-11ea-9946-30d971e01055.png)
![image](https://user-images.githubusercontent.com/20130001/71548953-b46f6f80-29db-11ea-9f0e-4caa6880dcc4.png)
### View previous scans of yours (OLD SCANS) <br>
![image](https://user-images.githubusercontent.com/20130001/71548960-cea94d80-29db-11ea-9166-9d45b86f1f66.png)
### New Scan by pasting content <br>
![image](https://user-images.githubusercontent.com/20130001/71548969-eb458580-29db-11ea-9c65-104230b29498.png)
### Scan by upload (.txt and .zip) <br>
![image](https://user-images.githubusercontent.com/20130001/71548971-04e6cd00-29dc-11ea-9c9e-971b736c3999.png)
### Detail View of scans (Zip, txt, or string) <br>
![image](https://user-images.githubusercontent.com/20130001/71554188-1662c000-2a42-11ea-8573-aa2985321d9b.png)
### Profile section <br>
![image](https://user-images.githubusercontent.com/20130001/71548979-28117c80-29dc-11ea-8022-d7ed63f04b55.png)
 ### Non-Functional requirements
*Usability
  <br> Handling large amounts of data - checked
  <br> The program should be handy and easy to use  - checked
<br>*Performance 
  <br> The program should be accurate and fast - checked
  <br> Identifying errors - include 

