#!/usr/bin/env python3

from random import choice as rc
import logging

from app import app
from models import db, Bakery, BakedGood

# Configure logging
logging.basicConfig(level=logging.INFO)

with app.app_context():
    try:
        # Delete all existing records
        BakedGood.query.delete()
        Bakery.query.delete()
        
        # Create bakery instances
        bakeries = [
            Bakery(name='Delightful Donuts'),
            Bakery(name='Incredible Crullers')
        ]
        
        # Add bakeries to session
        db.session.add_all(bakeries)
        db.session.commit()
        
        logging.info('Bakeries added successfully.')

        # Create baked goods instances
        baked_goods = [
            BakedGood(name='Chocolate Dipped Donut', price=2.75, bakery=bakeries[0]),
            BakedGood(name='Apple-Spice Filled Donut', price=3.50, bakery=bakeries[0]),
            BakedGood(name='Glazed Honey Cruller', price=3.25, bakery=bakeries[1]),
            BakedGood(name='Chocolate Cruller', price=3.40, bakery=bakeries[1])
        ]

        # Add baked goods to session
        db.session.add_all(baked_goods)
        db.session.commit()

        logging.info('Baked goods added successfully.')
    
    except Exception as e:
        logging.error(f'Error occurred: {str(e)}')
        db.session.rollback()

    finally:
        db.session.close()
