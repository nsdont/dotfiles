#!/usr/local/bin/python3
import sys
import html
import sqlite3

from pync import Notifier
from os.path import expanduser
from datetime import datetime, timedelta

database_path = expanduser('~/Library/Containers/com.omnigroup.OmniFocus2/'
                           'Data/Library/Caches/com.omnigroup.OmniFocus2/'
                           'OmniFocusDatabase2')


def generate_md(data, tag):
    project_fmt = '* {}'
    item_fmt = '  * {}'
    plan_summer = ''
    base_fmt = """### OmniFocus
{tasks}
{plan_summer}
### Life\n"""
    tasks = []
    for project in data:
        tasks.append(project_fmt.format(project))
        tasks.extend([item_fmt.format(i) for i in data[project]])
    tasks = '\n'.join(tasks)

    if tag in {'Weekly', 'Monthly'}:
        plan_summer = """
### Weekly Plan

#### Finish Plan

#### Process Plan

#### Raw Plan
"""

    return base_fmt.format(tasks=tasks, plan_summer=plan_summer)


def export_to_dayone(md, now, tag):
    uuid = '{}_{}'.format(now.strftime('%Y%m%d%H%M%S%f'), tag)
    filename = '~/Dropbox/Apps/Day One/Journal.dayone/entries/{}.doentry'
    filename = filename.format(uuid)
    filename = expanduser(filename)

    base_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Creation Date</key><date>{date_iso}</date>
    <key>Entry Text</key><string>{md}</string>
    <key>Starred</key><false/>
    <key>Tags</key><array><string>{tag}</string></array>
    <key>UUID</key><string>{uuid}</string>
</dict>
</plist>"""  # noqa

    with open(filename, 'wb') as f:
        date_iso = (now - timedelta(hours=8)).strftime("%Y-%m-%dT%H:%M:%SZ")
        content = base_content.format(date_iso=date_iso, md=html.escape(md),
                                      tag=tag, uuid=uuid)
        f.write(content.encode())


def main(start_ts, end_ts, now, tag='Daily'):
    conn = sqlite3.connect(database_path)
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

    md = generate_md(data, tag)

    export_to_dayone(md, now, tag)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        try:
            now = datetime.strptime(sys.argv[1], '%Y.%m.%d')
        except ValueError:
            print('时间串格式错误，比如: 2015.11.17')
            sys.exit(1)
    else:
        now = datetime.now()
    base_timestamp = datetime(2001, 1, 1).timestamp()
    today = datetime(now.year, now.month, now.day)
    tomorrow = today + timedelta(1)

    if now.weekday() == 5:
        # 生成周报
        today_timestamp = (today - timedelta(6)).timestamp() - base_timestamp
        tomorrow_timestamp = tomorrow.timestamp() - base_timestamp
        main(today_timestamp, tomorrow_timestamp, now, 'Weekly')

    if (now + timedelta(1)).month > now.month:
        # 生成月报
        today_timestamp = (today - timedelta(30)).timestamp() - base_timestamp
        tomorrow_timestamp = tomorrow.timestamp() - base_timestamp
        main(today_timestamp, tomorrow_timestamp, now, 'Monthly')

    # 生成日报
    today_timestamp = today.timestamp() - base_timestamp
    tomorrow_timestamp = tomorrow.timestamp() - base_timestamp
    main(today_timestamp, tomorrow_timestamp, now, 'Daily')

    Notifier.notify('Export DayOne Done.', title='Omnifocus Statistics')
