import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY
from helpers.pclass import Database
from os import getenv
import logging

logger = logging.getLogger('db')
sa_logger = logging.getLogger('sqlalchemy')
sa_logger.setLevel(logging.INFO)
sa_logger.handlers = logging.getLogger("db").handlers
sa_logger.propagate = 0


class PostgreSQL_DB(Database):
    def __init__(self, conn, meta):
        """

        :type conn: sqlalchemy.engine.base.Engine
        :type meta: sqlalchemy.sql.schema.MetaData
        """
        self.conn = conn
        self.meta = meta

    @staticmethod
    def connect(db=None, user=None, password=None, host='localhost', port=5432):
        """Returns a connection and a metadata object"""
        db = db or getenv('VK_POSTGRESQL_DB')
        user = user or getenv('VK_POSTGRESQL_USER')
        password = password or getenv('VK_POSTGRESQL_PASSWORD')

        assert db is not None, ValueError("db name is not defined")
        assert user is not None, ValueError("db user is not defined")
        assert password is not None, ValueError("db password is not defined")

        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(user, password, host, port, db)

        logger.info('vk.postgresql: connecting to %s db at %s:%s user: %s' % (db, host, port, user))
        conn = sa.create_engine(url, client_encoding='utf8')

        # Bind the connection to MetaData()
        meta = sa.MetaData(bind=conn, reflect=True)
        logger.info('vk.postgresql: connection successful')
        return PostgreSQL_DB(conn, meta)

    @property
    def tables(self):
        return self.meta.tables

    def create_tables(self):
        logger.info('vk.postgresql: creating group_members table')
        group_members = sa.Table('group_members', self.meta,
                                 sa.Column('timestamp', sa.DateTime,
                                           server_default=sa.func.now()),
                                 sa.Column('members', ARRAY(sa.Integer)))

        logger.info('vk.postgresql: writing new tables')
        self.meta.create_all(self.conn)
        logger.info('vk.postgresql: tables created')

    def insert_group_members(self, members):
        """

        :type members: list of int
        """
        query = self.tables['group_members'].insert().values(members=members)
        self.exec_query(query)

    def exec_query(self, query):
        self.conn.execute(query)
