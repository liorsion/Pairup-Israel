# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Partner'
        db.create_table('partner_partner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('general_description', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('experience_general', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('add_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('partner', ['Partner'])

        # Adding M2M table for field categories on 'Partner'
        db.create_table('partner_partner_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('partner', models.ForeignKey(orm['partner.partner'], null=False)),
            ('category', models.ForeignKey(orm['categories.category'], null=False))
        ))
        db.create_unique('partner_partner_categories', ['partner_id', 'category_id'])

        # Adding M2M table for field experience_categories on 'Partner'
        db.create_table('partner_partner_experience_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('partner', models.ForeignKey(orm['partner.partner'], null=False)),
            ('experiencecategory', models.ForeignKey(orm['experience_categories.experiencecategory'], null=False))
        ))
        db.create_unique('partner_partner_experience_categories', ['partner_id', 'experiencecategory_id'])


    def backwards(self, orm):
        
        # Deleting model 'Partner'
        db.delete_table('partner_partner')

        # Removing M2M table for field categories on 'Partner'
        db.delete_table('partner_partner_categories')

        # Removing M2M table for field experience_categories on 'Partner'
        db.delete_table('partner_partner_experience_categories')


    models = {
        'categories.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'experience_categories.experiencecategory': {
            'Meta': {'object_name': 'ExperienceCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'partner.partner': {
            'Meta': {'object_name': 'Partner'},
            'add_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['categories.Category']", 'symmetrical': 'False'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'experience_categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['experience_categories.ExperienceCategory']", 'symmetrical': 'False'}),
            'experience_general': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'general_description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['partner']
