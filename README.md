# microblogging-beta
this is a beta version of a micro blogging website developed by  Quantamix solutions

### how to setup and run framework
1. first of all you have to install 'virtualenv' in your local machine it's a python package which allow us to create multipe 
   virtual environments for diffrent projects
   
   a. in order to install virtualev make it sure that you have python and pip command line install
   
   b. when you have python and pip running in your local machine then follow the following command's 
    
   >pip install virtual env
   
   c. Now we have virtualenv installed which will make it possible to create individual environments
     to test our code in. But managing all these environments can become cumbersome. So we’ll pip install another helpful package…
   
2. then 
   > Install virtualenvwrapper-win
   
   This is the kit and caboodle of this guide.

3. Make a Virtual Environemt,Lets call it HelloWold. All we do in a command prompt is enter 
   > mkvirtualenv HelloWold
   
   This will create a folder with python.exe, pip, and setuptools all ready to go in its own little environment. It will also activate the    Virtual Environment which is indicated with the (HelloWold) on the left side of the prompt.
   
   Anything we install now will be specific to this project. And available to the projects we connect to this environment.
 
4. Connect our project with our Environment


   
   First lets create a directory with the same name as our virtual environment in our preferred development folder. 
   In this case mine is ‘dev’
   
   > (HelloWold) c:\users\abhishek>cd dev
   
   
   > (HelloWold) c:\users\abhishek\dev>mkdir HelloWold
   
   
   > (HelloWold) c:\users\abhishek\dev\HelloWold>
   
   Now to bind our virtualenv with our current working directory we simply enter ‘setprojectdir .’
   
   > (HelloWold) c:\users\abhishek\dev\HelloWold>setprojectdir
   
5. Now next time we activate this environment we will automatically move into this directory!
   Buttery smooth.
   
6. Deactivate
   
   Let say you’re content with the work you’ve contributed to this project and you want to move onto something else in the command line.    Simply type ‘deactivate’ to deactivate your environment.
   Like so:
   
   > (HelloWold) c:\users\abhishek\dev\HelloWold>deactivate
   
   
   > c:\users\abhishek\dev\HelloWold>
   
   Notice how the parenthesis disappear.
   You don’t have to deactivate your environment. Closing your command prompt will deactivate it for you. As long as the parenthesis are    not there you will not be affecting your environment. But you will be able to impact your root python installation.
   
   
   
7. Workon
   
   Now you’ve got some work to do. Open up the command prompt and type ‘workon HelloWold’
   to activate the environment and move into your root project folder.
   
   Like so:
   
   >c:\users\abhishek\dev\HelloWold>workon HelloWold
   
 8. Now you are done with setting up virtual environment, let's install few more packages which are specifically required in order 
    to run our web application,you can install all other essential packages from requirements.txt
    
    >(HelloWold) c:\users\abhishek\dev\HelloWold>pip install -r requirements.txt
    
    
 9. once you are done with installing all this packages it's finally time to run our application
    so within our virtual environment, run following command
    
    >(HelloWold) c:\users\abhishek\dev\HelloWold>python app.py
    
    now it will run our entire framework in debugger mode and will give you scrap like that: 
    
    C:\Users\ABHISH~1\Envs\TTBPbeta\lib\site-packages\flask_sqlalchemy\__init__.py:794: FSADeprecationWarning:     SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
  'SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and '
 * Serving Flask app "ttb" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
C:\Users\ABHISH~1\Envs\TTBPbeta\lib\site-packages\flask_sqlalchemy\__init__.py:794: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
  'SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and '
 * Debugger is active!
 * Debugger PIN: 415-049-322
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 
 now copy the link mentioned above and run it in browser, and now finally you'll able run entire web application in debugger mode
 and when you are done with testing press >>CTRL+C to exit from debugger mode.
 
 ************************************************************************************************************************************
    
                                            Quantamix solutions @2018 All Rights Reserved  
    
    
<<<<<<< HEAD
>>>>>>> 01ca46f0b56fdc92ca368cf272235d5fd06adf81
=======
>>>>>>> 01ca46f0b56fdc92ca368cf272235d5fd06adf81
