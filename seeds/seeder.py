"""Base Seeder functionality."""

from webframe.core.app import App
from webframe.utils import db

class Seeder:
    """Base Seeder class."""

    def run(self):
        pass

def run_seeds(seed_list, engine):
    """Run seeders in given list."""
    App().db() = db.make_session(engine)

    for seeder in seed_list:
        print('Seeding: ' + seeder.__class__.__name__)
        seeder.run()




