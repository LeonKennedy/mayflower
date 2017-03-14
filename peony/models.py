import uuid, datetime, pdb
from django.db import models
from django.core import serializers


class PeonyModel(models.Model):
    models_str = ("user", "item", "account")
    class Meta:
        abstract = True

    def getBaseDict(self):
        return dict([(i.attname,self.__getattribute__(i.attname)) for i in self._meta.fields ])

    def dictializer(self,queryset =None, dictionary=None):
        if queryset:
            for k in queryset:
                if(hasattr(self, k)):
                    object.__setattr__(self, k, queryset.get(k))
            return True
        for k in dictionary.keys():
            if(hasattr(self, k)):
                object.__setattr__(self, k, dictionary[k])
        

class User(PeonyModel):
    device_id = models.CharField(max_length=64, unique=True, default='olenji')
#    nickname = models.CharField(max_length=200, default=None)
    phone = models.CharField(max_length=55, unique=True,default=None, null=True)
#    password = models.CharField(max_length=66, default = None)
    expenditure = models.FloatField(default=0)
    income = models.FloatField(default=0)
    create_date = models.DateTimeField('date user sign up', auto_now_add=True)
    update_date = models.DateTimeField('last edit', auto_now = True)

    def __str__(self):
        return '[%d] %s %s' % (self.id, self.nickname, self.phone)

class Token(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable  = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField('date user sign up', auto_now_add=True)
    

class Item(PeonyModel):
    name = models.CharField(max_length=124)
    en_name = models.CharField(max_length=124, null=True,default=None)
    bar_code = models.CharField(max_length=64, null=True, default=None)
    price = models.FloatField(default=0)
    img = models.CharField(max_length=255, null=True,default=None)
    netweight = models.FloatField(default=0)
    tag = models.CharField(max_length=122,null=True, default=None)
    origin = models.CharField(max_length=3, null=True,default='US')
    remark = models.CharField(max_length=255, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField('last edit', auto_now = True)
    message = models.CharField(max_length=122,null=True,default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mom = models.ForeignKey('self', on_delete=models.CASCADE,null=True)

    def __str__(self):
        return str(self.id)

    def itemcopy(self,i):
        pass_attr = ('id', 'mom', 'user', 'create_data', 'update_date')
        attr = [ i.attname for i in self._meta.fields if i.attname not in pass_attr ]
        for a in attr:
            object.__setattr__(self, a, i.__getattribute__(a))


class Inventory(PeonyModel):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    item = models.ForeignKey(Item, null=True)
    stock = models.FloatField(default=0)
    num = models.FloatField(default=0)
    income = models.FloatField(default=0)
    expences = models.FloatField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField('last edit', auto_now = True)

#入库账单
class Account(PeonyModel):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    item = models.ForeignKey(Item, null=True)
    num = models.FloatField(default=0)
    #stock = models.FloatField(default=0)
    price = models.FloatField(default=0)
    shop = models.CharField(max_length=124, default=None)
    totalprice = models.FloatField('total price', default=0)
    origin = models.CharField(max_length=3, default='US')
    paytype = models.CharField(max_length=3, default = 0 )
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField('last edit', auto_now = True)
    message = models.CharField(max_length=255, default=None, null=True)
    # 0 is default
    # 7 is delete
    status = models.SmallIntegerField(default = 0 )
    inventory = models.ForeignKey(Inventory,null=True)


#售出账单
class Sales(PeonyModel):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    item = models.ForeignKey(Item, null=True)
    num = models.FloatField(default=0)
    price = models.FloatField(default=0)
    totalprice = models.FloatField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField('last edit', auto_now = True)
    message = models.CharField(max_length=255, default=None, null=True)
    # 0 is default
    # 7 is delete
    status = models.SmallIntegerField(default = 0 )
    
class Captcha(PeonyModel):
    phone = models.CharField(max_length=15,unique=True)
    code = models.PositiveIntegerField()
    last_date = models.DateTimeField(auto_now = True)

    def isExpired(self):
        print(self.last_date)
        print(datetime.datetime.utcnow() - datetime.timedelta(minutes=15))
        return self.last_date < (datetime.datetime.utcnow() - datetime.timedelta(minutes=15))
    

class Feedback(PeonyModel):
    user = models.ForeignKey(User)
    content = models.CharField(max_length=512, default=None)
    create_date = models.DateTimeField(auto_now_add=True)
    
    
    



