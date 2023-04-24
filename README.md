Added Features:
Context Manager:
Used to create key features of navigation and functionality for all databases included DTMT. In this version of DTMT, it's functionality is currently limited to just the employee data. However, by design, the objects classed in this file can and will be applied to all other databases here forward. i.e the Tooling Database.

utils.py Fetch All Function:
fetch_all_records is a function used in the current state of development to review the database during testing, it will be used later apply certain elements of the specific databases to different data analysis functions.

emp_database.py:
Total overhaul of the database file as I learn more effective ways of database management. Now this file is used to store functions that directly interact with the created database. Before, the file was attempting to house and manipulate the employee database outside of the main.py. This has several obvious pitfalls and needed correctly promptly before moving further in the application.

What's Next
Further Debugging
The register page a number of small bugs that need ironed out along with a few within that database. These are minor and not considered a major issues, they will be adjusted accordingly.

Login Screen Functionality
The next major component of this application will be the functionality of the login page, which will function quite similarly to the register page with less features and moving components.
