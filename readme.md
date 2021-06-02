
Install project dependency:
    Make sure you are connected to <venv_name>, the cmd prompt should look like " ( <venv_name> ) c:\something " , and install the dependencies declared at the "requirements.txt". 
    "requirements.txt" contains a list of items to be installed using pip install like so:
    `py -m pip install -r requir ements.txt`


In our case we changed the virtual enviroment path for this project, so activate it sa:
        `E:\WindowsUserProfile\Desktop\prosjekter\ProjPy\Envs\venv1\Scripts\activate`
        NOTE: in case if you're using "Powershell", you may encouter the fleg err:  
            "...Scripts\activate.ps1 is not digitally signed. You cannot run this script on the current system..."
            In that case change the "ExecutionPolicy" as follows:  
            `Set-ExecutionPolicy Unrestricted -Scope Process`  

Connect a project with the virtual environment  
    `setprojectdir "<project_path>" `

This project is structured as "Flask’s Application Factory"  
    https://hackersandslackers.com/flask-application-factory

Run the project:  
`python .\wsgi.py`  


# **Handle User Accounts & Authentication in Flask with Flask-Login**  
https://hackersandslackers.com/flask-login-user-authentication  


UserMixin from Flask-Login package:  
UserMixin is a helper provided by the Flask-Login library to provide boilerplate methods necessary for managing users. Models which inherit UserMixin immediately gain access to 4 useful methods: 
    - is_authenticated: Checks to see if the current user is already authenticated, thus allowing them to bypass login screens.  
    - is_active: If your app supports disabling or temporarily banning accounts, we can check if user.is_active() to handle a case where their account exists, but have been banished from the land.  
    - is_anonymous: Many apps have a case where user accounts aren't entirely black-and-white, and anonymous users have access to interact without authenticating. This method might come in handy for allowing anonymous blog comments (which is madness, by the way).  
    - get_id: Fetches a unique ID identifying the user.  