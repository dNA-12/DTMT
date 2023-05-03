# DTMT Login, Add Tool Functionality, and Databases Update

This branch, `login-addtool-functionality-databases`, introduces several major updates and changes to the DTMT project compared to previous versions. The primary goal of this update is to form user login-logout functionality, add new functionality for adding tools, and better database support across the application.

## Updates and Changes

1. **User Authentication and Login System**
   
   In this update, a user authentication and login system has been implemented. This allows users to securely create an account, log in, and manage their sessions while using the DTMT platform.

   Key features include:
   - Better register functionality
   - Login functionality
     - Store current user for database query and integration
     - Clearing screens once logged in or out
   - Session management
     - Allowing users to move freely between pages and updating respective databases accordingly

2. **Add Tool Screen Implementation**

   The ability to add tools to the DTMT platform has been introduced. Users can now easily add new tools with a streamlined user interface and guided prompts.

   Key improvements include:
   - Simple forms and input fields
     - Each including dropdown menus for easier searchability
   - Validation of input data
     - Functional communication and storage to the newly added tooling database
   - Tool categorization
     - Via part number, operation, employee, machine, description, and time of incident

3. **Improved Database Support**

   The database system has been updated to provide better support for storing and managing user and tool data. This update ensures a more stable and efficient experience for users as they interact with the platform and a more intuitive approach for future back-end development and implementation.

   Key changes include:
   - Enhanced data retrieval and storage methods
   - Better database management practices
   - New database additions: tool.db and current_user MainApp attribute

4. **Utils.py Implementations**

   With the new 'create_searchable_dropdown()' function, searchable dropdowns will now be a process of relative ease and high customization. This will be fantastic for future updates that will contain new data analysis features.

## What's Next

   Once a minor bug-fix patch releases for this update, to iron out some of the smaller quirks in the entry conditions, I will be pushing further into the realm of in-application data analytics. This will take time and will come in smaller updates as the application evolves into its final stages. After this major implementation, styling will come last. As this is a flexible development process, there may be other changes implemented between these larger features. Stay tuned!
