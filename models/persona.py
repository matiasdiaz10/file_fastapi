from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, BLOB
from conf.db import meta, engine

persona = Table("persona", meta,
            Column("id", Integer, primary_key=True),
            Column("nombre", String(255)),
            Column("apellido", String(255)),
            Column("dni", String(255)),
            Column("direccion", String(255)),
            Column("dirImg", String(255))
            )

meta.create_all(engine)