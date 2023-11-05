# Tugas Besar 2 IF2123 Aljabar Linier dan Geometri
## Member :
1. Filbert / 13522021
2. Juan Alfred Wijaya / 13522073
3. Azmi Mahmud Bazeid / 13522109

# Flask Development Setup and Usage Guide

This guide will walk you through setting up a virtual environment and running a Flask application for the first time.

## Initialize Virtual Environment
### Only if you haven't set up the virtual environment.
1. Open your terminal or command prompt.

2. Navigate to your project directory.

3. Create a virtual environment named "env" using Python's built-in `venv` module:

    ```
    python -m venv env
    ```

4. Activate the virtual environment (Windows):

    ```
    env\Scripts\activate
    ```

    Or activate the virtual environment (macOS/Linux):

    ```
    source env/bin/activate
    ```

## Install Dependencies

1. Make sure your virtual environment is activated (you should see "(env)" in your terminal prompt).

2. Install project dependencies from the `requirements.txt` file using pip:

    ```
    pip install -r requirements.txt
    ```

## Run the Flask Application

1. Ensure your virtual environment is still activated (you should see "(env)" in your terminal prompt).

2. Run the Flask application:

    ```
    flask run --debug
    ```

    This will start your Flask app, and you should see output indicating the server is running. By default, it will run on http://127.0.0.1:5000/.

3. Open your web browser and navigate to the URL mentioned in the output to access your Flask application.

## Deactivate Virtual Environment

When you're done working on your Flask application, you can deactivate the virtual environment:

1. Simply run the following command:

    ```
    deactivate
    ```

    This will return you to your system's global Python environment.

That's it! You've set up a virtual environment for your Flask project, installed the necessary dependencies, and run your Flask application. Enjoy developing with Flask!

