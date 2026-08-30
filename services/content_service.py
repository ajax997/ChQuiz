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
import jieba


class SentenceService:

    def __init__(self, csv_file):
        self.sentences = []
        self.index = {}

        self._load(csv_file)

    def _load(self, csv_file):

        try:
            df = pd.read_csv(
                csv_file,
                encoding="utf-8"
            )
        except UnicodeDecodeError:
            df = pd.read_csv(
                csv_file,
                encoding="gb18030"
            )

        for _, row in df.iterrows():

            sentence = {
                "Simplified": str(row["Simplified"]),
                "Traditional": str(row["Traditional"]),
                "Pinyin": str(row["Pinyin"]),
                "language_code": "vi",
                "Translation": str(row["Translation"]),
            }

            self.sentences.append(sentence)

            # Build inverted index
            words = set(jieba.cut(sentence["Simplified"]))

            for word in words:

                if not word.strip():
                    continue

                if word not in self.index:
                    self.index[word] = []

                self.index[word].append(sentence)

        print(
            f"Loaded {len(self.sentences)} sentences"
        )
        print(
            f"Index contains {len(self.index)} words"
        )

    def get_all_example_by_content(self, content):

        if not content:
            return []

        # Fast path: exact jieba word
        results = self.index.get(content, [])

        # Preserve your old DISTINCT behavior
        seen = set()
        output = []

        for sentence in results:

            simplified = sentence["Simplified"]

            if simplified in seen:
                continue

            seen.add(simplified)
            output.append(sentence)

        return output


sentence_service = SentenceService(
    "newsentence.csv"
)


def get_all_example_by_content(content):
    return sentence_service.get_all_example_by_content(content)