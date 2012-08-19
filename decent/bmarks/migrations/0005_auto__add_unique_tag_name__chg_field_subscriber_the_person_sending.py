# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Tag', fields ['name']
        db.create_unique('bmarks_tag', ['name'])


        # Changing field 'Subscriber.the_person_sending'
        db.alter_column('bmarks_subscriber', 'the_person_sending_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bmarks.Address']))

    def backwards(self, orm):
        # Removing unique constraint on 'Tag', fields ['name']
        db.delete_unique('bmarks_tag', ['name'])


        # Changing field 'Subscriber.the_person_sending'
        db.alter_column('bmarks_subscriber', 'the_person_sending_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bmarks.Human']))

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
        'bmarks.address': {
            'Meta': {'object_name': 'Address'},
            'domain': ('django.db.models.fields.CharField', [], {'default': "'localhost'", 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'bmarks.bookmark': {
            'Meta': {'ordering': "['-time', 'owner']", 'object_name': 'Bookmark'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bmarks.Address']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bmarks.Tag']", 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'bmarks.human': {
            'Meta': {'object_name': 'Human', '_ormbases': ['auth.User']},
            'address': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bmarks.Address']", 'unique': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'bmarks.subscriber': {
            'Meta': {'object_name': 'Subscriber', '_ormbases': ['bmarks.Address']},
            'address_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bmarks.Address']", 'unique': 'True', 'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {}),
            'the_person_sending': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'the_person_sending'", 'to': "orm['bmarks.Address']"})
        },
        'bmarks.subscription': {
            'Meta': {'object_name': 'Subscription', '_ormbases': ['bmarks.Address']},
            'address_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bmarks.Address']", 'unique': 'True', 'primary_key': 'True'}),
            'last_received_update': ('django.db.models.fields.DateTimeField', [], {}),
            'the_person_listening': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bmarks.Human']"})
        },
        'bmarks.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['bmarks']