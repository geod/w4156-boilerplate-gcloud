This code is used for the purposes of COMS 4156 - Advanced Software Engineering course at Columbia University. 
This is a boilerplate python flask code with configurations for Circle CI and google cloud.

# Tutorial 

Please log into github before progressing with the next steps.

### Step 1: First things first!

Grab your free google credits by following <a href='www.google.com'> this post </a> in piazza.

### Step 2: Fork

Fork this repository into your github. From now on, we will be working on your forked repository. 

How to fork ? <br/>
Look out for a button called `fork` in the top right of this page. It will create a replica of this repository and put in your github account. 

### Step 3: Clone

Open termnal -> go to any folder -> clone your forked repository into your local folder. 

How to clone? <br/>
Look out for a button called `clone` in the top right of the repository. Once you click that you will get a link like this `https://github.com/<your-name>/<your-repository-name>.git` 

Copy that and go to your folder and type the command: <br/>
`git clone <your-forked-repository-GIT-URL>`

### Step 4: Repo as origin

Now set this repository as your origin. 

How? <br/>

`git remote add origin <your-forked-repository-GIT-URL>`
    
### Step 5:Setting up CIRCLE CI. 

1. Go to <a href='https://circleci.com'> CircleCI </a>
2. Sign up for a free account. You can login using github (easy way). Else, you can signup and later authorize github account. 
3. Click on `projects` on the left pane -> `Add Project` -> `Setup Project` (Note: it might take sometime to sync the projects in your github into the Circle CI.)
4. Choose the following:
    * Operating System - Linux
    * Platform - 2.0
    * Language - Python
5. click `start building`
    
### Step 6: Setting up Google Cloud & Project

Login into <a href='https://cloud.google.com'>gcloud</a> using the account that you used for free credits. (Note: If you signed in using another account, switch account to the one that you used to grab free credits.)

1. If you are using google cloud first time, it will ask you to accept some terms, please do so.
2. On the top left -> click on `select a project`. If you have already used google cloud before and you have also created a project before, then you may see another project name there, even then click on it.
3. It will open a small pane -> Ensure that organization is `columbia.edu`, if not then select that.
4. Then, click on `+` button 
4. Give a project name say in this case `ase-boilerplate`.
5. Also, edit the Project ID and set it also to `ase-boilerplate` other wise, google adds some randome digits to the Project ID and we need this Project ID through out. So it is better if Project ID and Project Names are same.
6. click `Create`.

## Step 7: Enable App Engine Admin API & get Client Secret

1. click on `Console`
2. In the Search Bar -> search for `Google App Engine Admin API` -> click `Enable`
3. Click on "Credentials" -> click on `Create Credential` -> select `Service Account Key`
4. From the drop down of Service Account -> select `Compute Engine default service account`
5. For the Key Type: select JSON
6. click `create`.
7. A json file with name similar to `<ase-boilerplate-some-number>.json` will be downloaded on to your system. Remember the folder it is downloaded to, we need this later.

### step 8: Setting secret in Circle CI
1. Go to <a href='https://circleci.com'> CircleCI </a> -> click on `app`
2. Click on `Projects`
3. Click on little gear (notation for settings!) that is next to your project which is `ase-boilerplate`
4. Click on `Environment Variables`
5. Click on `Add Variable`
6. For Name: `CLIENT_SECRET`
7. Now, go to the folder where JSON file is downloaded previously and run this command: <br/>
    `base64 <ase-boilerplate-some-number>.json | pbcopy`
   It encodes the file into base64 format and copies into your clipboard. 
8. Now go back to browser and for value: press the paste buttons (CMD + V on Mac / CTRL + V on windows)

### step 9: Update circle.yaml file
In your local repository, update `circle.yaml` file by replacing the `<your-gcloud-project-id>` at two places with your Project ID from google cloud. 

Then,

`git add circle.yaml` <br/>
`git commit -m 'updating circle.yaml with project id'` <br/>
`git push origin master` <br/>

How do I find my project Id? <br/>
1. Go to <a href='https://cloud.google.com'>gcloud</a> and on top left select the project.
2. It opens a new pane, in that look for the Project ID corresponding to the project name you gave. In our case, it is `ase-boilerplate`

### step 10: Verify build in CircleCI
Step 8 would trigger a new build and release in Circle CI. 
To verify:
1. Go to `projects` -> `your project` -> open the lates build which will be like `master #some-number`
2. If everything is good -> build will succeed and the app will be deployed into google app engine. 
3. you can also verify that by going to `https://<your-gcloud-project-id>.appspot.com` which will show a message like starting with `hello`

### step 11: Setting up Google Cloud SDK & App Engine SDK in your local system

1. Following this link and perform the 3 steps under the `Interactive Installer` section: <br/>
<a href='https://cloud.google.com/sdk/downloads#interactive'>Google Cloud SDK</a>
2. Following this link and perform the steps from 3rd - 5th: <br/>
<a href='https://cloud.google.com/appengine/docs/standard/python/download'>App Engine extension for Python</a>
3. `cd <your-local-repository / folder>` in our case `cd ase-boilerplate`
4. `mkdir -t lib`
5. `pip install -r requirements.txt -t lib`
6. `dev_appserver.py ./`
7. Now, you will be running the application locally (but you are mimicking App Engine framework locally!). So now checkout <a href='http://localhost:8080'>localhost:8080</a>. You should be greeted with `hello` message

## Licensing

Copyright (C) 2018 Columbia University.
