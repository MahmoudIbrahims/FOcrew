### How to apply alembic migration data:


#### Create database FOcrew_DB by DBeaver app and apply this in terminal:

```bash
cd src
```

```bash
cd Models/schema
```


### copy the alembic.ini file  or Initiolization alembic::

```bash
 cp alembic.ini.example alembic.ini
 ```

```bash
alembic init alembic
```

#### Update the file alembic and put username database and passwordfor example:

```bash
postgresql://postgres:password@localhost:5432/databasename 

```

#### Update file env.py :

```bash
target_metadata=SQLAlchemyBase.metadata
```

#### Apply all schemes for database or create a new migration :
```bash
alembic revision --autogenerate -m "initial commit"
```

#### Upgrade the database :
```bash
alembic upgrade head
```
# ------------------------------------------

