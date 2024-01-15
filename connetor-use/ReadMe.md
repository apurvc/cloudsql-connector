###
Repo to test GCP sql language connector based on https://github.com/GoogleCloudPlatform/cloud-sql-python-connector/blob/main/samples/notebooks/postgres_python_connector.ipynb

***
1. Create A private mysql/postgres sql with private ip only, i.e. remove public ip. The idea is to test language connector allowing private encrypted connection using IAM authentication only.

2. once db is ready Create an IAM user using a service account, this account will be used in code, as this user doesn't have permissions on database it needs to be granted permissions.


3. Create a vm in the same network and region as sql database to allow connecting to sql server over private ip. In API scope enable cloudsql.
4. SSH to vm and execute follwing commands 

```
sudo apt update && sudo apt-get install -y python3-venv
python3 -m venv df-env
source df-env/bin/activate
python3 -m pip install -q --upgrade pip setuptools wheel
``` 

*Clone this repository and from the connector-use folder run *
``` 
python3 -m pip install -r requirements.txt
and then 
python3 pstgressyscall.py will print current database time as no DDL/DML is being executed. 
python3 pstgrssandwiches.py will fail as to execute DDL/DML permissions are required to be provided to the user.
``` 


***
Option used to grant permission -Cloud SQl proxy , Follow https://cloud.google.com/sql/docs/postgres/connect-auth-proxy#linux-64-bit
Ref: https://cloud.google.com/sql/docs/postgres/add-manage-iam-users#grant-db-privileges

once cloud proxy is setup run psql or mysql as needed and provide permissions. 

Postgres
``` 
GRANT cloudsqlsuperuser TO 213447898-compute@developer; # the IAM user created in previous section visible in users.
```
*Mysql
``` 
GRANT ALL PRIVILEGES ON *.* TO '213447898-compute'@'%';
```

Once grant is given run the script again 

``` 
python3 pstgrssandwiches.py

``` 

This time it will print the database inserted values

> (df-env) apurv_chandra@instance-1:~/dataflow$ python pstgrstest.py                                                                                                                                                                               
(1, 'HOTDOG', 'Germany', 7.5)
(2, 'BÀNH MÌ', 'Vietnam', 9.1)
(3, 'CROQUE MADAME', 'France', 8.3)
(4, 'HOTDOG1', 'Germany', 7.5)
(5, 'BÀNH MÌ1', 'Vietnam', 9.1)
(6, 'CROQUE MADAME1', 'France', 8.3)


