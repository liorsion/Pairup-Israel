# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding unique constraint on 'ExperienceCategory', fields ['name']
        db.create_unique('experience_categories_experiencecategory', ['name'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'ExperienceCategory', fields ['name']
        db.delete_unique('experience_categories_experiencecategory', ['name'])


    models = {
        'experience_categories.experiencecategory': {
            'Meta': {'object_name': 'ExperienceCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['experience_categories']
