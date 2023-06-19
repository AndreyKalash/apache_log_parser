from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ApacheLog(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    ip_address = Column(String(15), nullable=True)
    remote_logname = Column(String(255), nullable=True)
    remote_user = Column(String(255), nullable=True)
    request_dtime = Column(DateTime, nullable=True)
    request_method = Column(String(10), nullable=True)
    requested_url = Column(String(255), nullable=True)
    status_code = Column(Integer, nullable=True)
    response_size = Column(BigInteger, nullable=True)
