from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
import config

Base = declarative_base()

def get_utc_now():
    return datetime.datetime.now(datetime.timezone.utc)

class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    acquired_at = Column(DateTime, default=get_utc_now)
    active = Column(Boolean, default=True)

class Target(Base):
    __tablename__ = 'targets'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)

class Prospect(Base):
    __tablename__ = 'prospects'
    id = Column(Integer, primary_key=True)
    platform = Column(String, nullable=False)
    external_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    price = Column(String)
    url = Column(String)
    evaluated = Column(Boolean, default=False)
    worth_trading = Column(Boolean, default=False)
    evaluation_reason = Column(Text)
    contacted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=get_utc_now)

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    prospect_id = Column(Integer, ForeignKey('prospects.id'))
    direction = Column(String) # 'outbound' or 'inbound'
    content = Column(Text)
    sent_at = Column(DateTime, default=get_utc_now)
    is_dry_run = Column(Boolean, default=True)

engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

    # Initialize state if empty
    session = SessionLocal()

    # Add initial inventory if not exists
    if not session.query(Inventory).first():
        watch = Inventory(name="Garmin 7 Watch", description="Garmin Fenix 7 smartwatch, good condition.")
        session.add(watch)

    # Add target if not exists
    if not session.query(Target).first():
        porsche = Target(name="2008 Porsche Cayman 3.4 987 S 2dr", description="End goal of the trading sequence.")
        session.add(porsche)

    session.commit()
    session.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
