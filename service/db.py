from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    token = Column(String(100), nullable=False)
    
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    content = Column(String(500), nullable=False)
    author = Column(String(500), nullable=False)

def create_engine_and_session():
    engine = create_engine('mysql+mysqlconnector://test:test@localhost/site')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return engine, session

def login_user(username, password):
    userdata = session.query(User).filter_by(username=username, password=password).first()
    session.close()
    return userdata

def register_user(username, password, token):
    new_user = User(username=username, password=password, token=token)
    session.add(new_user)
    session.commit()
    return True

def create_post(id, content, author):
    new_user = Post(id=id, content=content, author=author)
    session.add(new_user)
    session.commit()
    return True

def get_post(username):
    postlist = session.query(Post).filter_by(author=username).all()
    session.close()
    return postlist

def del_post(post_id):
    post_to_delete = session.query(Post).filter(Post.id == post_id).first()
    if post_to_delete:
        session.delete(post_to_delete)
        session.commit()
        return True
    else:
        return False
    
engine, session = create_engine_and_session()