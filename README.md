<br />
<div align="center">
  <a href="https://gitlab.pg.innopolis.university/code-forcer-ise-5">
    <img src="assets/logo.svg" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">CodeForces</h3>

  <p align="center">
    Effective and simple tool for uploading grades from CodeForces contests to Moodle
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li>
          <a href="#built-with">Built With</a>
        </li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li>
          <a href="#installation">Installation</a>
          <ul>
            <li>
              <a href="#run-the-backend-api">Run the backend API</a>
            </li>
            <li>
              <a href="#run-the-web-frontend">Run the web frontent</a>
            </li>
          </ul>
        </li>
      </ul>
    </li>
    <li>
      <a href="#features">Features</a>
      <ul>
        <li>
          <a href="#backend">Backend</a>
        </li>
        <li>
          <a href="#frontend">Frontend</a>
        </li>
      </ul>
    </li>
    <li>
      <a href="#troubleshooting">Troubleshooting</a>
    </li>
  </ol>
</details>

## About The Project
<div align="center">
  <img src="assets/CodeForcer.jpeg" alt="Homepage" width="1024"/>
</div>
Our project is the most pizdatiy

### Built With
- Frontend: [![React][React.js]][React-url]
- Backend: [![FastAPI][Fastapi]][Fastapi-url]
- Containerization: [![Docker][docker]][docker-url]
- Database: [![SqLite][sqlite]][sqlite-url]


## Features
### Backend 
- Adding students' handles
- Downloading CodeForces submissions
- Editing students' handles
- Creating .csv file with results of the CodeForces contest that can be uploaded to Moodle
- Centralized students' handles
- Application of late submissions policy

### Frontend 
- Dark&Light theme
- Smooth animations
- Sleek and intuitive design

## Getting Started

### Installation

#### Clone this repository

```
git clone https://gitlab.pg.innopolis.university/code-forcer-ise-5/code_forcer.git
```

#### Install the requirements
```
pip install ./backend/src/requirements.txt
```

### Run the backend API

Windows
```
python ./backend/src/main.py
```

GNU/Linux 
```
python3 ./backend/src/main.py
```

### Run the web frontend

You should have Node.js on your machine. To install required version follow this [guide](https://tecadmin.net/install-latest-nodejs-npm-on-linux-mint/).
After successful installation:

```
cd frontend
npm i
npm run build
```


## Roadmap

See the [roadmap.sh](https://roadmap.sh/r/codeforcer) for a full list of proposed features (and known issues).


## License 

Distributed under the MIT License. See `LICENSE` for more information.



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot]: https://ibb.co/640xgDW
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Fastapi]: https://img.shields.io/badge/fastapi-20232A?style=for-the-badge&logo=fastapi&color=04998a&logoColor=ffffff
[Fastapi-url]: https://fastapi.tiangolo.com/
[docker]: https://img.shields.io/badge/docker-20232A?style=for-the-badge&logo=docker&logoColor=ffffff&color=0e1756
[docker-url]: https://www.docker.com/
[sqlite]: https://img.shields.io/badge/sqlite-20232A?style=for-the-badge&logo=sqlite&logoColor=46a3dc&color=003c58
[sqlite-url]: https://img.shields.io/badge/sqlite-20232A?style=for-the-badge&logo=sqlite&logoColor=46a3dc&color=003c58

