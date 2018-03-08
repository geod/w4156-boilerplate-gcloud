This code is used for the purposes of COMS 4156 - Advanced Software Engineering course at Columbia University, New York. 
This is a boilerplate python flask code along with configurations for Circle CI and Google Cloud.

# Setup Instructions 

Please log into github before progressing with the next steps.

### Step 1: First things first!

Grab your free google credits by following <a href='https://piazza.com/class/jchzhd6cdxz4dy?cid=31' target="_blank"> this post </a> in piazza.

### Step 2: Fork

Fork this repository into your github. From now on, we will be working on your forked repository. 

How to fork ? <br/>
Look out for a button called `fork` in the top right of this page. It will create a replica of this repository and put it in your github account. 

### Step 3: Clone

Open termnal -> go to any folder -> clone your forked repository into your local folder. 

How to clone? <br/>
Look out for a button called `clone` in the top right of the repository. Once you click that you will get a link like this `https://github.com/<your-name>/<your-repository-name>.git` 

Copy that and go to your folder and type the command: <br/>
`git clone <your-forked-repository-GIT-URL>`

### Step 4: Set Repository as origin

Now set this repository as your origin. 

How? <br/>

`git remote add origin <your-forked-repository-GIT-URL>`

### Step 5: Set up Google Cloud, Project & App Engine

Login into <a href='https://cloud.google.com'>Google Cloud</a> using the account that you used for free credits. (Note: If you signed in using another account, switch account to the one that you used to grab free credits.)

1. If you are using google cloud first time, it will ask you to accept some terms, please do so.
2. On the top left -> click on `select a project`. If you have already used google cloud before and you have also created a project before, then you may see another project name there, even then click on it.
3. It will open a small pane -> Ensure that organization is `columbia.edu`, if not then select that.
4. Then, click on `+` button 
4. Give a project name say in this case `ase-boilerplate`.
5. Also, edit the Project ID and set it also to `ase-boilerplate` other wise, google adds some randome digits to the Project ID and we need this Project ID through out. So it is better if Project ID and Project Names are same.
6. click `Create`.
7. Search for `App Engine` -> Ensure that Google App Engine Services are available. Upon seeing the home page of App Engine and choosing a language is taking you to a tutorial then it means the services are available.

### Step 6: Set up CIRCLE CI. 

1. Go to <a href='https://circleci.com'> CircleCI </a>
2. Sign up for a free account. You can login using github (easy way). Else, you can signup and later authorize github account. 
3. Click on `projects` on the left pane -> `Add Project` -> `Setup Project` (Note: it might take sometime to sync the projects in your github into the Circle CI.)
4. Choose the following:
    * Operating System - Linux
    * Platform - 2.0
    * Language - Python
5. click `start building`
    
### Step 7: Enable App Engine Admin API & retrieve Client Secret

1. click on `Console`
2. In the Search Bar -> search for `Google App Engine Admin API` -> click `Enable`
3. Click on "Credentials" -> click on `Create Credential` -> select `Service Account Key`
4. From the drop down of Service Account -> select `Compute Engine default service account`
5. For the Key Type: select JSON
6. click `create`.
7. A json file with name similar to `<ase-boilerplate-some-number>.json` will be downloaded on to your system. Remember the folder it is downloaded to, we need this later.

### Step 8: Setup CLIENT_SECRET and GCLOUD_PROJECT_ID variables in Circle CI

1. Go to <a href='https://circleci.com'> CircleCI </a> -> click on `app`
2. Click on `Projects`
3. Click on little gear (notation for settings!) that is next to your project which is `ase-boilerplate`
4. Click on `Environment Variables`
5. Click on `Add Variable`
6. For Name: `CLIENT_SECRET`
7. Now, go to the folder where JSON file is downloaded previously and run this command: <br/>
    `base64 <ase-boilerplate-some-number>.json | pbcopy` <br/>
   It encodes the file into base64 format and copies into your clipboard. 
9. Now go back to browser and for value: press the paste buttons (CMD + V on Mac / CTRL + V on windows)
10. Again Click on `Add Variable`
11. For Name: `GCLOUD_PROJECT_ID`
12. For Value: put your your Project ID from google cloud.

How do I find my project Id? <br/>
1. Go to <a href='https://cloud.google.com'>Google Cloud</a> and on top left select the project.
2. It opens a new pane, in that look for the Project ID corresponding to the project name you gave. In our case, it is `ase-boilerplate`

### Step 9: Verify build in CircleCI

Step 8 would trigger a new build and release in Circle CI. 
To verify:
1. Go to `projects` -> `your project` -> open the lates build which will be like `master #some-number`
2. If everything is good -> build will succeed and the app will be deployed into google app engine. 
3. you can also verify that by going to `https://<your-gcloud-project-id>.appspot.com` which will show a message like starting with `hello`

