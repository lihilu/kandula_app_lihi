# Kandula Project Application


# What Is Kandula?
Kandula is the a flask based Python web application that will be used in the mid and final project of the course.

The Kandula application has a UI (that will not be part of this course) and backend code which provides data and capabilities to the UI

You main coding tasks throughout the course will be to implement the backend code that is needed to run Kandula properly in production

Kandula will also be the application you will build & deploy (CI & CD) in your mid and final project

> For an introduction to Kandula we recommend you see [this video](https://drive.google.com/file/d/130FJG422J3M5OuEi84byE9VBU_wDUy0S/view?usp=sharing)

# How Can I Run It?
There are two ways of running the Kandula application
* [Virtualenv](#virtualenv)
* [Docker](#docker)

## Virtualenv
> :warning: Make sure you have Python 3.7 and above installed. \
> :warning: Make sure you create your Virtualenv with Python3 (Run `python -V` ins the command line when in Virtualenv)
1. In the `kandula` folder, create & activate Virtualenv
   ```shell script
   $ virtualenv venv
   $ source venv/bin/activate
   ```
2. When in Virtualenv, install all the Kandula dependencies using `pip`
   ```shell script
   $ pip install -r requirements.txt
   ```
3. Run the application from command line:
   ```shell script
   $ FLASK_ENV=development AWS_ACCESS_KEY_ID=xxxxx AWS_SECRET_ACCESS_KEY=xxxxx bin/run
   ```
> AWS_SECRET_ACCESS_KEY & AWS_ACCESS_KEY_ID values should be set to your AWS credentials

If no errors appear in the log, the app should run on `http://localhost:5000`

## Docker
> Make sure you have Docker installed and that you are in the ROOT folder
1. Build the Docker image locally
   ```shell script
   $ docker build -t opsschool/kandula .
   ```

1. Run the Docker container with the mandatory env variables
   ```shell script
   $ docker run -it -e FLASK_ENV=development -e AWS_ACCESS_KEY_ID=xxxxx -e AWS_SECRET_ACCESS_KEY=xxxxx -e AWS_DEFAULT_REGION=<the-desired-region> --name kandula-app --rm -p 5000:5000 opsschool/kandula
   ```
> AWS_SECRET_ACCESS_KEY & AWS_ACCESS_KEY_ID values should be set to your AWS credentials

If no errors appear in the log, the app should run on `http://localhost:5000`

# How Can I Test My Code?
1. Run the app via [Virtualenv](#virtualenv) or [Docker](#docker)
2. Use Pytest - Pytest is a library to run tests in Python. We will learn more about this later in the course. The current Pytest is aim to test the basic use cases you need to implement. If all tests pass, it means your implementation is correct. To tun Pytest you need to:
   1. Make sure you are on Virtualenv
   2. From the root folder run the following `pip` command to install all required dependencies
   ```shell script
   $ pip install -r requirements.txt
   ```
   3. Run Pytest:
   ```shell script
   $ pytest
   ```
   **IMPORTANT NOTE:** Some tests may fail due to missing implementation. Usually you will not merge code unless code passes, but for our case most of the code will only be implemented in **final project**. So some tests will still fail in first implementations and that is **OKAY**.

# Logging
While running, the Kandula application produces a `kandula.log` at the root path of the application. Use the log as an additional tool to debug your application

# Where Do I Implement My Code?
Kandula has additional code that is needed in order for it to run including UI, configuration and other application runtime files.
Much of this code is out of scope for this course and is not needed to be touched.

You should only implement code in places you see a `TODO` comment explaining you what you need to perform.

Feel free to extract functions or files if you wish to.

## Important Notes PLEASE READ!
1. Notice that the Kandula implementation uses [Python classes](https://docs.python.org/3/tutorial/classes.html#classes).
 Though **you do not need to implement any classes** it is important you understand how classes & objects look and used in Python
 
    [Click here](https://docs.python.org/3/tutorial/classes.html#classes) to Read more about classes and object in Python (Do not need to go beyond section `9.4`)
1. You can extract or create any additional methods or files but in now way should you change the signature or name of the existing methods, classes or files
