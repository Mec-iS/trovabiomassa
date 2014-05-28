# encoding: utf-8

from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import ugettext as _

class CompanySuppling(models.Model):
    '''
       Position in supply chain
    '''
    class Meta:
        verbose_name = u'Posición en la cadena'
        verbose_name_plural = u'Posiciones en la cadena de suministro'
    TYPES_CMP = (
    (0, u'Productor'),
    (1, u'Intermediario (B2B)'),
    (2, u'Dealer (al por mayor)'),
    (3, u'Dealer (detalle)'),
    (5, u'Proveedor de Servicios'),
    (6, u'instalador'),
    )
    
    id                  = models.AutoField(primary_key=True)
    type                = models.IntegerField(max_length=50, choices=TYPES_CMP)
    
    def __unicode__(self):
        name = ''
        for i in self.TYPES_CMP:
           if i[0] == self.type:
              name = i[1]
        return name
    def _getName(self):
        name = ''
        for i in self.TYPES_CMP:
           if i[0] == self.type:
              name = str(i[1])
        return name
    
class ProductGroup(models.Model):
    '''
       Products sold by companies
    '''
    class Meta:
        verbose_name = u'Categoría de producto'
        verbose_name_plural = u'Categorías de productos'
    TYPES_SOLD = (
    (1, u'Combustible'),
    (2, u'Caldera'),
    (3, u'Transporte'),
    (4, u'Central'),
    )

    id                  = models.AutoField(primary_key=True)
    category            = models.IntegerField(max_length=50, choices=TYPES_SOLD)
    
    def __unicode__(self):
        name = ''
        for i in self.TYPES_SOLD:
           if i[0] == self.category:
              name = i[1]
        return name    

class Company(models.Model):
    '''
    All companies' datas
    '''
    class Meta:
        ordering = ['name']
        verbose_name = u'Empresa o Zona Geográfica'
        verbose_name_plural = u'Empresas y Áreas Geográficas'

    id                  = models.AutoField(primary_key=True)
    name                = models.CharField(max_length=150)
    owner_of_account    = models.ForeignKey(User, related_name='+')
    added               = models.DateTimeField(auto_now_add = True)
    modified            = models.DateTimeField(auto_now = True)
    address             = models.CharField(max_length=150)
    city                = models.CharField(max_length=50)
    CAP                 = models.CharField(max_length=8)
    province            = models.CharField(max_length=80)
    region              = models.CharField(max_length=50)
    country             = models.CharField(max_length=5, default='ES')
    lat                 = models.FloatField()
    lng                 = models.FloatField()
    supply_positioning  = models.ManyToManyField(CompanySuppling)
    products_group      = models.ManyToManyField(ProductGroup)
    tel                 = models.CharField(max_length=100)
    web                 = models.CharField(max_length=254, null=True, blank=True, default='')
    email               = models.CharField(max_length=80, null=True, blank=True, default='')
    #cmpUserID          = db.StringProperty(default='')
    slug                = models.SlugField(unique=True, editable=False) # URLify(quote_plus() and lower() of /cmpRegion/cmpProv/cmpName/
    courier             = models.ManyToManyField('self', null=True, blank=True)
    
    def __unicode__(self):
        return self.name

class Chain(models.Model):
    '''
       recursive class describing companies supply chain 
    '''
    id                  = models.AutoField(primary_key=True)
    seller              = models.ForeignKey(Company)
    supplier            = models.ForeignKey('self', default=None, null=True, blank=True)
        
class Certificate(models.Model):
    '''
    Each product class has one or more certificates
    '''
    class Meta:
        verbose_name = u'Certificación'
        verbose_name_plural = u'Certificaciones'

    name           = models.CharField(max_length=80) 
    detail         = models.CharField(max_length=500) 
    
    def __unicode__(self):
        return self.name

class ProductCategory(models.Model):
    ''' 
    Products macro-categories
    '''
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        
    TYPES = (
    (1, u'Combustible'),
    (2, u'Caldera'),
    (3, u'Transporte'),
    (4, u'Central'),
    )
    id                   = models.AutoField(primary_key=True)
    slug                 = models.SlugField(unique=True, editable=False)
    type                 = models.IntegerField(default=1, choices=TYPES) # 1:Combustibile 2:Caldaia 3:Trasporto 4:Centrale
    description          = models.TextField(null=True, blank=True)
    name                 = models.CharField(max_length=100) # es. Pellet, Nocciolino, Caldaia HT234
    burning_data         = models.TextField(null=True, blank=True)
    certif_data          = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
        new = ''
        for n in self.name:
             new += unicode(n).encode('utf-8')

        return str(new)
        
class Package(models.Model):
    class Meta:
        verbose_name = 'Formato de embalaje'
        verbose_name_plural = 'Formatos de embalaje'

    id                   = models.AutoField(primary_key=True)
    slug                 = models.SlugField(unique=True, editable=False)
    name                 = models.CharField(max_length=100)
    weight_kg            = models.FloatField(null=True, blank=True) 

    def __unicode__(self):
        return self.name+'/'+str(self.weight_kg)
    
    def __str__(self):
        return self.name+'/'+str(self.weight_kg)
        
