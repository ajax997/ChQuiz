from db import get_conn, release_conn
from psycopg2.extras import RealDictCursor


def get_all_example_by_content(content):
    conn = get_conn()
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
                    SELECT s.content_id,
                           s.simplified,
                           s.traditional,
                           s.pinyin,
                           t.language_code,
                           t.translation
                    FROM sentence s
                             JOIN translation t
                                  ON t.content_id = s.content_id and t.language_code = 'vi'
                    WHERE s.segments ~ %s
                    ORDER BY s.simplified, t.language_code;
                    """, (content,))

        return cur.fetchall()

    finally:
        cur.close()
        release_conn(conn)