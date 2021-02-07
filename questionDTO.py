from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

Base = declarative_base()

# CREATE TABLE questions( questionId INT, questionFrontendId INT, title TEXT, titleSlug TEXT, content TEXT,
#                         isPaidOnly INT, difficulty TEXT, likes INT, dislikes INT);

class Question(Base):
    __tablename__ = "questions"
    questionId = Column(Integer, primary_key=True)
    questionFrontendId = Column(Integer)
    title = Column(String)
    titleSlug = Column(String)
    content = Column(String)
    isPaidOnly = Column(Integer)
    difficulty = Column(String)
    likes = Column(Integer)
    dislikes = Column(Integer)

def query_all(dbName='leetcode.db'):
    db_engine = create_engine('sqlite:///{}'.format(dbName))
    Session = sessionmaker()
    Session.configure(bind=db_engine)
    session = Session()
    results = session.query(Question).all()

def createObjectFromJson(quest_json):
    questionId = quest_json.get('questionId', -1)
    questionObj = Question(questionId=questionId)

    questionObj.questionFrontendId = quest_json.get('questionFrontendId', -1)
    questionObj.title = quest_json.get('title', "").replace("'", " ").replace('"', " ").replace(";", " ")
    questionObj.titleSlug = quest_json.get('titleSlug', "").replace("'", " ").replace('"', " ").replace(";", " ")
    # content = quest_json.get('content', "") # TODO: store question content
    questionObj.isPaidOnly = 1 if quest_json.get('isPaidOnly', False) else 0
    questionObj.difficulty = quest_json.get('difficulty', "").replace("'", " ").replace('"', " ").replace(";", " ")
    questionObj.likes = quest_json.get('likes', -1)
    questionObj.dislikes = quest_json.get('dislikes', -1)
    return questionObj

def addQuestion(session, questionObj):
    question = (
        session.query(Question).filter(Question.questionId == questionObj.questionId).one_or_none()
    )
    # Does the Question already exist?
    if question is not None:
        print("id:{} exist".format(questionObj.questionId))
        return
    session.add(questionObj)
    session.commit()
