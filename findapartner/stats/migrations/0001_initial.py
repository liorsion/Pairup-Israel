# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'StatModel'
        db.create_table('stats_statmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stat_type', self.gf('django.db.models.fields.CharField')(max_length=4)),
        ))
        db.send_create_signal('stats', ['StatModel'])


    def backwards(self, orm):
        
        # Deleting model 'StatModel'
        db.delete_table('stats_statmodel')


    models = {
        'stats.statmodel': {
            'Meta': {'object_name': 'StatModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stat_type': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        }
    }

    complete_apps = ['stats']
