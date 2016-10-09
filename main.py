# -*- coding: utf-8 -*-
from api import vk
from db.vk import engines
from helpers.arguments import parser
from time import sleep
import logging
import logging.config

logging.config.fileConfig("logging.conf")
args = parser.parse_args()


def main():
    logging.info('connect to db')
    engine = engines[args.engine].connect()
    if args.migrate:
        logging.info('start migration')
        engine.create_tables()
        return
    group = vk.group(args.group)
    logging.info('main: retrieve group members')
    members = group.get_members().ids
    logging.info('main: got %s members' % len(members))
    logging.info('main: write members to db')
    engine.insert_group_members(members)


if __name__ == '__main__':
    main()
