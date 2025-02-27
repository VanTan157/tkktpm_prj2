class DBRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'cart' and model._meta.model_name == 'cart':
            return 'postgresql'
        elif model._meta.app_label == 'customer' and model._meta.model_name == 'customer':
            return 'mysql'
        elif model._meta.app_label == 'mobile' and model._meta.model_name == 'mobile':
            return 'mongodb'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'cart' and model._meta.model_name == 'cart':
            return 'postgresql'
        elif model._meta.app_label == 'customer' and model._meta.model_name == 'customer':
            return 'mysql'
        elif model._meta.app_label == 'mobile' and model._meta.model_name == 'mobile':
            return 'mongodb'
        return 'default'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'cart' and model_name == 'cart':
            return db == 'postgresql'
        elif app_label == 'customer' and model_name == 'customer':
            return db == 'mysql'
        elif app_label == 'mobile' and model_name == 'mobile':
            return db == 'mongodb'
        return db == 'default'