# Flask RESTFul Template
This is a simple REST API project with Python template.

The project has:

<table align="center">
<tr>
  <td><b>Library</b></td>
  <td><b>Documentation</b></td>
</tr>
<tr>
  <td>Flask-RESTFul</td>
  <td><a href="https://flask-restful.readthedocs.io/en/latest/">https://flask-restful.readthedocs.io/en/latest/</a></td>
</tr>
<tr>
  <td>Flask-JWT</td>
  <td><a href="https://pythonhosted.org/Flask-JWT/">https://pythonhosted.org/Flask-JWT/</a></td>
</tr>
<tr>
  <td>Flask-SQLAlchemy</td>
  <td><a href="https://flask-sqlalchemy.palletsprojects.com/en/2.x/">https://flask-sqlalchemy.palletsprojects.com/en/2.x/</a></td>
</tr>
<tr>
  <td>Flask-ApiSpec (Swagger UI/API)</td>
  <td><a href="https://flask-apispec.readthedocs.io/en/latest/">https://flask-apispec.readthedocs.io/en/latest/</a></td>
</tr>
</table>


So, next we will see more details.

* * *

## Getting Started

First, we need to prepare the setup and then just do:

- `make setup`
>> **Note:** In most cases, it is recommended to use the **virtual env**.
>
> If you are beginner, use **pyenv** or a simple command: **python3 -m venv venv**

* * *

## Makefiles

If you haven't experience with Makefiles, I recommend you read about this:

https://makefiletutorial.com/

Now if you know, even a little ... you can look at the file at the root of the repository and in the 
[makefiles](/makefiles) folder.

### Running Makefile

Makefile in my opinion was made to make life easier, BUT I need to agree that Bash Script is easier for me.
Sometimes I still get confused with GNU ... So I mean that for the simplest thing I use Makefiles and for more complex 
cases I prefer to use Bash... and if it's even more complex I use Python Script.

You can see all the routes, doing: 
```shell
$: make routes

Endpoint                       Methods                 Rule
-----------------------------  ----------------------  -----------------------
_default_auth_request_handler  POST                    /auth
group                          DELETE, GET, POST       /group/<name>
grouplist                      GET                     /groups
index                          GET                     /
people                         DELETE, GET, POST, PUT  /person/<name>
peoplelist                     GET                     /people
static                         GET                     /static/<path:filename>
userregister                   DELETE, POST, PUT       /register
userregister                   DELETE, POST, PUT       /register/<username>
```

To run in debug mode (developer), do:
```shell
$: make dev

 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 180-260-245
```


To run in production mode, do:
```shell
$: make run

[uWSGI] getting INI configuration from uwsgi.ini
*** Starting uWSGI 2.0.19.1 (64bit) on [Mon May  3 02:39:57 2021] ***
...
WSGI app 0 (mountpoint='') ready in 0 seconds on interpreter 0x7fa03f605c70 pid: 63322 (default app)
*** uWSGI is running in multiple interpreter mode ***
spawned uWSGI master process (pid: 63322)
spawned uWSGI worker 1 (pid: 63369, cores: 4)
spawned uWSGI worker 2 (pid: 63370, cores: 4)
spawned uWSGI worker 3 (pid: 63371, cores: 4)
spawned uWSGI worker 4 (pid: 63372, cores: 4)
spawned uWSGI worker 5 (pid: 63373, cores: 4)
spawned uWSGI worker 6 (pid: 63374, cores: 4)
spawned uWSGI worker 7 (pid: 63375, cores: 4)
spawned uWSGI worker 8 (pid: 63376, cores: 4)
spawned uWSGI worker 9 (pid: 63377, cores: 4)
spawned uWSGI worker 10 (pid: 63378, cores: 4)
```
> (*Why not **make prod**? I don't know*)
>
> However, If you really need to run in production mode, I strongly recommend that you use **docker**, like
      *Kubernetes* or *Docker Swarm*.
      
Now that you have chosen the mode (prod or dev), you need to build some important data.

There are two options:

- **Swagger UI**;
- Continue with the **Makefile** targets.

* * *

### Swagger UI

Just open your browser and access the endpoint `/`

![](/docs/swagger.png)

* * *

## Makefile targets

So let's go!

- create a user and associate with group, e.g:
```shell
$: make create-user name=wallace password=salles group_id=1
{
    "message": "User created successfully."
}
 ```

- create a group, e.g: 
```shell
$: make create-group name=admin

{
    "name": "admin",
    "users": [
        {
            "name": "wallace",
            "group_id": 1
        }
    ]
}
```

With the username, you can generate token, then do: 
```shell
$: make token jwt_user=wallace jwt_pass=salles

{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJI......U_TjASv45sp_M0oFdpqd2udGo"
}
```
>> Putting the password on the CLI doesn't seem very secure, right?
>> Instead, you can define an environment variable.
>>> export jwt_user=wallace
>>>
>>> export jwt_pass=salles
>
> **Note:** I decided to remove the `jwt_required` decorator to avoid complexity in this project, but it's easy to put
> in again. Therefore, it isn't necessary to generate a token for these tests.


Now you can play with creating, removing and updating people, e.g:
```shell
$: make create-person name=wsalles email=ops@wallacesalles.dev role=DevOps

{
    "name": "wsalles",
    "role": "DevOps",
    "email": "ops@wallacesalles.dev"
}
```

```shell
$: make update-person name=wsalles email=wallace_robinson@hotmail.com role=Pythonic

{
    "name": "wsalles",
    "role": "Pythonic",
    "email": "wallace_robinson@hotmail.com"
}
```

```shell
$: make delete-person name=wsalles

{
    "message": "Person deleted."
}
```
    

Ok, I know... easy-peasy, right?

* * *

### Credits end Motivations:
- https://blog.teclado.com/
- https://pythonacademy.com.br/blog/

* * *

So, let's rock! :rocket:

- Follow me on [LinkedIn](https://linkedin.com/in/wallacesalles)
- Visit my page: [https://wallacesalles.dev](https://wallacesalles.dev)