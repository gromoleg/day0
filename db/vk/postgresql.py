import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY
from os import getenv
import logging

logger = logging.getLogger('db')
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logging.getLogger('sqlalchemy.engine').handlers = logging.getLogger("db").handlers


class PostgreSQL_DB(object):
    def __init__(self, conn, meta):
        """

        :type conn: sqlalchemy.engine.base.Engine
        :type meta: sqlalchemy.sql.schema.MetaData
        """
        self.conn = conn
        self.meta = meta

    @staticmethod
    def connect(db, user, password=None, host='localhost', port=5432):
        """Returns a connection and a metadata object"""
        password = password or getenv('VK_POSTGRESQL_PASSWORD')
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
