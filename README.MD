 <h3 align="center">Moon Slot Machine</h3>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a> 
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li> 
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li> 
    <li><a href="#contact">Contact</a></li> 
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This repository contains a simple slot machine backend which offers the ability to create players
and then use them to "spin" the slot machine and earn prizes.
In addition it supports a configurable goals/mission setup which allows users to hit certain goals
and as a result earn bigger prizes.
The project was built using Python, FastAPI and a Redis database.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Running this project requires the following to be installed:
* Redis (either a local or a remote database)
* Python 3.11+

<!-- USAGE EXAMPLES -->
## Usage

To run through a Python IDE:
* Open the project in your IDE
* Run the main.py script. You can change the port as you see fit (default is 8000)

To run from terminal:
* Go to project directory
* Run uvicorn main:app --host 0.0.0.0 --port 8000

To run tests:
* Open the project in your IDE
* Locate the tests directory and run required tests. Please note that integration tests
execution requires having the service started and a Redis DB available. Integration tests WILL write additional data to the Redis DB used by the service

After running the service you can browse to the FastAPI openapi.json file to view the exact API documentation
for example here: [http://localhost:8000/docs](http://localhost:8000/docs)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Amir Avni - [avamir10@gmail.com](mailto:avamir10@gmail.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
