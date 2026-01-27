from app.db.base import Base, engine
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, ForeignKey, Integer, Float, DateTime

class Weight(Base):
    __tablename__ = "weights"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime)
    initial_weight = Column(Float)
    final_weight = Column(Float)

    scale_id: Mapped[int] = mapped_column(Integer, ForeignKey('scales.scale_id'))
    scale: Mapped["Scale"] = relationship("Scale", back_populates='weights')
    package_id: Mapped[int] = mapped_column(Integer, ForeignKey('packages.package_id'))
    package: Mapped["Package"] = relationship("Package", back_populates='weights')

    def to_dict(self):
        return {
            "id": self.id,
            "date_time": self.date_time.isoformat(timespec='seconds'),
            "initial_weight": self.initial_weight,
            "final_weight": self.final_weight,
            "scale": self.scale.get_name(),
            "scale_id": self.scale.get_id(),
            "package": self.package.get_name(),
            "package_id": self.package.get_id()
        }
 
# Base.metadata.create_all(engine)