# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding index on 'StatModel', fields ['stat_type']
        db.create_index('stats_statmodel', ['stat_type'])

        # Adding unique constraint on 'StatModel', fields ['stat_type']
        db.create_unique('stats_statmodel', ['stat_type'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'StatModel', fields ['stat_type']
        db.delete_unique('stats_statmodel', ['stat_type'])

        # Removing index on 'StatModel', fields ['stat_type']
        db.delete_index('stats_statmodel', ['stat_type'])


    models = {
        'stats.statmodel': {
            'Meta': {'object_name': 'StatModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stat_counter': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'stat_type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4', 'db_index': 'True'})
        }
    }

    complete_apps = ['stats']
