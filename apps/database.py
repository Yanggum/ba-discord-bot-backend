# database.py

from databases import Database
from os import environ
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData

# .env 환경파일 로드
load_dotenv()

# 디비 접속 URL
DB_CONN_URL = '{}://{}:{}@{}:{}/{}'.format(
    environ['DB_TYPE'],
    environ['DB_USER'],
    environ['DB_PASSWD'],
    environ['DB_HOST'],
    environ['DB_PORT'],
    environ['DB_NAME'],
)

# 쿼리를 위한 db 커넥션(비동기) 부분
db_instance = Database(
    DB_CONN_URL,
    min_size=5,			# 기본 connection 수
    max_size=1000,		# 최대 connection 수
    pool_recycle=500	# mysql 에 설정된 wait_timeout 시간 동안 재요청이 없을 경우 MySQL에서 해당 세션의 연결을 끊어버린다 (https://yongho1037.tistory.com/569)
    )

# 모델 초기화를 위한 db 커넥션 부분
db_engine = create_engine(DB_CONN_URL)
db_metadata = MetaData()