import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    email: Mapped[str] = mapped_column(String)
    phone_number: Mapped[str] = mapped_column(String)


class SettlementsTypes(db.Model):
    __tablename__ = 'settlements_types'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)


class Countries(db.Model):
    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)


class Settlements(db.Model):
    __tablename__ = 'settlements'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    country_id: Mapped[int] = mapped_column(ForeignKey('countries.id'), nullable=False, index=True)
    settlement_type_id: Mapped[int] = mapped_column(ForeignKey('settlements_types.id'), nullable=False)


class StreetsTypes(db.Model):
    __tablename__ = 'streets_types'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)


class Streets(db.Model):
    __tablename__ = 'streets'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    settlement_id: Mapped[int] = mapped_column(ForeignKey('settlements.id'), nullable=False, index=True)
    street_type_id: Mapped[int] = mapped_column(ForeignKey('streets_types.id'), nullable=False)


class Addresses(db.Model):
    __tablename__ = 'addresses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    house_number: Mapped[int] = mapped_column(Integer, nullable=False)
    department_number: Mapped[int] = mapped_column(Integer)

    street_id: Mapped[int] = mapped_column(ForeignKey('streets.id'), nullable=False)


class HousingsTypes(db.Model):
    __tablename__ = 'housings_types'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)


class Housings(db.Model):
    __tablename__ = 'housings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    housing_type_id: Mapped[int] = mapped_column(ForeignKey('housings_types.id'), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False, index=True)
    renter_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    address_id: Mapped[int] = mapped_column(ForeignKey('addresses.id'))


class Comforts(db.Model):
    __tablename__ = 'comforts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)


class ComfortsAssociationTable(db.Model):
    __tablename__ = 'comforts_association_table'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    comfort_id: Mapped[int] = mapped_column(ForeignKey('comforts.id'), nullable=False)
    housing_id: Mapped[int] = mapped_column(ForeignKey('housings.id'), nullable=False)


class Records(db.Model):
    __tablename__ = 'records'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    housing_id: Mapped[int] = mapped_column(ForeignKey('housings.id'))


class History(db.Model):
    __tablename__ = 'history'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    renter_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    housing_id: Mapped[int] = mapped_column(ForeignKey('housings.id'), index=True)

    rent_start: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    rent_end: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

    price: Mapped[int] = mapped_column(Integer, nullable=False)
