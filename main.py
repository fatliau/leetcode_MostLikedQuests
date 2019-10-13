import requests
from requests.exceptions import HTTPError
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def get_all_slugs():
    url = "https://leetcode.com/api/problems/all/"
    slugs = []
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        r_json = response.json()
        for slug in r_json["stat_status_pairs"]:
            slugs.append(slug["stat"]["question__title_slug"])
    return slugs

def get_quest_info(slug):
    query = """
    query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    envInfo\n    libraryUrl\n    __typename\n  }\n}\n
    """
    body = {"operationName":"questionData",
            "variables":{"titleSlug":slug},
            "query":query}

    url = "https://leetcode.com/graphql"
    try:
        response = requests.post(url, json=body)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        r_json = response.json()
        return r_json["data"]["question"]

def createRawTable(dbName='leetcode.db'):
    createTableSQL = "CREATE TABLE questions( " \
                     "questionId INT, questionFrontendId INT, title TEXT, titleSlug TEXT, content TEXT, " \
                     "isPaidOnly INT, difficulty TEXT, likes INT, dislikes INT);"
    db_connect = create_engine('sqlite:///{}'.format(dbName))
    conn = db_connect.connect()
    try:
        conn.execute(createTableSQL)
        print("created table: {}".format(dbName))
    except SQLAlchemyError as e:
        print("SQL error: {}".format(e))
        raise SQLAlchemyError

def insertQuestInfo(quest_json, dbName='leetcode.db'):
    questionId = quest_json.get('questionId', -1)
    questionFrontendId = quest_json.get('questionFrontendId', -1)
    title = quest_json.get('title', "").replace("'", " ").replace('"', " ").replace(";", " ")
    titleSlug = quest_json.get('titleSlug', "").replace("'", " ").replace('"', " ").replace(";", " ")
    # content = quest_json.get('content', "") # TODO: store question content
    content = ""
    isPaidOnly = quest_json.get('isPaidOnly', -1)
    difficulty = quest_json.get('difficulty', "").replace("'", " ").replace('"', " ").replace(";", " ")
    likes = quest_json.get('likes', -1)
    dislikes = quest_json.get('dislikes', -1)
    # print(questionId, questionFrontendId, title, titleSlug, content, isPaidOnly, difficulty, likes, dislikes)

    insertSQL = "INSERT INTO questions (questionId, questionFrontendId, title, titleSlug, content, isPaidOnly, difficulty, likes, dislikes) " \
                "VALUES ( {}, {}, '{}', '{}', '{}', {}, '{}', {}, {});".format(questionId, questionFrontendId, title, titleSlug, content, isPaidOnly, difficulty, likes, dislikes)

    db_connect = create_engine('sqlite:///{}'.format(dbName))
    conn = db_connect.connect()
    try:
        conn.execute(insertSQL)
    except SQLAlchemyError as e:
        print("SQL error: {}".format(e))
        raise SQLAlchemyError

def insert_all_quest():
    slugs = get_all_slugs()
    inserted = 0
    for slug in slugs:
        quest_json = get_quest_info(slug)
        if quest_json:
            insertQuestInfo(quest_json)
        else:
            print("json invalid in {}".format(slug))
        inserted += 1
        print("inserted {}/{}".format(inserted, len(slugs)))


if __name__ == "__main__":
    createRawTable()
    insert_all_quest()
