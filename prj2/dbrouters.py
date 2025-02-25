class CustomerRouter:
    """
    Định tuyến truy vấn cho ứng dụng 'customer' sang cơ sở dữ liệu 'mysql'.
    """

    app_label = 'customer'

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return 'mysql'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return 'mysql'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # Cho phép các mối quan hệ giữa các model cùng thuộc một cơ sở dữ liệu
        if obj1._meta.app_label == self.app_label and obj2._meta.app_label == self.app_label:
            return True
        elif self.app_label not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Chỉ migrate các model của app 'customer' sang cơ sở dữ liệu 'mysql'
        if app_label == self.app_label:
            return db == 'mysql'
        # Các app khác chỉ migrate trên cơ sở dữ liệu 'default'
        if db == 'default':
            return True
        return None
