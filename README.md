# Bob the Builder

Can we build it? Yes we can! Bob is a framework for automating builds for payloads in a "scriptably" configurable way. Read more at [https://coffeegist.com/security/automation-through-azure-with-bob/](https://coffeegist.com/security/automation-through-azure-with-bob/).

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
cd bob
cp bob-config.json.sample bob-config.json
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

### Configuring a blueprint

Once you have access, run the following command to configure a blueprint:

```bash
python bob.py configure -f my-blueprint.json
```

### Queueing a blueprint

Feel free to modify your blueprint manually, especially if you are building a pipeline that has queue-time variables. Then, using your newly configured blueprint, `my-blueprint.json`:

```bash
python bob.py run -f my-blueprint.json -o ./build-artifacts
```

## When you're finished...

This project obviously uses virtual environments (venv). When you're done with Bob, just deactivate your virtual environment by issuing the following command:

```bash
deactivate
```

## That's it!!

Please post any issues you come across!
