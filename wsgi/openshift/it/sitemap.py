
#from django.contrib.sitemaps import Sitemap
from it.models import ProductCategory, Company, Fuel
from urllib import quote_plus
#from django.core.urlresolvers import reverse
from it.TrovaBiomassa import productsList, formatPageInfos, makeDicts
from django.http import StreamingHttpResponse

def Sitemap(request):
    html= ['''<?xml version="1.0" encoding="UTF-8"?>
        <urlset
           xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
           http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
            <url>
                <loc>http://www.trovabiomassa.com/</loc>
            </url>
            <url>
                <loc>http://www.trovabiomassa.com/privacy/</loc>
            </url>
            <url>
                <loc>http://www.trovabiomassa.com/about/</loc>
            </url>
            <url>
                <loc>http://www.trovabiomassa.com/energia/</loc>
            </url>'''
        ]
    
    #to be optimized
    region_provinces, products = makeDicts()
    
    for k, v in products.iteritems():
        html.append('<url><loc>http://www.trovabiomassa.com/cercabiomassa/'+v+'/</loc></url>')
        html.append('<url><loc>http://www.trovabiomassa.com/trovabiomassa/'+v+'/</loc></url>')
        regions = []
        for key, val in region_provinces.iteritems():
            provinces = []
            if val[0] not in regions:
                regions.append(val[0])
                html.append('<url><loc>http://www.trovabiomassa.com/cercabiomassa/'+v+'/'+val[0]+'/</loc></url>')
                for el in val:
                    if val.index(el) != 0:
                       if el not in provinces:
                           provinces.append(el)
                           for e in el:
                               html.append('<url><loc>http://www.trovabiomassa.com/cercabiomassa/'+v+'/'+val[0]+'/'+e[1]+'/</loc></url>')
        
        for f in Fuel.objects.all():
            set = [f.product.slug, f.reseller.region, f.reseller.province, f.reseller.name, str(f.reseller.id)]
            for e in set:
               e.encode('utf8')
               set[set.index(e)] = quote_plus(e.lower().encode('utf8'))
            html.append('<url><loc>http://www.trovabiomassa.com/'+set[0]+'/'+set[1]+'/'+set[2]+'/trova/'+set[3]+'/'+set[4]+'/'+set[0]+'/</loc></url>')
            
        
    
    html.append('</urlset>')
    
    ''.join(html)
    
    return StreamingHttpResponse(html, content_type="text/xml")
    
def Robots(request):
    
    html = 'User-agent: * Disallow: /admin/ Disallow: /coordinate/ Disallow: /user/ Sitemap: http://www.trovabiomassa.com/sitemap.xml'
    return StreamingHttpResponse(html, content_type="text/html")

