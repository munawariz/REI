
![GitHub contributors](https://img.shields.io/github/contributors/harizMunawar/REI)
![GitHub forks](https://img.shields.io/github/forks/harizMunawar/REI?style=social)
![GitHub stars](https://img.shields.io/github/stars/harizMunawar/REI?style=social)
![GitHub last commit](https://img.shields.io/github/last-commit/harizMunawar/REI)
![GitHub issues](https://img.shields.io/github/issues/harizMunawar/REI)
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

<p align="center">
  <h3 align="center">REI</h3>

  <p align="center">
    Rapor Elektronik Indonesia
    <br />
    <a href="https://github.com/harizMunawar/REI"><strong>Explore the docs »</strong></a>
    <br />
    <br />    
    <a href="https://github.com/harizMunawar/REI/issues">Report Bug</a>
    ·
    <a href="https://github.com/harizMunawar/REI/issues">Request Feature</a>
  </p>
</p><br>

<!-- TABLE OF CONTENTS -->
## Table of Contents

- [Table of Contents](#table-of-contents)
- [About The Project](#about-the-project)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Admin Site](#admin-site)
  - [Export HTML to PDF](#export-html-to-pdf)
- [Our Team](#our-team)
- [Contributing](#contributing)

<!-- ABOUT THE PROJECT -->
## About The Project

REI or Rapor Elektronik Indonesia is a Django PWA that handle the flow of school report card management.
This app can produce a digital school report card in the form of PDF file.

### Built With

* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Visual Studio Code](https://code.visualstudio.com/)
* Love

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

These are list of things you need to have before you use the project and how to install them.
* Python<br>
Download the Python installer [here](https://www.python.org/downloads/) (preferably Python 3.8)<br>
Run the installer
* Text Editor<br>
You can choose any text editor that suits you the most, but I reccomend using Visual Studio Code<br>
Download the VSCode installer [here](https://code.visualstudio.com/download)<br>
Run the installer

### Installation
To get started, Install the requirements.txt<br>
You can use any virtual environment you want, but I prefer [virtualenv](https://pypi.org/project/virtualenv/)

__1. Setting Up Virtual Environment__<br>
Open terminal in the root directory of this project
```
pip install virtualenv 
virtualenv env
```

__2. Activate Your Virtual Environment__<br>
For Windows
```
cd env/Scripts
activate.bat
```
For Linux
```
cd env/bin
activate
```

__3. Install The requirements.txt__<br>
In the root directory of this project
```
pip install -r requirements.txt
```

__4. Migrating The Models__<br>
In the root directory of this project
```
manage.py migrate
```

__5. Create SuperUser Account__<br>
In the root directory of this project
```
manage.py createsuperuser
```
You can input any data for the superuser account
<p style="color: red; font-weight: bold">BUT PLEASE INSERT 'A' AS A LEVEL FOR THE USER</p>

__6. Running The Server__<br>
In the root directory of this project
```
manage.py runserver
```
Default port is 8000, so access the [server](127.0.0.1:8000) there

### Admin Site
To access the admin site visit the <text style="background-color: #A9A9A9; padding: 3px; border-radius: 4px; color: white">/admin</text> url<br>
You will need your "Nomor Induk" & "Password" from [step 5](#installation) as a login authentication

### Export HTML to PDF
To properly use the export to PDF feature, we use [weasyprint](https://pypi.org/project/WeasyPrint/). As stated by weasyprint <sup>[[1]](#weasyprintdocs)</sup>

>Besides a proper Python installation and a few Python packages, WeasyPrint needs the Pango, cairo and GDK-PixBuf libraries. They are required for the graphical stuff: Text and image rendering. These libraries aren’t Python packages. They are part of GTK+ (formerly known as GIMP Toolkit), and must be installed separately.

Therefore before you use and run this project you need to install the GTK3 runtime. [Click here to download the installation file](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases/download/2020-07-15/gtk3-runtime-3.24.20-2020-07-15-ts-win64.exe)<br>
After you finish the installation you need to add to PATH the GTK3 runtime. Depending on the GTK installation route you took, the proper folder name is something along the lines of:
- C:\msys2\mingw32\bin
- C:\msys2\mingw64\bin
- C:\Program Files\GTK3-Runtime Win64\bin

## Our Team
* **Front-end team**: Azka Atqia
* **Back-end team**: [Hariz Sufyan Munawar](https://github.com/harizMunawar)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---
<a name="weasyprintdocs">[1]</a>: Keep in my mind that this step is only for Windows OS. For more information about this step please read the [official weasyprint documentation](https://weasyprint.readthedocs.io/en/stable/install.html)