import datetime  
import time

from urllib import quote_plus, unquote_plus
from models import ProductCategory, Company, Fuel, CompanySuppling
from collections import OrderedDict
from django.core.cache import cache

def doUrlify(name):
    name = str(name.encode('utf8'))
    name = name.lower()
    name = quote_plus(name)
    return name
    
def makeDicts():
    # Informations on regions and products for JS environment in the page (populating menus)
    pdcts = {} 
    region_provinces = OrderedDict() 
    for p in ProductCategory.objects.all():
        pdcts[str(p.name)] = str(p.slug)
    
    for c in Company.objects.all().exclude(tel='123'):
        if region_provinces.get(c.region) is None:
            lower = doUrlify(c.region)
            region_provinces[c.region] = [lower, []]
        
        lower = doUrlify(c.province)     
        if [c.province, lower] not in region_provinces.get(c.region)[1]:
            r = region_provinces[c.region]
            r[1].append([c.province, lower])
            
    region_provinces = OrderedDict(sorted(region_provinces.items(), key=lambda t: t[0]))
    return region_provinces, pdcts

def productsList():
    products = []
    for e in ProductCategory.objects.all().filter(type=1).order_by('id'):
        products.append((e.id, e.slug, e.name, 'ico-'+e.slug)) 
    return products
 
def formatPageInfos(paramsArray, title, firstInstance):
    region = 'None'
    province = 'None'
    for k,v in paramsArray.iteritems():
           if k == 'product':
              if v != 'None':
                p = unquote_plus(v).capitalize()
                product = p                                        # set the product
                try:                                               # avoid url hacking
                   fromDB = ProductCategory.objects.get(name=product)
                except:
                   return 'Pellet', None, None, 'Trova Biomassa', 'Seleziona un prodotto', None, None
                description, burning, certif = fromDB.description, fromDB.burning_data, fromDB.certif_data
                if firstInstance == True:
                   title.append(p)
              else:
                product = 'Pellet'
                fromDB = ProductCategory.objects.get(name=product)
                description, burning, certif = fromDB.description, fromDB.burning_data, fromDB.certif_data
                if firstInstance == True:
                   p = unquote_plus(v).capitalize()
                   title.append(p)
           else:
              if v != 'None':
                set = unquote_plus(v)
                set = set.title()
                if firstInstance == True:
                   title.append(set)
                if k == 'region':
                   region = set                                 # the region
                if k == 'province':
                   province = set                               # the province
          
    title = ' '.join(title)
    
    return product, region, province, title, description, burning, certif

