# Internship Portal

This repository presents the code of an internship portal.

## Guide to Setting Up the Project

This guide will walk you through setting up the project locally. After downloading or cloning the files, proceed as follows:

### Step 1: Creating the Database & Populating its Data

1. Open **MySQL Workbench** or your preferred MySQL client.
2. Run the script **`InternshipPortalDB.sql`** to create the database (this is the DML part).
3. Next, run the script **`InternshipPortalDummyData.sql`** to populate the database with some essential data.

### Step 2: Configuring the Application

1. Open the file **`app2.py`** in a text editor. (VS Code Recommended)
2. Locate the `get_db_connection` method.
3. Edit the **root password** in the connection string to match the MySQL root password on your machine.
   - This is the **only change** required.

### Step 3: Running the Application

1. Save your changes to **`app2.py`**.
2. Run the application (python app2.py in terminal)




