import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey, DateTime, Boolean, CheckConstraint, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from sqlalchemy.sql import text


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

    first_name: Mapped[str] = mapped_column(String(20), nullable=False)
    second_name: Mapped[str] = mapped_column(String(20), nullable=False)


class SettlementsTypes(db.Model):
    __tablename__ = 'settlements_types'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)


class Countries(db.Model):
    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)


class Settlements(db.Model):
    __tablename__ = 'settlements'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)

    country_id: Mapped[int] = mapped_column(ForeignKey('countries.id', ondelete="CASCADE"), nullable=False, index=True)
    settlement_type_id: Mapped[int] = mapped_column(ForeignKey('settlements_types.id', ondelete="CASCADE"), nullable=False)


class StreetsTypes(db.Model):
    __tablename__ = 'streets_types'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)


class Streets(db.Model):
    __tablename__ = 'streets'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)

    settlement_id: Mapped[int] = mapped_column(ForeignKey('settlements.id', ondelete="CASCADE"), nullable=False, index=True)
    street_type_id: Mapped[int] = mapped_column(ForeignKey('streets_types.id', ondelete="CASCADE"), nullable=False)


class Addresses(db.Model):
    __tablename__ = 'addresses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    house_number: Mapped[int] = mapped_column(String(5), nullable=False)
    department_number: Mapped[int] = mapped_column(String(5), nullable=True)

    street_id: Mapped[int] = mapped_column(ForeignKey('streets.id', ondelete="CASCADE"), nullable=False)
    settlement_id: Mapped[int] = mapped_column(ForeignKey('settlements.id', ondelete='CASCADE'), nullable=True)
    country_id: Mapped[int] = mapped_column(ForeignKey('countries.id', ondelete='CASCADE'), nullable=True)


class HousingsTypes(db.Model):
    __tablename__ = 'housings_types'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    icon: Mapped[str] = mapped_column(String(40), nullable=True)
    required_department_number: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class Housings(db.Model):
    __tablename__ = 'housings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)

    housing_type_id: Mapped[int] = mapped_column(ForeignKey('housings_types.id', ondelete="CASCADE"), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=False, index=True)
    renter_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True, nullable=True)
    address_id: Mapped[int] = mapped_column(ForeignKey('addresses.id', ondelete="CASCADE"), nullable=False)

    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),
                                                          nullable=False,
                                                          default=datetime.datetime.utcnow())


class Units(db.Model):
    __tablename__ = 'units'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    short_name: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)


class Comforts(db.Model):
    __tablename__ = 'comforts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    unit_id: Mapped[int] = mapped_column(ForeignKey('units.id'), nullable=False)

    min_value: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    max_value: Mapped[int] = mapped_column(Integer, nullable=False, default=1)


class ComfortsAssociationTable(db.Model):
    __tablename__ = 'comforts_association_table'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    comfort_id: Mapped[int] = mapped_column(ForeignKey('comforts.id', ondelete="CASCADE"), nullable=False)
    housing_id: Mapped[int] = mapped_column(ForeignKey('housings.id', ondelete="CASCADE"), nullable=False)
    value: Mapped[int] = mapped_column(Integer, nullable=False)


class Records(db.Model):
    __tablename__ = 'records'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(400), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    housing_id: Mapped[int] = mapped_column(ForeignKey('housings.id', ondelete="CASCADE"), nullable=False)

    current_status: Mapped[str] = mapped_column(String(30), default='Hidden', nullable=False)
    visitors_amount: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    created_date: Mapped[datetime.datetime] = mapped_column(Date, nullable=False,
                                                            default=datetime.datetime.today())
    updated_time: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False,
                                                            default=datetime.datetime.utcnow())

    CheckConstraint("created_time >= updated_time", name="records_time_check")


class History(db.Model):
    __tablename__ = 'history'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    renter_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    housing_id: Mapped[int] = mapped_column(ForeignKey('housings.id'), index=True)

    rent_start: Mapped[datetime.datetime] = mapped_column(Date, nullable=False)
    rent_end: Mapped[datetime.datetime] = mapped_column(Date, nullable=False)

    CheckConstraint("rent_end > rent_start", name="history_rent_time_check")

    price: Mapped[int] = mapped_column(Integer, nullable=False)


class Documents(db.Model):
    __tablename__ = 'documents'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    history_id: Mapped[int] = mapped_column(ForeignKey('history.id', onupdate='CASCADE'), nullable=False)
    file_path: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)


def create_triggers():
    unique_address_trigger_function = text('''\
        CREATE OR REPLACE FUNCTION check_address_is_unique()
        RETURNS trigger AS
        $$
        DECLARE
            addresses_amount integer;
        BEGIN
            SELECT count(*) into addresses_amount FROM addresses
            WHERE street_id = NEW.street_id 
            and department_number = NEW.department_number 
            and house_number = NEW.house_number;
            
            IF addresses_amount > 0 THEN
                RAISE EXCEPTION 'Данный адрес уже был занят!';
            END IF;
            
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    ''')

    address_trigger = text('''\
    CREATE OR REPLACE TRIGGER on_address_insert_unique BEFORE INSERT ON addresses
    FOR EACH ROW
    EXECUTE FUNCTION check_address_is_unique();''')

    update_address_info_after_insert = text('''\
            CREATE OR REPLACE FUNCTION update_address_info_after_insert()
            RETURNS trigger AS
            $$
            DECLARE
                p_country_id integer;
                p_settlement_id integer;
            BEGIN
                SELECT settlement_id INTO p_settlement_id from settlements
                join streets on settlements.id = streets.settlement_id
                where streets.id = NEW.street_id
                limit 1;
                
                SELECT country_id into p_country_id from countries
                join settlements on settlements.country_id = countries.id
                where settlements.id = p_settlement_id
                limit 1;
                
                NEW.country_id := p_country_id;
                NEW.settlement_id := p_settlement_id;

                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        ''')

    update_address_info_after_insert_trigger = text('''\
            CREATE OR REPLACE TRIGGER on_address_insert_data BEFORE INSERT ON addresses
            FOR EACH ROW
            EXECUTE FUNCTION update_address_info_after_insert();''')

    db.session.execute(unique_address_trigger_function)
    db.session.execute(address_trigger)

    db.session.execute(update_address_info_after_insert)
    db.session.execute(update_address_info_after_insert_trigger)

    db.session.commit()
