# Readme

## Instructions:
1.  **Clone the Repository:**
  
        `git clone https://github.com/NaviRocker/iVedha-Task.git` 
    
2.  **Test 1:**
    
    -   Change into the `Test1` directory within the cloned repository.
        
        `cd Test1` 
        
***Run the Script:***
 -   Execute the script using the following command:
        `python script.py`
Certainly! Below are step-by-step instructions to run the `webservices.py` script:

#### Prerequisites for 2nd Part:

 - Install the required Python packages using the following command:
    ```bash
    pip install Flask elasticsearch
    ```
**Run the Script:**
   - Execute the script using the following command:
     ```bash
     python webservices.py
     ```

**Access the Web Services:**
   - The Flask web server will start, and you can access the web services at `http://127.0.0.1:5000/` in your web browser.

**Use the API Endpoints:**
   - You can use the following API endpoints:
     - **Add Data to Elasticsearch:**
       - Send a POST request to `http://127.0.0.1:5000/add` with a JSON file attached. Make sure the file format is JSON.
     - **Health Check:**
       - Send a GET request to `http://127.0.0.1:5000/healthcheck` to get the overall health status.
     - **Specific Health Check:**
       - Send a GET request to `http://127.0.0.1:5000/healthcheck/service_name` to get health status for a specific service (replace `service_name` with the actual service name).

**Stop the Web Server:**
   - Press `Ctrl+C` in the terminal where the Flask app is running to stop the web server.

3. **Test 2:**
- Switch to the `Test2` Folder.
- Ensure Ansible is installed on your machine. If not, install it using: 
    `pip install ansible`

#### Verify Installation
`ansible-playbook assignment.yml -i inventory.ini -e action=verify_install` 

#### Check Disk Usage
`ansible-playbook assignment.yml -i inventory.ini -e action=check_disk` 

#### Check Status
`ansible-playbook assignment.yml -i inventory.ini -e action=check_status`

4. **Test 03:**
- Try it on Google Colab
