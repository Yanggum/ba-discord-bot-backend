from dotenv import load_dotenv
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData
from sqlacodegen.codegen import CodeGenerator
from os import environ

load_dotenv()

url = environ['DB_CONN_URL']
engine = create_engine(url)
metadata = MetaData(engine)
metadata.reflect(engine)


with open('../apps/chat/models.py', 'w', encoding='utf-8') as outfile:
    generator = CodeGenerator(metadata)
    generator.render(outfile)