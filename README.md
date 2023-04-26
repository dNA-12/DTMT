# DTMT (Database Corrections and Integration)

## Added Features

### Context Manager

The Context Manager is used to create key features of navigation and functionality for all databases included in DTMT. In this version of DTMT, its functionality is currently limited to just the employee data. However, by design, the objects classed in this file can and will be applied to all other databases here forward, such as the Tooling Database.

### utils.py Fetch All Function

`fetch_all_records` is a function used in the current state of development to review the database during testing. It will be used later to apply certain elements of the specific databases to different data analysis functions.

### emp_database.py

The `emp_database.py` file has undergone a total overhaul as more effective ways of database management are learned. Now, this file is used to store functions that directly interact with the created database. Before, the file was attempting to house and manipulate the employee database outside of the `main.py`. This had several obvious pitfalls and needed to be corrected promptly before moving further in the application.

## What's Next

### Further Debugging

The register page has a number of small bugs that need to be ironed out, along with a few within the database. These are minor and not considered major issues; they will be adjusted accordingly.

### Login Screen Functionality

The next major component of this application will be the functionality of the login page, which will function quite similarly to the register page but with fewer features and moving components.
