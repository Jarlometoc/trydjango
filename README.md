FibSim Documentation
This web server was created by S. Bur*****, 9-2015 to 1-2016 for a 30cr project in Bioinformatics, Lund University. 

The results of this project, in the form of the code used to make the FibSim website, can be accessed at http://mogwai.plantbio.lu.se:8000/.  The program and website-related files currently reside on the ‘Mogwai’ server at the Department of Biochemistry, Lund University, backed up by Git with a copy of the source-code stored at the GitHub repository under the name of ‘Jarlometoc’. 

Software versions
1.	Bootstrap version 3.3.6
2.	CrispyForms version 1.2.1
3.	Django version1.8
4.	HTML version 5
5.	Jsmol version 13
6.	Python version 3
7.	SQlite version 3.10.1


Django is python-based and functions are divided up into ‘apps’- a fancy word for folders of associated code. 
The main app is trydjango18, which has the code for the actual pages (home/about/contact/main/example) and settings.py, which is where you change email, toggle debugging and other admin functions. 
Other apps are Inputs, Runs and Results. The views.py file for each app is where the action is, and models.py is the associated tables of the database for that particular app.  
The templates folder has all of the html. 
Adding a ‘choice’ to a existing form requires 1) navigating to the Inputs folder, finding views.py and editing the class associated with the form of interest and 2) modifying the associated model in models.py, found in the input folder.  
Each time you modify the model, you need to run ‘makemigrations’ and ‘migrate’, as described above. 
Adding a new table is more complex. You need to add a new class to views.py (use older input classes as a ref), add a new class to models.py (again follow existing class formats), add a table to the HTML and finally add a URL (urls.py) to allow the form to find the associated class in views.py.  
Adding pages requires modifying views.py found in trydjango18 and the urls.py found there.
