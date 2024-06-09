from orm_base import Base
from sqlalchemy import Column, Integer, String, Identity
from sqlalchemy.orm import Mapped, mapped_column

db_connection = " mongodb+srv://cluster22803.xx9rtqy.mongodb.net"

class Department(Base):
    __tablename__ = "departments"  # give name of the table for SQLAlchemy

    departmentId: Mapped[int] = mapped_column('department_id', Integer, Identity(start=1, cycle=True), nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column('name', String(50), nullable=False)
    abbreviation: Mapped[str] = mapped_column('abbreviation', String(6), nullable=False)
    chair_name: Mapped[str] = mapped_column('chair_name', String(80), nullable=False)
    building: Mapped[str] = mapped_column('building', String(10), nullable=False)
    office: Mapped[int] = mapped_column('office', Integer, nullable=False)
    description: Mapped[str] = mapped_column('description', String(80), nullable=False)

    def __init__(self, name: str, abbreviation: str, chair_name: str, building: str, office: int, description: str):
        self.name = name
        self.abbreviation = abbreviation
        self.chair_name = chair_name
        self.building = building
        self.office = office
        self.description = description

    def __str__(self):
        return (f"Department id: {self.departmentId} \n"
                f"name: {self.name}\n"
                f"Abbreviation: {self.abbreviation} \n"
                f"Chair: {self.chair_name}\n"
                f"Building: {self.building}\n"
                f"Office: {self.office}\n"
                f"Description: {self.description}")