class Fuel(models.Model):
    '''
    Fuels' offers
    '''
    class Meta:
        verbose_name = '<Oferta> Combustible en el mercado'
        verbose_name_plural = '<Oferta> Combustibles en el mercado'

    id                   = models.AutoField(primary_key=True)
    reseller             = models.ForeignKey(Company, related_name='fuel_seller')
    product              = models.ForeignKey(ProductCategory, related_name='fuel_kind') # Pellet - Nocciolino - Caldaia - Trasporto - Centrale
    package              = models.ForeignKey(Package)
    producer             = models.ForeignKey(Company, null=True, blank=True)
    certification        = models.ManyToManyField(Certificate)
    rating               = models.FloatField(null=True, default=0.0)
    selling_price        = models.FloatField()
       
    is_local             = models.BooleanField(default=False)
    made_in_italy        = models.BooleanField(default=False)
    made_in_eu           = models.BooleanField(default=False)
    made_outside         = models.BooleanField(default=False)
    specs                = models.CharField(max_length=350, null=True, blank=True)
    selling              = models.BooleanField(default=True)
   
   
    added                = models.DateTimeField(auto_now_add = True)
    modified             = models.DateTimeField(auto_now = True)
    
    
    
    def __unicode__(self):
        if self.producer:
            producer = str(self.producer.name)
            return 'ID:'+str(self.id)+'>'+self.product.slug+' venduto da '+self.reseller.slug+' in '+str(self.package.name)+' prodotto da '+producer
        return 'ID:'+str(self.id)+'>'+self.product.slug+' venduto da '+self.reseller.slug+' in '+str(self.package.name)
    
 
class Boiler(models.Model):
    '''
        Boilers' offers
    '''
    class Meta:
        verbose_name = '<Oferta> Caldera en el mercado'
        verbose_name_plural = '<Oferta> Caldera en el mercado'

    id                   = models.AutoField(primary_key=True)
    reseller             = models.ForeignKey(Company, related_name='boiler_seller')
    product              = models.ForeignKey(ProductCategory, related_name='boiler_kind') # Pellet - Nocciolino - Caldaia - Trasporto - Centrale
    
    description          = models.CharField(max_length=350, null=True)   
    producer             = models.ForeignKey(Company, null=True, blank=True)
    Heating              = models.CharField(max_length=50, choices=((u'acqua',u'ad acqua'),(u'aria',u'ad aria'),))  #  ad aria calda, ad acqua calda
    fuel                 = models.ManyToManyField(ProductCategory)
    minpower             = models.IntegerField() # in Kw, lower end of the range
    maxpower             = models.IntegerField() # in Kw, upper end of the range
    surface              = models.IntegerField() # in m2
    price                = models.FloatField()
    certification        = models.ManyToManyField(Certificate)
    selling              = models.BooleanField(default=True)
    
    
    
    added                = models.DateTimeField(auto_now_add = True)
    modified             = models.DateTimeField(auto_now = True)
    
    
    
    #BoilerType          = db.ReferenceProperty(Products) # subcategory of boilers
    
class Deliver(models.Model):
    '''
    Child class from Market that stores the transports' offers
    '''
    class Meta:
        verbose_name = '<Oferta> Transporte en el mercado'
        verbose_name_plural = '<Oferta> Transporte en el mercado'
        
    VEHICLES = (
    (u'camiones', u'camion'),
    (u'vehículo articulado', u'autoarticolato'),
    (u'van', u'furgone'),
    (u'caja abierta ', u'cassonato'),
    )
    LOADERS = (
    (u'neumático', u'neumático'), 
    (u'volquete', u'volquete'), 
    (u'piano móvil', u'piano móvil'), 
    (u'grúa', u'grúa'), 
    (u'cisterna', u'cisterna'),
    )
    
    id                   = models.AutoField(primary_key=True)
    server               = models.ForeignKey(Company, related_name='deliver_server')
    package              = models.ManyToManyField(Package)
    vehicle              = models.CharField(max_length=50, choices=VEHICLES)
    unloader             = models.CharField(max_length=50, choices=LOADERS)
    maxQ                 = models.IntegerField(null=True) # consegna massima eseguibile in q
    minQ                 = models.IntegerField(null=True) # consegna minima eseguibile in q
    payload              = models.IntegerField(null=True) # portata in tons
    eurocat              = models.CharField(max_length=5)
    COTwo                = models.FloatField(null=True) # emissioni cm3/Km
    range                = models.IntegerField(default=20, null=True) #raggio di consegna massimo



    
'''
class powerPlant(Market):
    
    Child class from Market that stores big powerplants' positions
   
    input                = models.CharField(max_length=) # possibili combustibili
    output           = db.FloatProperty() # output in Kw/Mw
    unity            = db.StringProperty(choices=['KW', 'MW'])
    type             = db.StringProperty(choices=['biomassa', 'fotovoltaico termico', 'fotovoltaico','biogas', 'biomassa alghe'])
    producer         = db.ReferenceProperty(Companies, collection_name='plant_prod')
    owner            = db.ReferenceProperty(Companies, collection_name='plant_owner')
    features         = db.TextProperty()
    lat              = db.FloatProperty(required = True)
    lng              = db.FloatProperty(required = True)


(
    (u'', u''),
    (u'', u''),
    (u'', u''),
    (u'', u''),
    )
'''
