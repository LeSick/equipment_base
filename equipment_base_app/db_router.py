class AppDataRouter:
    app_labels = {'equipment', 'repairs', 'homepage', 'accounts'}  # your custom apps

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.app_labels:
            return 'appdata'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.app_labels:
            return 'appdata'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.app_labels or
            obj2._meta.app_label in self.app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.app_labels:
            return db == 'appdata'
        return db == 'default'