class TrovaBiomassa(object):
    '''   
       This class manages the flow of the search from/to the Biomassa handlers
    '''
    def initialize(self, URLencoded):
       self.firstInstance      = False
       self.URLencoded         = URLencoded
       
       #dictionary of values from the URL
       fromURL = self.URLencoded
       
       #make a list of product from the db
       self.products = productsList()
         
       #set a variable for page title
       if self.firstInstance == False:
          self.title              = ['Trova Biomassa']
          title                   = self.title
          self.firstInstance      = True
       
       #format for template the values  from the URL 
       self.product, self.region, self.province, self.title, self.description, self.burning, self.certif  = formatPageInfos(fromURL, title, self.firstInstance)
       
       #dictionary of formatted values
       self.URLdecoded = {'product': self.product, 'region': self.region, 'province': self.province}
       
       #dictionaries to handle the values passed to Javascript (populating menus)
       self.regions, self.pdcts = makeDicts()
       
       #list to handle the geocoded results
       self.listed = []
               
    def getMarkers(self):
        '''
           Handler for datastore lookup for product/region/province
        '''
        # get parameters as come down from URL 
        fromURL = self.URLdecoded
        
        # get the single product key
        p = ProductCategory.objects.get(name=fromURL['product'])
        
        if p is None:
            return {}
            
        id = p.id
        
        # mkts
        # = Fuel.objects.all().filter(selling=True).filter(product=id)
        
        if fromURL['region'] == 'None': 
            self.mkts = Fuel.objects.all().filter(selling=True).filter(product=id) # use the starting query
        else:
            if fromURL['province'] == 'None': 
                self.mkts = Fuel.objects.all().filter(selling=True).filter(product=id).filter(reseller__region=fromURL['region']) # add Region filter
            else:
                self.mkts = Fuel.objects.all().filter(selling=True).filter(product=id).filter(reseller__province=fromURL['province']) # add Province filter
        
        # checking if the counter has changed, if true setting cache, else getting       
        counter = self.mkts.count()

        cache_key = str(fromURL['product'] +'-'+ fromURL['region'] +'-'+ fromURL['province']).replace(" ","-")
        cache_key_counter = cache_key +'-counter'
        get_counter = cache.get(cache_key_counter)
        get_data = cache.get(cache_key)

        if get_counter and get_data:
            if get_counter != counter:
                GeoJson = self.doGeoLoc()
                cache.set(cache_key, GeoJson)
                return GeoJson
            else:
                cache.set(cache_key_counter, counter)
                return get_data
        else:
            cache.set(cache_key_counter, counter)
            GeoJson = self.doGeoLoc()
            cache.set(cache_key, GeoJson)
            return GeoJson

    
    def doGeoLoc(self):
        '''
           Data is made in GeoJson v1 format http://geojson.org/geojson-spec.html 
        '''
        GeoJson = { "type": "FeatureCollection",
                  "features": []
                  }
        for m in self.mkts:
            data = {'company': m.reseller.name, 'product': m.product.name, 'address': m.reseller.address, 'p_slug': m.product.slug,
                    'city': m.reseller.city,'CAP': m.reseller.CAP,  'province': m.reseller.province, 
                    'region':m.reseller.region, 'slug': m.reseller.slug, 'id': m.reseller_id, 'web': m.reseller.web}
            offers = []
            e = m.reseller
            coords = [e.lng, e.lat]
            list_of_packages = []
            for f in Fuel.objects.all().filter(reseller=e.id):
                inner_data = {}
                certificates = []
                inner_data['package'] = f.package.name
                if f.product.name == m.product.name:
                    list_of_packages.append(f.package.name)
                inner_data['price'] = f.selling_price
                for c in f.certification.all():
                    certificates.append(c.name)
                inner_data['certificates'] = certificates
                inner_data['rating'] = f.rating
                
                if f.producer is not None:
                    inner_data['producer'] = f.producer.name
                offers.append(inner_data)

                data['offers'] = offers

            data['list_of_packages'] = list(set(list_of_packages))
            
            if data not in self.listed:
                    result = {
                       "type": "Feature", 
                       "geometry": {"type": "Point", "coordinates": []}, 
                       "properties":{} 
                    }
                    self.listed.append(data)
                    result['properties'] = data
                    result['geometry']['coordinates'] = coords
                    GeoJson['features'].append(result)
        
        return GeoJson

def ToBuyBiomassFuels(id, product):
        '''
           Function to build the data for presenting the final query results
           (single company lookup)
        '''
        listed = []
        GeoJson = { "type": "FeatureCollection",
                  "features": []
                  }
                  
        c = Company.objects.get(id=id)
        p = ProductCategory.objects.get(slug=product)
        
        position = [CompanySuppling._getName(p) for p in c.supply_positioning.all()]

        data = {'company': c.name, 'address': c.address,
                'city': c.city,'CAP': c.CAP,  'province': c.province, 
                'region':c.region, 'slug': c.slug, 'ID': id, 'web': c.web, 'email': c.email,
                'tel': c.tel, 'position': position}
        offers = []
        selling = []
        produced_in = []
        coords = [c.lng, c.lat]

        for f in Fuel.objects.all().filter(reseller=id).filter(selling=True):
            inner_data = {}
            certificates = []
            inner_data['package'] = f.package.name
            inner_data['price'] = f.selling_price
            for c in f.certification.all():
                certificates.append(c.name)
            inner_data['certificates'] = certificates
            inner_data['rating'] = f.rating
            inner_data['product'] = f.product.name
            inner_data['product_slug'] = f.product.slug
            if f.product.name not in selling: selling.append(f.product.name)
            inner_data['is_local'] = f.is_local
            inner_data['made_in_italy'] = f.made_in_italy
            inner_data['made_in_eu'] = f.made_in_eu
            inner_data['made_outside'] = f.made_outside
                
            if f.producer is not None:
                inner_data['producer'] = f.producer.name
                inner_data['produced_in'] = f.producer.country
                inner_data['couriers'] = [[c.name,c.id,c.slug] for c in f.reseller.courier.all()]
            offers.append(inner_data)

            data['offers'] = offers
            data['selling'] = selling
            
        if data not in listed:
            result = {
                "type": "Feature", 
                "geometry": {"type": "Point"}, 
                "properties":{} 
                }
            listed.append(data)
            result['properties'] = data
            result['geometry']['coordinates']= coords
            GeoJson['features'].append(result)
        
        return GeoJson
