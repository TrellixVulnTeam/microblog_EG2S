# QuantamixSkillTest


# git

first you need to clone the repository from the link given below 

https://github.com/abhishekm47/microblog


# python

Our whole project is python based and in your current assignment you have to run web application which is flask-python web framework so you have to install python in order to run and work on this assignment 

1. first install python 3.0 + in your machine we recommend yout to install "Anaconda Navigator" it will install the python and
it's essential dependencies

2. download anaconda navigator from this link : https://anaconda.org/anaconda/anaconda-navigator 

3. install anaconda navigator and then use anaconda prompt as your command line it will provide you support for python and pip

### how to setup and run framework
1. first of all you have to install 'virtualenv' in your local machine it's a python package which allow us to create multiple 
   virtual environments for different projects
   
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
   
   This will create a folder with python.exe, pip, and setup tools all ready to go in its own little environment. It will also activate the    Virtual Environment which is indicated with the (HelloWold) on the left side of the prompt.
   
   Anything we install now will be specific to this project. And available to the projects we connect to this environment.
 
4. Connect our project with our Environment


   
   First let’s create a directory with the same name as our virtual environment in our preferred development folder. 
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
    To run our web application, you can install all other essential packages from requirements.txt
    
    >(HelloWold) c:\users\abhishek\dev\HelloWold>pip install -r requirements.txt
    
    
 9. once you are done with installing all this packages it's finally time to run our application
    so within our virtual environment, run following command
    
    >(HelloWold) c:\users\abhishek\dev\HelloWold>python microblog.py
   

 10. Then open your browser of your preference and paste this URL:  http://localhost:5000 
 
 Now copy the link mentioned above and run it in browser, and now finally you'll able run entire web application in debugger mode
 And when you are done with testing press CTRL+C to exit from debugger mode. in the command line




# Working with assignment

1. In frontend we are currently using flask as backend technology 

2. In the current Project root directory navigate to the /app folder


3. now you are in app folderwhere you'll be able to see all features of this assignment framework and you can create a new blueprint or you can work on existing blueprints depending on your assignment  


4. We are using template inheritance in order to avoid repeated code we basically extends templates/layout.html in every other template to import all configuration and navigation bar 

5. In your current assignment we are providing you a basic running application with all data and depending on your assignment you may have to create a new feature or modify the existing one that's the way we will examine your skill as a backend devloper 
 
 6. When you’re done and satisfied with your work you need to submit the work before the deadline which is Saturday (26/01/2019)


 7. When you are ready to submit your work just make a pull request to the same repository and drop a mail on       quantamixsolutions@gmail.com that 
    you have submitted your work and made a pull request
 
 8. Our team will review your work and we'll get back to you as soon as we finish reviewing all othercandidates

 9. we hope that you’ll understand the purpose of this assignment and will use fare methods.


ALL THE BEST  👍


# Contact Us

For any further help in order to setup environment and if you have any other questions and need assistance please reach us out:
Phone No :  +917014969260, +919545558468
Email : quantamixsolutions@gmail.com
Discord : https://discord.gg/Qv9Ptx

 ************************************************************************************************************************************

                                    Quantamix solutions B.V. @2019 All Rights Reserved  



