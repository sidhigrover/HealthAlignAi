# CogniQ: Collateral Generator

CogniQ is an AI-driven platform designed to generate customized marketing collaterals using voice input. This tool streamlines the process of creating professional marketing materials tailored to user specifications.

## Features

- **Voice Input:** Provide verbal descriptions to create marketing collaterals.
- **Automated Design:** Leverages AI to convert text into custom-designed brochures and materials.
- **User-Friendly Interface:** Simplifies the workflow for users with no technical expertise.

## Set Up

**Fork the Repository:**

   - Click on the "Fork" button in the top right corner of the page. This will create a copy of the repository under your GitHub account.

**Clone the Repository**

   - Replace `your-username` with your GitHub username:

   ```bash
   git clone https://github.com/your-username/CogniQ
   cd CogniQ
   ```

**Set Up the Virtual Environment**

   It's recommended to use a virtual environment to manage project dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows use: venv\Scripts\activate
   ```

## Installation

To set up and run the project, follow these steps:

1. **Install Required Packages**

   Once Python and pip are installed, run the following commands in VSCode or your preferred terminal:

   ```bash
   pip install flask
   pip install pillow
   pip install flask-login
   pip install SQLAlchemy
   pip install requests
   ```

2. **Install Python and pip**

   Ensure that Python and pip are installed on your system. Here's a guide:
   - [How to install python](https://www.geeksforgeeks.org/how-to-install-python-on-windows/)
   - [How to install pip](https://www.geeksforgeeks.org/how-to-install-pip-on-windows/)

---

3. **INSTALL STABLE DIFFUSION**

   **Step 1: Fork the Repository**

   - **Go to the Repository:**
     - Visit the GitHub page of the repository: [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui).

   - **Fork the Repository:**
     - Click on the "Fork" button in the top right corner of the page. This will create a copy of the repository under your GitHub account.

   **Step 2: Clone the Repository**

   - **Open Terminal or Command Prompt:**
     - You can use Git Bash, Terminal, or Command Prompt, depending on your operating system.

   - **Clone the Repository:**
     - Use the following command to clone the forked repository to your local machine. Replace `your-username` with your GitHub username:

       ```bash
       git clone https://github.com/your-username/stable-diffusion-webui.git
       ```

   - **Navigate to the Directory:**
     - Change your directory to the cloned repository:

       ```bash
       cd stable-diffusion-webui
       ```

   **Step 3: Run the Command**

   - **Execute the Script:**
     - Run the following command to start the web UI with API support:

       ```bash
       ./webui.sh --api
       ```
---

## Running the Application

1. **Start the Flask Server**

   Run the following command to start the application:

   ```bash
   flask run
   ```

2. **Start Stable Diffusion**

   To start the stable diffusion model on the local server:

   ```bash
   ./webui.sh --api
   ```

3. **Access the Application**

   Open your web browser and navigate to `http://localhost:5000` to use the application.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue.
