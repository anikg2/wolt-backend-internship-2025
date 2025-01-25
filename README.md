
##  Submission by Anik Ghosh  

Hello, and hope you are doing well!

My submission of the DOPC service is written in Python, and I would like to be a part of your team in Berlin. The project and its dependencies have been managed with [uv](https://docs.astral.sh/uv/), but it is not necessary to install `uv` to run the service.

### Installation Procedure
Please install Python 3.12 or newer from this [link](https://www.python.org/downloads/).
Once Python has been installed, you will need to install the python packages called `fastapi`, `httpx`, and `uvicorn` to run the service. You will also need `pytest` and `pytest-asyncio` to run the tests.

The simplest way to do this is with `pip`, which is installed alongside Python.
Please run the following two commands to install the 5 aforementioned packages:
`pip install fastapi httpx uvicorn` 
`pip install pytest pytest-asyncio`
These are the only necessary packages.
### (Optional) Use a uv environment instead of installing packages
If you already have uv installed, I have provided an evironment in the root project folder. To activate it please open a terminal in the root directory of my project, and enter the following command:
`source .venv/Scripts/activate ` 
If this does not work, please try installing the packages with pip instead.

### Running the service
Once the packages have been installed, please extract the `anik-submission.zip` file, which I have uploaded on [Google Drive](https://drive.google.com/drive/u/1/folders/1gaiDW9JAqB4pNxK2XwXgMgQAnSx2ZQZI) along with this document. You will also find the unzipped project files in a folder in the same directory as this document and the `anik-submission.zip` file. Once the files have been extracted and the above five packages have been installed, please navigate to the project root and simply enter the following command:
`python -m dopc`
By default, the dopc service runs on port 8000, but you can change this with the `--port` argument. If you would like to use a different port number, please run the following command from the project root:
`python -m dopc --port 3333`, where 3333 is an example port number.
All source code for the service is available in the folder called `dopc` in the project root. It has been modularized for maintainability.
### Running the tests
All tests are available in the `tests` folder in the project root. Please run them by simply running the command `pytest` from the project root.

### Additional Points
- I have used the Haversine formula to calculate the shortest distance between two points, given their latitude and longitude coordinates. 
- The code for this project is on my GitHub in a forked repository [anikg2/wolt-backend-internship-2025](https://github.com/anikg2/wolt-backend-internship-2025)
- If you like my work, please contact me at [anik.ghosh@rwth-aachen.de](mailto:anik.ghosh@rwth-aachen.de) or connect with me on [LinkedIn](https://www.linkedin.com/in/anik-ghosh-05b70a328/).

## Thank you very much, and hope to hear from you soon!