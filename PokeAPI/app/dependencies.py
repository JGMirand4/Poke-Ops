from sqlmodel import Session, create_engine

from .config import settings

connect_args = {'check_same_thread': False}
engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session
