# Bob the Builder

Can we build it? Yes we can! Bob is a framework for automating builds for payloads in a "scriptably" configurable way.

## Dependencies

To ensure use of python virtual environments on Ubuntu, run the following command to install the necessary packages.
```bash
sudo apt-get install python3-venv
```

## Installation

```bash
git clone git@github.com:coffeegist/bob-the-builder.git
cd bob-the-builder
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

## Setup  

Copy and edit the `bob-config.json` file to include a personal access token and organization url to the Azure DevOps account of your choosing.

```bash
cp bob/bob-config.json.sample bob/bob-config.json
```

## Running

For this project to function, you need to have access to an Azure DevOps account that has pre-existing pipelines configured to build payloads.

### Creating a token

Login to https://dev.azure.com/YOUR_USERNAME/_usersSettings/tokens
- Click **+ New Token**
  - Name: “Bob”
  - Organization: "\<YOUR_ORG_HERE\>"
  - Scope: Full Access
  - Click **Create**

### Configuring a build

Once you have access, run the following command to configure a blueprint:

```bash
cd bob
python bob.py configure -f my-build.json
```

### Queueing a build

Using the previously configured blueprint, `my-build.json`:

```bash
python bob.py run -f my-build.json -o ./build-artifacts
```

## When you're finished...

This project obviously uses virtual environments (venv). When you're done with Bob, just deactivate your virtual environment by issuing the following command:

```bash
deactivate
```

## That's it!!

Please post any issues you come across!
