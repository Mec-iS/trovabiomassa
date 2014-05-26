from django.contrib import admin
from models import Company, Certificate, ProductCategory, Package, Fuel, Deliver, Boiler, CompanySuppling, ProductGroup
from django.db.models import Q
from urllib import quote_plus

def doUrlify(name):
    name = name.lower()
    name = quote_plus(name.encode('utf8'))
    return name


class CompanyAdmin(admin.ModelAdmin):
    
    def save_model(self, request, obj, form, change):
        obj.who = request.user
        name = obj.name
        name = doUrlify(name)
        obj.slug = name
        obj.save()
        
class CertificateAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.who = request.user
        obj.save()
        
class ProductCategoryAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.who = request.user
        name = obj.name
        name = doUrlify(name)
        obj.slug = name
        obj.save()
        
class PackageAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.who = request.user
        name = obj.name
        name = doUrlify(name)
        obj.slug = name
        obj.save()

'''



class FuelCOURIERInline(admin.StackedInline):
    model = Fuel.courier.through
    model._meta.verbose_name_plural = "Possibili Trasporti"
    model._meta.verbose_name = "Traporto"
    
class FuelPRODUCERInline(admin.StackedInline):
    model = Fuel.producer.through
    model._meta.verbose_name_plural = "Fornitori da cui compra"
    model._meta.verbose_name = "Fornitori"
'''
        
class FuelAdmin(admin.ModelAdmin):
    #exclude = ['package', 'courier', 'producer']
    #inlines = [FuelPKGInline, FuelCOURIERInline, FuelPRODUCERInline]
    '''
    def formfield_for_manytomanykey(self, db_field, request, **kwargs):
        if db_field.name == "courier":
            kwargs["queryset"] = Company.objects.filter(categories__id=3)
        return super(FuelAdmin, self).formfield_for_manytomanykey(db_field, request, **kwargs)
    '''
    def save_model(self, request, obj, form, change):
        obj.who = request.user
        obj.save()
        
class DeliverAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.who = request.user
        obj.save()
        
class BoilerAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.who = request.user
        obj.save()

class ProductGroupAdmin(admin.ModelAdmin):
    pass
class CompanySupplingAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Company, CompanyAdmin)
admin.site.register(Certificate, CertificateAdmin)
admin.site.register(ProductGroup, ProductGroupAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Fuel, FuelAdmin)
admin.site.register(Deliver, DeliverAdmin)
admin.site.register(Boiler, BoilerAdmin)

admin.site.register(CompanySuppling, CompanySupplingAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
