# Pre-requisites for backend team

1. AWS CLI naka-setup na on local device (naka-pin sa GC tutorial)
2. Serverless naka-setup na on local device (naka-pin sa GC tutorial)
3. Python 3.8
4. Git
5. Download Postman

# Cloning the repository

1. Create a folder dedicated to the Photobooth app.
2. Open a terminal inside that folder. `pwd` to make sure that you are in the correct directory.
3. Clone the repository using

```
git clone https://github.com/aws-community-day-ph/api.git
```

# Script to activate the Python environment for the service

Test the terminal to see if it's working

```
echo "Using this service's Python environment"
```

Check python version

```
python --version
```

or

```
python3 --version
```

If command used is `python3 --version`, do `alias python=python3`. Make sure that the version is 3.8.

Activate the virtual environment

```
. $PWD/venv/bin/activate
```

Install all necessary modules from requirements.txt

```
python -m pip install -r requirements.txt
```

# Deploying the code

1. Check if you have successfully setup your AWS CLI profile using `aws configure`.
   - If there are values, just press enter. If there are none, prefer to the tutorial pinned at the backend GC.
2. Deploy your code using `serverless deploy`.
   - If any errors arise, inform Sir Tony nalang at most likely baka permission error lang yan.

# Git stuff

To get the latest version of the code, pull from the origin

```
// git pull origin {branchname}
git pull origin master
```

You can also check the link of your origin when debugging

```
git remote -v
```

---

Before making any changes, create a new branch with the following format: `features/{feature_mo}`

```
git checkout -b features/{new_feature}
```

---

When you're done with your changes, do the following:

```
pip freeze > requirements.txt
git add .
git commit -m "short message here"
git push origin master
```

- `pip freeze > requirements.txt` will print all modules used in the code into the requirements.txt file
- `git add .` will add all changes to the stage
- `git commit -m "short message here"` will finalize the changes and save them
- `git push origin master` will upload the changes to the remote repository (origin)

# To-do list

- Ayusin return responses
- Update status sa dynamodb (pending | uploaded | templated | sent)
- Generate presigned URL of templated image
  - To be discussed: duration ng presigned url
- Do update request function
