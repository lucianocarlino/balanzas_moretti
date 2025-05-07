from sqlalchemy import Column, ForeignKey, Integer, Table
from app.db.base import Base

class ScaleHasPackages(Base):
    __tablename__ = "scales_has_packages"

    id = Column(Integer, primary_key=True)
    scale_id = Column('scale_id', Integer, ForeignKey('scales.scale_id'))
    package_id = Column('package_id', Integer, ForeignKey('packages.package_id'))