### Step 10: Database Setup (if required for your project)
#### Create a SQL instance.
1. Home Page -> Menu -> SQL
2. Create Instance -> Select MySQL -> Select Second Generation 
3. give a name (may be "mysql1" )-> and give a simple password (may be "root").
4. Next, wait for couple of minutes for google cloud to process your request and create an instance
5. Once, it is ready, you will get a green tick next to it. 
6. Click on "mysql1" (or your instance name) once you see a green tick next to it. 
7. There will be a pane called `Connect to this instance`. In that copy the value of `Instance connection name`.

#### Setting configuration in your code
1. Go to your code
2. go to app.yaml -> update `<YOUR_CONNECTION_NAME>`  with `Instance connection name` you copied in previous step
3. likewise update `<YOUR_USERNAME>` with username and `<YOUR_PASSWORD>` with password.
4. Commit your code and push it to repo. It will trigger a build in Circle CI.
5. Once your build has succeeded, then go to `https://<your-gcloud-project-id>.appspot.com/databases` and you should see a list of schemas/databases that come by default in your mysql instance.

#### (optional) connecting to SQL instance locally 
1. Go to Home Page -> Menu -> SQL -> "mysql1" (or your instance name)
2. Click on Authorization tab -> For `name` put something like "HOME IP" -> for `Network` put your public IP address. This is called whitelisting IP address. Google cloud or any cloud providers by default block access from new IP addresses to their services. How do you find your public IP ? Google Search -> "myip"
3. Then click save.
4. Go to `overview` tab -> `Connect to this instance` -> `IPv4 address` -> copy IP Address. You need this to connect to mysql from you local computer. 
5. Open Terminal -> `mysql --host=<IP_ADRESS_YOU_COPIED_PREIVOUSLY> --user=root --password=<YOUR_MYSQL_INSTANCE_PASSWORD>`
6. Once you login succefully: try `show schemas`
7. That will give you the same result as going to `https://<your-gcloud-project-id>.appspot.com/databases`

### Step 11: (optional but highly recommended as a pre-requisite for step 12) Setup Anaconda
If you don't have Python 2.7 in your system, then follow along:
1. Download <a href='https://www.anaconda.com/download/#macos'>Anaconda</a> with Python version 3.6 (Don't get confused about 3.6 here!! We will be creating virtual environment with 2.7 instead of using Anaconda with Python 2.7 version which is a good practice!)
2. Install Anaconda by double clicking the .dmg file 
3. After installation -> Terminal -> `conda create -n python2env python=2.7`
4. `source activate python2env`
5. At this point you have activated virtual environment named `python2env` with packages `python=2.7`. So now if you test `python --version` you will see `python 2.7` as output 
6. At this point, continue your previous work with this virtual environment active. 
7. run `easy_install -U pip`
8. Once you are done, deactivate the environment with `source deactivate`
9. Fun Check: try `python --version` now! (it will show your default python version installed in your system)
10. Before moving to next step do `source activate python2env` as running the system locally requires python2.7 and also we will be installing packages mentioned in requirements.txt in this virtual environment instead of your local base installation. 

### Step 12: Setup Google Cloud SDK, App Engine SDK and Database in your local system
1. Following this link and perform the 3 steps under the `Interactive Installer` section corresponding to your operating system. For our case it is Mac OS (vice versa you can choose Linux / windows based on your OS): <br/>
<a href='https://cloud.google.com/sdk/downloads#interactive'>Google Cloud SDK</a>
2. Following this link <a href='https://cloud.google.com/appengine/docs/standard/python/download'>App Engine extension for Python</a> and perform the steps below (and skip if you already have it): 
    * 1st step (Check your python version by typing  `python --version` in you terminal / shell. If it is python 2.7, then skip the step, else check out optional Step 12 in this file.)
    * 3rd step (perform this step)
    * 4th step (Check if you have git installed by typing `git`. If yes, then skip, else perfrom this step. )
    * 5th step (perform this step)
    
3. In your local system -> `cd <your-repository>` in our case `cd ase-boilerplate` <br/>
4. `mkdir -p lib`
5. `pip install -r requirements.txt -t lib`
6. `pip install -r requirements.txt`. (This is extra step if you are using database setup).
6. `dev_appserver.py ./`
7. Now, you will be running the application locally (in locally mimicked App Engine framework!). So now checkout <a href='http://localhost:8080'>localhost:8080</a>. You should be greeted with `hello` message
8. After you are done, press `ctrl+c` to stop the local server. 

## Licensing

Copyright (C) 2018 Columbia University.
