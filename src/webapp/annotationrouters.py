from .models import Course, FavouriteCourse, Post, FavouritePost, Profile, Comment, TagDict, Annotations

#from .models import Annotations

class AnnotationsDBRouter(object):
    def db_for_read(self, model, **hints):
        if model.__class__.__name__== 'annotations':
            return 'annotationsdb'
        else:
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        if model.__class__.__name__== 'annotations':
            return 'annotationsdb'
        else:
            return 'default'

        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        #print(model_name + " " + app_label + " " + db + " Giris")
        if db == 'annotationsdb':
            # Migrate Django core app models if current database is devops
            if model_name in ['auth','admin','annotations']: 
                return True            
            else:
                # Non Django core app models should not be migrated if database is devops
                return False
     
        return None





    """     def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.model_name == 'annotation_label' or \
           obj2._meta.model_name == 'annotation_label':
           return True
        else:
            return 'default'           
        return None """