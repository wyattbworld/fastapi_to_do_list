
PLATFORM: Windows 11 using git bash
Create the virutual environment using Python 3.13.9
> python -m venv venv
> cd ./venv

Activate the virtual environment
> source ./vev/Scripts/activate

Download required modules.
> python -m pip install pydantic
> python -m pip install fastapi
> python -m pip install uvicorn
> python -m pip install httpx
> python -m pip install pytest

Setup the git
> git init
> git add . --force
> git commit -m "first commit"
> git branch -M main
> git remote add origin https://github.com/wyattbworld/fastapi_to_do_list.git
> git push -u origin main