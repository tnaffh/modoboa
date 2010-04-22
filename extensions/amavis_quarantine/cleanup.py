#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mailng.lib import db, parameters

if __name__ == "__main__":
    conn = db.getconnection("amavis_quarantine")
    max_messages_age = parameters.get("amavis_quarantine", "MAX_MESSAGES_AGE")

    print "Deleting messages older than %d days..." % max_messages_age
    db.execute(conn, """
DELETE FROM msgs WHERE time_num < UNIX_TIMESTAMP()-%d*24*3600;
""" % max_messages_age)

    print "Deleting unreferenced e-mail addresses..."
    db.execute(conn, """
DELETE FROM maddr
  WHERE NOT EXISTS (SELECT 1 FROM msgs WHERE sid=id)
  AND NOT EXISTS (SELECT 1 FROM msgrcpt WHERE rid=id);
""")

    print "Optimizing tables..."
    db.execute(conn, """
OPTIMIZE TABLE msgs, msgrcpt, quarantine, maddr;
""")

    db.close(conn)

    print "Done."