from sqlalchemy import create_engine, orm

DATABASE_URL = "postgresql://postgres:123@localhost:5432/library_api"

engine = create_engine(DATABASE_URL)
Session = orm.sessionmaker(bind=engine)
Base = orm.declarative_base()
