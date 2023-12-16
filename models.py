import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey, DateTime, Boolean, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(256), nullable=False)

    email: Mapped[str] = mapped_column(String(40), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=True)

    first_name: Mapped[str] = mapped_column(String(20), nullable=True)
    second_name: Mapped[str] = mapped_column(String(20), nullable=True)

    email_is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    user_is_verified: Mapped[bool] = mapped_column(Boolean, default=False)


class SettlementsTypes(db.Model):
    __tablename__ = 'settlements_types'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)


class Countries(db.Model):
    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)


class Settlements(db.Model):
    __tablename__ = 'settlements'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)

    country_id: Mapped[int] = mapped_column(ForeignKey('countries.id'), nullable=False, index=True)
    settlement_type_id: Mapped[int] = mapped_column(ForeignKey('settlements_types.id'), nullable=False)


class StreetsTypes(db.Model):
    __tablename__ = 'streets_types'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)


class Streets(db.Model):
    __tablename__ = 'streets'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)

    settlement_id: Mapped[int] = mapped_column(ForeignKey('settlements.id'), nullable=False, index=True)
    street_type_id: Mapped[int] = mapped_column(ForeignKey('streets_types.id'), nullable=False)


class Addresses(db.Model):
    __tablename__ = 'addresses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    house_number: Mapped[int] = mapped_column(Integer, nullable=False)
    department_number: Mapped[int] = mapped_column(String(5), nullable=True)

    street_id: Mapped[int] = mapped_column(ForeignKey('streets.id'), nullable=False)


class HousingsTypes(db.Model):
    __tablename__ = 'housings_types'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    icon: Mapped[str] = mapped_column(String(40), nullable=True)
    required_department_number: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class Housings(db.Model):
    __tablename__ = 'housings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)

    housing_type_id: Mapped[int] = mapped_column(ForeignKey('housings_types.id'), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False, index=True)
    renter_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True, nullable=True)
    address_id: Mapped[int] = mapped_column(ForeignKey('addresses.id'), nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),
                                                          nullable=False,
                                                          default=datetime.datetime.utcnow())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),
                                                          nullable=False,
                                                          default=datetime.datetime.utcnow())


class Units(db.Model):
    __tablename__ = 'units'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    short_name: Mapped[str] = mapped_column(String(15), nullable=False)


class Comforts(db.Model):
    __tablename__ = 'comforts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    unit_id: Mapped[int] = mapped_column(ForeignKey('units.id'), nullable=False)


class ComfortsAssociationTable(db.Model):
    __tablename__ = 'comforts_association_table'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    comfort_id: Mapped[int] = mapped_column(ForeignKey('comforts.id'), nullable=False)
    housing_id: Mapped[int] = mapped_column(ForeignKey('housings.id'), nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)


class Records(db.Model):
    __tablename__ = 'records'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(400), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    housing_id: Mapped[int] = mapped_column(ForeignKey('housings.id'), nullable=False)

    current_status: Mapped[str] = mapped_column(String(30), default='Hidden', nullable=False)
    visitors_amount: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    created_time: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_time: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    CheckConstraint("created_time >= updated_time", name="records_time_check")


class History(db.Model):
    __tablename__ = 'history'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    renter_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    housing_id: Mapped[int] = mapped_column(ForeignKey('housings.id'), index=True)

    rent_start: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    rent_end: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    CheckConstraint("rent_end > rent_start", name="history_rent_time_check")

    price: Mapped[int] = mapped_column(Integer, nullable=False)
