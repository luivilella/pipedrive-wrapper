# pipedrive-wrapper

## Hight level integration with [Pipedrive](https://www.pipedrive.com/).

Organization  (Search / Create / Detail)

    from pipedrive import PipeDrive

    pd = PipeDrive()

    pd.organization.search('xpto')

    pd.organization.detail(1)

    pd.organization.create({
        'name': 'organization name',
        'new field': 'this field will be auto created'
    })


## APIs


    # Search - The api search api order the results based in request IP address.
    $ curl http://localhost/api/organizations?search=br%20luis%2001
    {"success": true, "data": [{"id": 65, ...}]}

    # Detail
    $ curl http://localhost/api/organizations/70
    {
        "success": true,
        "data": {
            "data": {"id": 70 ...},
            "fields": [{"key": "id", "name": "ID: "}]
        }
    }

    # Create
    curl --header "Content-Type: application/json" \
        --request POST \
        --data '{"data": {"name": "My Fake Company", "new field": "xyz"}}' \
        http://localhost/api/organizations
    {
        "success": true,
        "data": {
            "id": 98,  "name": "My Fake Company", ... 
        }
    }

## Pages

Search
![image](https://user-images.githubusercontent.com/921729/41329318-5a1d5348-6ea3-11e8-967d-16ce294c9fc2.png)

Detail
![image](https://user-images.githubusercontent.com/921729/41329336-8223cca0-6ea3-11e8-91ff-fa0b73576d5c.png)

Create
![image](https://user-images.githubusercontent.com/921729/41329412-e4b57a4e-6ea3-11e8-8e5f-98128d67a16a.png)
![image](https://user-images.githubusercontent.com/921729/41329420-fd1858fe-6ea3-11e8-8ed5-c7b1ce3e0e2f.png)

## Instalation

To integrate with PipeDrive the backend app needs the token configuration, you just need to update `app/.env` with the backend key

### Docker

Make sure that you have [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/) installed in you env.

Checking docker version:

    $ docker --version
    Docker version 18.03.1-ce, build 9ee9f40
    
    $ docker-compose --version
    docker-compose version 1.21.1, build 5a3f1a3

Once you have docker installed run the commands bellow:

    $ make build && make up

Now the app should be running in your http://localhost

### Manual instalation

#### Backend 

The backend is a simple python env you just need to install the requirements and run the web api:

    $ cd app
    $ cp .env.template .env
    # Add your PipeDrive api token
    $ vi .env
    $ pip install -r requirements.txt
    $ python wsgi.py
    Bottle v0.12.13 server starting up (using WSGIRefServer())...
    Listening on http://0.0.0.0:8080/
    Hit Ctrl-C to quit.

Now the rest api should be running at http://localhost:8080/

#### Frontend

Make sure that you have [yarn](https://yarnpkg.com/lang/en/docs/install/) installed, and run the commands bellow.

    $ yarn install
    $ yarn run build
    $ yarn run start:dev

The frontend app should be running at http://localhost:8081/dist/build/search/
