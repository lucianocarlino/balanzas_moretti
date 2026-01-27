from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Meta, engine, Base

class Scale(Base):
    __tablename__ = "scales"

    scale_id: Mapped[int]= mapped_column(Integer, primary_key=True)
    slave_address = Column(Integer, index=True, nullable=True, default=-1)
    name = Column(String, unique=True)
    online = Column(Boolean, default=False)
    mapped = Column(Boolean, default=False)
    active = Column(Boolean, default=True)

    packages = relationship('Package', secondary="scales_has_packages", back_populates='scales', lazy='joined')

    weights: Mapped[list['Weight']] = relationship("Weight", back_populates="scale")

    def __repr__(self):
        return f"Id: {self.scale_id} ; Adress: {self.slave_address} ; Packages: {self.packages}"
    
    def get_name(self):
        return f'{self.name}'

    def get_id(self):
        return f'{self.scale_id}'