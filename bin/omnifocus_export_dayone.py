#!/usr/local/bin/python3
"""OmniFocus export to Dayone.

Usage:
  omnifocus_export_dayone.py
  omnifocus_export_dayone.py <date> [--show]
  omnifocus_export_dayone.py (-s | --show)

Options:
  -h --help     Show this screen.
  --version     Show version.
  -s --show     Only echo to screen.

"""
import sys
import sqlite3
import uuid
import logging
import logging.handlers

from pync import Notifier
from docopt import docopt
from os.path import expanduser
from datetime import datetime, timedelta

omnifocus_db_path = expanduser('~/Library/Containers/com.omnigroup.OmniFocus2/'
                               'Data/Library/Caches/com.omnigroup.OmniFocus2/'
                               'OmniFocusDatabase2')

dayone2_db_path = expanduser('~/Library/Group Containers/5U8NS4GX82.dayoneapp2'
                             '/Data/Documents/DayOne.sqlite')

logger = logging.getLogger('omnifocus_export')

tags_enum = {
    'Daily': 1,
    'Monthly': 2,
    'Weekly': 3,
    'Yearly': 4
}


def setup_logging():
    LOG_FILE = '/tmp/omnifocus_export.log'
    fmt = '%(asctime)s - %(message)s'
    formatter = logging.Formatter(fmt)

    handler = logging.handlers.RotatingFileHandler(
        LOG_FILE, maxBytes=1024 * 1024, backupCount=5)
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

    logger.setLevel(logging.DEBUG)


def generate_md(data, tag):
    project_fmt = '* {}'
    item_fmt = '  * {}'
    plan_summer = ''
    base_fmt = '### OmniFocus\n{tasks}\n{plan_summer}\n### Life\n'
    tasks = []
    for project in data:
        tasks.append(project_fmt.format(project))
        tasks.extend([item_fmt.format(i) for i in data[project]])
    tasks = '\n'.join(tasks)

    if tag in {'Weekly', 'Monthly'}:
        plan_summer = '\n### {} Plan\n\n#### OKR Judge\n'
        plan_summer = plan_summer.format(tag)

    return base_fmt.format(tasks=tasks, plan_summer=plan_summer)


def export_to_dayone(md, now, tag):
    conn = sqlite3.connect(dayone2_db_path)
    cur = conn.cursor()

    start_at = datetime(2001, 1, 1)
    timestamp = (now - start_at).total_seconds()
    zuuid = str(uuid.uuid4().hex).upper()
    cuuid = str(uuid.uuid4()).upper()

    sql = """
        INSERT INTO ZENTRY (
            Z_ENT, Z_OPT, ZSTARRED, ZJOURNAL, ZCREATIONDATE, ZMODIFIEDDATE,
            ZCHANGEID, ZTEXT, ZUUID
        ) VALUES (
            2, 2, 0, 2, {}, {}, '{}', '{}', '{}');
    """
    cur.execute(sql.format(timestamp, timestamp, cuuid, md, zuuid))
    conn.commit()

    sql = """
        select Z_PK from ZENTRY where ZUUID = '{}' order by ZCREATIONDATE desc;
    """
    ids = [i for i in cur.execute(sql.format(zuuid))]

    sql = """
        INSERT INTO Z_2TAGS (
            Z_2ENTRIES, Z_20TAGS
        ) VALUES ('{}', '{}');
    """

    conn.execute(sql.format(ids[0][0], tags_enum[tag]))
    conn.commit()
    conn.close()


def do(start_ts, end_ts, now, tag='Daily', only_show=False):
    conn = sqlite3.connect(omnifocus_db_path)
    cur = conn.cursor()

    sql = """
    select t.name as 'task_name', p.name as 'project_name' from task as t
        left join task as p on p.projectInfo = t.containingProjectInfo
    where
        t.projectinfo is null and
        t.dateCompleted >= {} and
        t.dateCompleted < {} and
        t.containingProjectInfo in (
            select projectInfo from task where projectInfo is not NULL and
                name not like "%Ritual%" and name not like "%REVIEW%"
        );
    """

    data = {}

    for t, p in cur.execute(sql.format(start_ts, end_ts)):
        if p not in data:
            data[p] = list()
        data[p].append(t)

    sql = """
    select name from task
    where
        projectinfo is null and
        ininbox = 1 and
        dateCompleted >= {} and
        dateCompleted < {};
    """
    data['Inbox'] = []
    for t, in cur.execute(sql.format(start_ts, end_ts)):
        data['Inbox'].append(t)
    if not len(data['Inbox']):
        data.pop('Inbox')

    md = generate_md(data, tag)

    if only_show:
        print(md)
    else:
        export_to_dayone(md, now, tag)


def main(args):
    if args['<date>']:
        try:
            now = datetime.strptime(args['<date>'], '%Y.%m.%d')
        except ValueError:
            print('时间串格式错误，比如: 2015.11.17')
            sys.exit(1)
    else:
        now = datetime.utcnow()
    only_show = args['--show']
    base_timestamp = datetime(2001, 1, 1).timestamp()
    today = datetime(now.year, now.month, now.day)
    tomorrow = today + timedelta(1)

    if now.weekday() == 5:
        # 生成周报
        logger.info('Start generate weekly...')
        today_timestamp = (today - timedelta(6)).timestamp() - base_timestamp
        tomorrow_timestamp = tomorrow.timestamp() - base_timestamp
        do(today_timestamp, tomorrow_timestamp, now, 'Weekly',
            only_show=only_show)
        logger.info('Finish generate weekly...')

    tomorrow = now + timedelta(days=1)
    if tomorrow.month > now.month or (now.month == 12 and tomorrow.month == 1):
        # 生成月报
        logger.info('Start generate monthly...')
        today_timestamp = (today - timedelta(30)).timestamp() - base_timestamp
        tomorrow_timestamp = tomorrow.timestamp() - base_timestamp
        do(today_timestamp, tomorrow_timestamp, now, 'Monthly',
           only_show=only_show)
        logger.info('Finish generate monthly...')

    # 生成日报
    logger.info('Start generate daily...')
    today_timestamp = today.timestamp() - base_timestamp
    tomorrow_timestamp = tomorrow.timestamp() - base_timestamp
    do(today_timestamp, tomorrow_timestamp, now, 'Daily', only_show=only_show)
    logger.info('Finish generate daily...')

    if not only_show:
        Notifier.notify('Export DayOne Done.', title='Omnifocus Statistics')


if __name__ == '__main__':
    setup_logging()
    arguments = docopt(__doc__, version='0.1.1')

    logger.info('--------START------')
    main(arguments)
    logger.info('--------END--------')
