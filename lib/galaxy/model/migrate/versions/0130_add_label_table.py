"""
Migration script to add the history_dataset_association_label table.
"""
from sqlalchemy import *
from sqlalchemy.orm import *
from migrate import *
from migrate.changeset import *
from galaxy.model.custom_types import *
from sqlalchemy.exc import *
import datetime
now = datetime.datetime.utcnow

import sys
import logging
log = logging.getLogger( __name__ )
log.setLevel( logging.DEBUG )
handler = logging.StreamHandler( sys.stdout )
format = "%(name)s %(levelname)s %(asctime)s %(message)s"
formatter = logging.Formatter( format )
handler.setFormatter( formatter )
log.addHandler( handler )

metadata = MetaData()

# New table to store information about cloned tool shed repositories.
HistoryDatasetAssociationLabel_table = Table( "history_dataset_association_label", metadata,
    Column( "id", Integer, primary_key=True ),
    Column( "history_dataset_association_id", Integer, ForeignKey( "history_dataset_association.id" ), index=True ),
    Column( "create_time", DateTime, default=now ),
    Column( "update_time", DateTime, default=now, onupdate=now ),
    Column( "label", TrimmedString( 255 ) ) )

def upgrade(migrate_engine):
    metadata.bind = migrate_engine
    print __doc__
    metadata.reflect()
    try:
        HistoryDatasetAssociationLabel_table.create()
    except Exception, e:
        log.debug( "Creating history_dataset_association_label table failed: %s" % str( e ) )

def downgrade(migrate_engine):
    metadata.bind = migrate_engine
    metadata.reflect()
    try:
        HistoryDatasetAssociationLabel_table.drop()
    except Exception, e:
        log.debug( "Dropping history_dataset_association_label table failed: %s" % str( e ) )
