from db import get_conn, release_conn
from psycopg2.extras import RealDictCursor
def get_all_collection():
    conn = get_conn()
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            "SELECT * FROM collection"
        )
        return cur.fetchall()
    finally:
        cur.close()
        release_conn(conn)

def get_all_collection_item_by_id(collection_id, user_id):
    conn = get_conn()
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""SELECT ci.id          AS collection_item_id,
                              ci.collection_id,
                              ci.content_id,
                              ci.display_order,

                              c.type         AS content_type,
                              c.created_at   AS content_created_at,

                              s.simplified   AS sentence_simplified,
                              s.traditional  AS sentence_traditional,
                              s.pinyin       AS sentence_pinyin,
                              s.difficulty,

                              cw.simplified  AS word_simplified,
                              cw.traditional AS word_traditional,
                              cw.pinyin      AS word_pinyin,
                              cw.hsk_level,

                              cc.simplified  AS character_simplified,
                              cc.traditional AS character_traditional,
                              cc.pinyin      AS character_pinyin,
                              cc.hsk_level   AS character_hsk_level,

                              ucip.mastery_score,
                              ucip.total_reviews,
                              ucip.correct_reviews,
                              ucip.failed_reviews,
                              ucip.current_streak,
                              ucip.best_streak,
                              ucip.avg_response_ms,
                              ucip.hint_count,
                              ucip.first_reviewed_at,
                              ucip.last_reviewed_at,
                              ucip.next_review_at

                       FROM collection_item ci
                                JOIN content c
                                     ON c.id = ci.content_id

                                LEFT JOIN sentence s
                                          ON s.content_id = c.id

                                LEFT JOIN chinese_word cw
                                          ON cw.content_id = c.id

                                LEFT JOIN chinese_character cc
                                          ON cc.content_id = c.id

                                LEFT JOIN user_collection_item_progress ucip
                                          ON ucip.collection_item_id = ci.id
                                              AND ucip.user_id = %s

                       WHERE ci.collection_id = %s

                       ORDER BY ci.display_order;""", (user_id, collection_id))
        return cur.fetchall()
    finally:
        cur.close()
        release_conn(conn)