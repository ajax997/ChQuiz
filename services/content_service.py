# from db import get_conn, release_conn
# from psycopg2.extras import RealDictCursor
#
#
# def get_all_example_by_content(content):
#     conn = get_conn()
#     try:
#         cur = conn.cursor(cursor_factory=RealDictCursor)
#
#         cur.execute("""SELECT DISTINCT ON (s.simplified) s.content_id,
#                                                          s.simplified,
#                                                          s.traditional,
#                                                          s.pinyin,
#                                                          t.language_code,
#                                                          t.translation
#                        FROM sentence s
#                                 JOIN translation t
#                                      ON t.content_id = s.content_id
#                                          AND t.language_code = 'vi'
#                        WHERE s.segments ~ %s
#                        ORDER BY s.simplified, s.content_id;""", (content,))
#
#         return cur.fetchall()
#
#     finally:
#         cur.close()
#         release_conn(conn)


import pandas as pd


CSV_FILE = "newsentence.csv"


class SentenceService:
    def __init__(self, csv_file):
        self.df = self._load_csv(csv_file)

    def _load_csv(self, csv_file):
        try:
            return pd.read_csv(
                csv_file,
                encoding="utf-8-sig"
            )
        except UnicodeDecodeError:
            return pd.read_csv(
                csv_file,
                encoding="gb18030"
            )

    def get_all_example_by_content(self, content):
        """
        Find sentences containing `content`.

        Returns:
            list[dict]
        """

        if not content:
            return []

        # Search Simplified Chinese.
        # regex=False means content is treated literally.
        results = self.df[
            self.df["Simplified"].str.contains(
                content,
                regex=False,
                na=False
            )
        ].copy()

        # Remove duplicate Simplified sentences
        results = results.drop_duplicates(
            subset=["Simplified"]
        )

        # Return the same structure that the old DB query returned
        results["language_code"] = "vi"

        return results[
            [
                "Simplified",
                "Traditional",
                "Pinyin",
                "language_code",
                "Translation",
            ]
        ].to_dict("records")


# --------------------------------------------------
# Load CSV ONCE
# --------------------------------------------------

sentence_service = SentenceService(CSV_FILE)


# --------------------------------------------------
# Public function
# --------------------------------------------------

def get_all_example_by_content(content):
    return sentence_service.get_all_example_by_content(content)