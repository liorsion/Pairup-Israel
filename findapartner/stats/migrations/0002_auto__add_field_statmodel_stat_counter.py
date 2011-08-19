# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'StatModel.stat_counter'
        db.add_column('stats_statmodel', 'stat_counter', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'StatModel.stat_counter'
        db.delete_column('stats_statmodel', 'stat_counter')


    models = {
        'stats.statmodel': {
            'Meta': {'object_name': 'StatModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stat_counter': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'stat_type': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        }
    }

    complete_apps = ['stats']
