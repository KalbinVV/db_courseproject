import models


def export_data():
    export_countries()

    export_settlements_types()
    export_russian_towns()

    export_housings_types()
    export_streets_types()

    export_orenburgs_streets()

    export_comforts()


def export_settlements_types():
    settlements_types = ['Город']

    for settlement_type in settlements_types:
        settlement_type_model = models.SettlementsTypes(name=settlement_type)

        models.db.session.add(settlement_type_model)
        models.db.session.commit()


def export_streets_types():
    streets_types = ['Улица', 'Проспект', 'Набережная', 'Шоссе']

    for street_type in streets_types:
        street_type_model = models.StreetsTypes(name=street_type)

        models.db.session.add(street_type_model)
        models.db.session.commit()


def export_housings_types():
    housings_types = [('Квартира', 'Уютная квартира', True, 'department_icon.png'),
                      ('Дом', 'Уютный дом', False, 'house_icon.png'),
                      ('Загородный дом', 'Уютный загородный дом', False, 'villa_icon.png')]

    for housing_type in housings_types:
        housing_type_model = models.HousingsTypes(name=housing_type[0],
                                                  description=housing_type[1],
                                                  required_department_number=housing_type[2],
                                                  icon=housing_type[3])

        models.db.session.add(housing_type_model)
        models.db.session.commit()


def export_countries():
    with open('data/countries.txt', 'r') as f:
        for line in f.readlines():
            if len(line) == '\n':
                continue

            country = models.Countries(name=line.replace('\n', ''))

            models.db.session.add(country)
            models.db.session.commit()


def export_russian_towns():
    russia_id = models.Countries.query.filter_by(name='Россия').first().id
    town_id = models.SettlementsTypes.query.filter_by(name='Город').first().id

    with open('data/russian_towns.txt', 'r') as f:
        for line in f.readlines():
            if len(line) == '\n':
                continue

            settlement = models.Settlements(name=line.replace('\n', ''),
                                            country_id=russia_id, settlement_type_id=town_id)

            models.db.session.add(settlement)
            models.db.session.commit()


def export_orenburgs_streets():
    street_id = models.StreetsTypes.query.filter_by(name='Улица').first().id
    highway_id = models.StreetsTypes.query.filter_by(name='Шоссе').first().id
    pedestrian_id = models.StreetsTypes.query.filter_by(name='Набережная').first().id
    avenue_id = models.StreetsTypes.query.filter_by(name='Проспект').first().id

    orenburg_id = models.Settlements.query.filter_by(name='Оренбург').first().id

    with open('data/orenburg_streets.txt', 'r') as f:
        for line in f.readlines():
            args = line.split('\t')

            street_name = args[0]
            street_type = args[1]

            if street_type == 'pedestrian':
                street_type_id = pedestrian_id
            elif street_type == 'trunk':
                street_type_id = highway_id
            elif street_type == 'primary':
                street_type_id = avenue_id
            else:
                street_type_id = street_id

            street = models.Streets(name=street_name,
                                    street_type_id=street_type_id,
                                    settlement_id=orenburg_id)

            models.db.session.add(street)
            models.db.session.commit()


def export_comforts():
    units = [('Квадратные метры', 'Кв. метры'), ('Штук', 'шт')]

    for unit in units:
        unit_model = models.Units(name=unit[0],
                                  short_name=unit[1])

        models.db.session.add(unit_model)
        models.db.session.commit()

    comforts = [('Количество комнат', 'Количество комнат с учетом кухни', 2, 1, 30),
                ('Площадь', 'Общая площадь помещения', 1, 5, 500),
                ('Количество парковочных мест', 'Количество парковочных мест, поставляемых вместе с жильём.', 2, 0, 15),
                ('Наличие WI-FI', 'Наличие доступа к интернету через WI-FI', 2, 0, 1)]

    for comfort in comforts:
        comfort_mode = models.Comforts(name=comfort[0],
                                       description=comfort[1],
                                       unit_id=comfort[2],
                                       min_value=comfort[3],
                                       max_value=comfort[4])

        models.db.session.add(comfort_mode)
        models.db.session.commit()

