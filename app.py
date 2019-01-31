import math

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask import Flask, request, jsonify

from setup_db import Base, Product
from validation.validate_in import validate_json, schema

engine = create_engine('sqlite:///lucas_store.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

app = Flask(__name__)


@app.route('/')
@app.route('/api')
def hello_world():
    return 'Welcome to the store API </br> Nothing to show for now'


"""
Receive json as:
{
    "code" : " - ",
    "name" : " - ",
    "description" : " - ",
    "price_unit"  : " - ",
    "price_pack"  : " - "
}
"""


@app.route('/api/products/<int:code_product>', methods=['GET'])
def read_product(code_product):
    session = DBSession()

    try:
        product = session.query(Product).filter_by(code=code_product).one()
        data = {
            "name": product.name,
            "description": product.description,
            "price_unit": product.price_unit / 100,
            "price_pack": product.price_pack / 100
        }
        return jsonify(status="ok", data=data)

    except NoResultFound:
        return jsonify(status="error", message="Product {} not found".format(code_product))

    except MultipleResultsFound:
        return jsonify(status="fail", message="Internal Error: Many results of {}".format(code_product))

    finally:
        session.close()


@app.route('/api/products', methods=['POST'])
@validate_json(schema['/products']['post'])
def create_product():
    session = DBSession()
    json = request.get_json(force=True)
    try:
        # confirm that the product doesn't exist yet
        assert session.query(Product).filter_by(code=json['code']).first() is None,\
            "Product {} duplicated".format(json['code'])

        product = Product(
            code=json['code'],
            name=json['name'],
            description=json['description'],
            price_unit=math.trunc(json['price_unit'] * 100),
            price_pack=math.trunc(json['price_pack'] * 100)
        )

        session.add(product)
        session.commit()
        return jsonify(status="ok")

    except KeyError as error:
        return jsonify(status="error", message="field '{}' is required in json sent".format(error.args[0]))

    except AssertionError as error:
        return jsonify(status="error", message=error.args[0])

    finally:
        session.close()


@app.route('/api/products', methods=['PATCH'])
@validate_json(schema['/products/{code}']['patch'])
def update_product():
    session = DBSession()
    json = request.get_json(force=True)
    try:
        product = session.query(Product).filter_by(code=json['code']).one()
        product.price_unit = json['price_unit']
        product.price_pack = json['price_pack']
        session.commit()
        return jsonify(status="ok")

    except NoResultFound:
        return jsonify(status="error", message="Product {} not found". format(json['code']))

    finally:
        session.close()


@app.route('/api/products', methods=['DELETE'])
@validate_json(schema['/products/{code}']['delete'])
def delete_product():
    session = DBSession()
    json = request.get_json(force=True)
    try:
        product = session.query(Product).filter_by(code=json['code']).one()
        session.delete(product)
        session.commit()
        return jsonify(status="ok")

    except MultipleResultsFound:
        return jsonify(status="error", message="Internal Error: Many products to delete")

    except NoResultFound:
        return jsonify(status="error", message="Product {} not found".format(json['code']))

    finally:
        session.close()


if __name__ == '__main__':
    app.run(debug=True)
