Welcome to Fortinet Health Check project. 

If you would like to test it, there are two ways:


1. Using docker compose. 
2. Natively

*We recommend docer...*

**Anyhow**

## 1. Using Docker compose

Install docker: https://docs.docker.com/engine/install/

Then install docker compose: https://docs.docker.com/compose/install/

Next, create a `.env` file on thre root folder with the following content:
```env
POSTGRES_DB=fortiget_healthcheck
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
SECRET_KEY=hp2W6i6%jMD3h^j^*oKu
```

replace POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD and SECRET_KEY with what you are comfortable with. 

Or, you know, leave them like that, it will still work. 

Now run the project:

```shell
docker-compose up -d 
```

Your project is up. 
Now, let's move to the native side of things.

## 2. Running Natively
Let's get started with setting up the project. 

If you are running this project natively, you will need to have postgresql installed. 
If it is not yet installed (how???), follow the following tutorial on how to install it on Linux:

https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-20-04-quickstart

If on Windows, download it from here:
https://www.enterprisedb.com/postgresql-tutorial-resources-training?uuid=7c756686-90b4-4909-89ed-043e0705a76e&campaignId=7012J000001BfmaQAC

As usual click next -> next -> ...repeat until it is finally installed. One thing to note, do not forget the username and password it prompts you for, these will come in really handy the next step. 

Now that we have the Windows and Linux world both on the same wavelength, let us set up our environment vairables. 

In your root directory, create a file called .env, it will look something like:

```env
POSTGRES_DB={{ DB_NAME }}
POSTGRES_USER={{ DB_USER }}
POSTGRES_PASSWORD={{ DB_PASSWORD }}
POSTGRES_HOST={{ DB_HOSE }} 
SECRET_KEY={{ RANDOM_STRING }}
```
So, remember the username and password we kept while installing postgrresql, replace {{ DB_USER }} and {{ DB_PASSWORD }} with the two.

replace everything inside {{  }} with the relevant vairable. 

Now create the database:

```sql
CREATE DATABASE {{ DB_NAME }}
```

`{{ DB_NAME }}` is the name of the database you would like to have. 

Now, set the FLASK_APP environment variable as run.py. If on Linux run;
```shell
export FLASK_APP=run.py
```

and on windows:
```shell
set FLASK_APP=run.py
```

Once that is done, run the following command to make sure the dependedncies are installed:
```shell
pip install -r requirements.txt
```

Run the migrations:
```shell
flask db upgrade
```

Then run the app, either:
`flask run`

or 

`python run.py`


Your project will be live. 