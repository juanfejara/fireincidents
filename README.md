This assestment if to ingest Fire incidents from San Francisco, downloaded
from the page data.sfgov.org, in particular the dataset wr8u-xric, and ingested
into a SQLite database (could be swiched to any other one in easy way).

The develop environment was Debian, with an environment manage pyenv and poetry.
The application run inside a docker, and output the SQLite database in the
data directory under the name fire_incidents.db.

The information about the data schema is in the attached file
FIR-0001_DataDictionary_fire-incidents.xlsx.

The LIMIT variable inside the scrap script is the limit records possible get
as free connection.

To build the container run:

```sh
docker build -t fire_incidents .
```

After build the container, run with:

```sh
docker run -v ./data:/usr/src/app/data fire_incidents 
```


And after running you can see the message:

Data saved to SQL database.
