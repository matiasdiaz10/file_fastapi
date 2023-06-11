from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://root:@localhost:3307/image")
meta = MetaData()
con = engine.connect()