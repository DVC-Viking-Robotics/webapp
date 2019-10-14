Here's a list of commands for using pipenv, which is mostly coming from [this website](https://pipenv.kennethreitz.org/en/latest/basics/):

## Installing pipenv
```bash
pip install --user pipenv
```

## Setup
Create a new virtual environment:
```bash
pipenv --python 3.6  # Any *installed* python version works
```

Removing said virtual environment:
```bash
pipenv --rm
```

You can install the dependencies if there is an existing `Pipfile`:
```bash
pipenv install  # you can also add the '--dev' flag to install the dev dependencies
```

If you want to ensure that the dependencies are installed exactly from `Pipfile.lock`, you can run the following:
```bash
pipenv sync
```

In the case that a `Pipfile` doesn't exist, you can create one after installing *at least* one package:
```bash
pipenv install <package>
```

You can also import a `requirements.txt` file to create your `Pipenv` file from there:
```bash
pipenv install -r path/to/requirements.txt
```

Generating a `Pipenv.lock` lock file is as follows:
```bash
pipenv lock # you can include pre-released with the '--pre' flag
```

## Installing/Uninstalling
You can install or uninstall any package with the following commands (similar to pip):
```bash
pipenv install <package>
pipenv uninstall <package>
```

You can also install specific or semi-specific versions with the following modification:
```bash
pipenv install "requests~=1.2"
pipenv install "requests>=1.4"
```
You can find more info about this [here](https://pipenv.kennethreitz.org/en/latest/basics/#specifying-versions-of-a-package).

If you need to nuke your virtual environment and start from scratch, you can run the following command. **NOTE: THIS IS A DESTRUCTIVE ACTION**
```bash
pipenv uninstall --all
```

## Checking dependencies
You can check your dependencies for security vulnerabilities:
```bash
pipenv check
```

You can also see a dependency tree of your project:
```bash
pipenv graph
```

## Running the project
Since we don't have easy access to the virtual environment folder, the procedure to running the project has changed slightly. There's two ways to do so:
1. Activate the virtual environment and then run the project normally:
```bash
pipenv shell
python -m webapp.app
```
2. Run a command directly in the virtual environment without explicitly activating the env itself:
```bash
pipenv run python -m webapp.app
```

Note: You can run any command in the virtual environment via `pipenv run [command]`