# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UserStatModel'
        db.create_table('stats_userstatmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stat_type', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('stat_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('related_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userprofile.UserProfile'])),
        ))
        db.send_create_signal('stats', ['UserStatModel'])

        # Deleting field 'StatModel.related_user'
        db.delete_column('stats_statmodel', 'related_user_id')


    def backwards(self, orm):
        
        # Deleting model 'UserStatModel'
        db.delete_table('stats_userstatmodel')

        # Adding field 'StatModel.related_user'
        db.add_column('stats_statmodel', 'related_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userprofile.UserProfile'], null=True, blank=True), keep_default=False)


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'experience_categories.experiencecategory': {
            'Meta': {'object_name': 'ExperienceCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'stats.statmodel': {
            'Meta': {'object_name': 'StatModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stat_counter': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'stat_type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4', 'db_index': 'True'}),
            'stat_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'stats.userstatmodel': {
            'Meta': {'object_name': 'UserStatModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'related_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userprofile.UserProfile']"}),
            'stat_type': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'stat_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'userprofile.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'extra_info': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'looking_for_position': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['experience_categories.ExperienceCategory']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'user_slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['stats']
