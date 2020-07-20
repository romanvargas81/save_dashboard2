from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

DB = SQLAlchemy(metadata=MetaData(schema='ns_sync'))
