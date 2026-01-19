from app.db.base import Base, Meta, engine
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Boolean, Column, Float, Integer, String

class Package(Base):
    __tablename__ = "packages"

    package_id: Mapped[int]= mapped_column(Integer, primary_key=True)
    expected_weight = Column(Float)
    minimum_weight = Column(Float)
    maximum_weight = Column(Float)
    name = Column(String, unique=True)
    active = Column(Boolean, default=True)

    scales = relationship('Scale', secondary="scales_has_packages", back_populates='packages')

    weights: Mapped[list['Weight']] = relationship('Weight', back_populates='package')

    def __repr__(self):
        return f'Package id: {self.package_id} ; Objective weight: {self.expected_weight} ; Minimum weight: {self.minimum_weight} ; Maximum weight: {self.maximum_weight} ; Name: {self.name}'
    
    def get_name(self):
        return f'{self.name}'