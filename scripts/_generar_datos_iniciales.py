# Genera data/cras.json y data/localidades.json (solo la primera vez). Despues se editan a mano.
import json
CRA_CURSOS='Educación Infantil (2.º ciclo) y Educación Primaria (definición general del modelo CRA; pendiente de verificar en cada centro)'
CRIE_CURSOS='Estancias de convivencia para alumnado de 5.º y 6.º de Primaria de escuelas rurales (excepcionalmente 4.º), según el programa de 2017-18; pendiente de verificar el curso actual'
PEND='Pendiente de verificar'
CRA=[
('teruel-uno','CRA Teruel Uno','Perales del Alfambra',['Alfambra','Argente','Camañas','Galve','Pancrudo','Perales del Alfambra','Visiedo'],'https://crateruel1.catedu.es/','https://crateruel1.catedu.es/inicio/','Primer CRA de Aragón. Agrupa 11 municipios; tiene aulas abiertas en 7 (cerradas: Escorihuela, Fuentes Calientes, Orrios y Rillo). Pancrudo se deduce por eliminación: verificar. Dirección: C/ Frontón 6, 44163 Perales del Alfambra. Tel. 978 775 282.'),
('turia','CRA Turia','San Blas',['Caudé','San Blas','Villalba','Villaspesa','Celadas','Riodeva','Villastar','Villel'],'https://craturia.catedu.es/','https://craturia.catedu.es/presentacion/','Caudé, San Blas, Villalba y Villaspesa son barrios de Teruel capital. Dirección: La Iglesia s/n, 44195 San Blas. Tel. 978 617 557.'),
('somontano-bajo-aragon','CRA Somontano Bajo Aragón','La Mata de los Olmos',['Berge','Cañizar del Olivar','Ejulve','Estercuel','La Mata de los Olmos','Los Olmos','Molinos'],'https://crasomontanobajoaragon.catedu.es/','https://crasomontanobajoaragon.catedu.es/','Siete pueblos del noreste de la provincia.'),
('muniesa','CRA Muniesa','Muniesa',['Alacón','Loscos','Muniesa','Oliete'],'https://cramuniesa.wordpress.com/','https://cramuniesa.wordpress.com/',''),
('sierra-de-albarracin','CRA Sierra de Albarracín','Tramacastilla',['Royuela','Torres de Albarracín','Noguera de Albarracín','Tramacastilla','Griegos','Guadalaviar'],None,'https://plazasprofesores.com/centros-primaria/cra-sierra-de-albarracin/','Fuente secundaria (c. 2022): verificar localidades con el centro.'),
('albarracin','CRA de Albarracín','Albarracín',['Albarracín','Gea de Albarracín'],'https://craalbarracin.catedu.es/','https://craalbarracin.catedu.es/informacion-general/','Desde el curso 2016-17 solo integra Albarracín y Gea de Albarracín.'),
('bronchales-orihuela','CRA Bronchales-Orihuela','Orihuela del Tremedal',['Orihuela del Tremedal','Bronchales'],None,'https://crietcalamocha.catedu.es/informacion-general-2/criet-de-calamocha/documentos/','Creado en 2016 (Decreto 82/2016) al separarse del CRA de Albarracín.'),
('eras-del-jiloca','CRA Eras del Jiloca','El Poyo del Cid',['El Poyo del Cid','Báguena'],None,'https://crietcalamocha.catedu.es/informacion-general-2/criet-de-calamocha/documentos/',''),
('alto-maestrazgo','CRA Alto Maestrazgo','Cantavieja',['Cantavieja','Fortanete','La Iglesuela del Cid','Villarluengo'],'https://craaltomaestrazgo.catedu.es/','https://craaltomaestrazgo.catedu.es/wp-content/uploads/sites/184/2024/04/Plan-de-Acogida-2023-2024.pdf','El plan de acogida 2023-24 habla de cinco localidades pero solo se leen cuatro: verificar la quinta.'),
('algars','CRA Algars','Cretas',['Cretas','Beceite','Lledó'],None,'https://www.lacomarca.net/bajo-aragon-historico-tiene-vacantes-10-plazas-auxiliares-educacion-especial-zona-rural-tambien-hay-ninos-con-necesidades/amp/',''),
('alifara','CRA Alifara','La Fresneda',['La Fresneda','La Portellada','Ráfales'],None,'https://atencioncomunitaria.aragon.es/wp-content/uploads/2024/10/CS-Valderrobres-2024.pdf','Una fuente de 2016 añade Valjunquera: verificar.'),
('tastavins','CRA Tastavins','Peñarroya de Tastavins',['Peñarroya de Tastavins','Fuentespalda','Monroyo'],None,'https://atencioncomunitaria.aragon.es/wp-content/uploads/2024/10/CS-Valderrobres-2024.pdf',''),
('matarranya','CRA Matarranya','Calaceite',['Calaceite','Mazaleón','Valdeltormo'],None,'https://www.dpteruel.es/DPTweb/tag/centros-escolares/feed/',''),
('olea','CRA Olea','Castellote',['Castellote'],None,'https://www.lacomarca.net/cubiertas-solo-4-10-plazas-vacantes-auxiliares-educacion-especial-bajo-aragon-historico/','Seis colegios integran la agrupación; solo la sede está confirmada. Resto de localidades pendiente de verificar.'),
('maestrazgo-gudar','CRA Maestrazgo-Gúdar','Mosqueruela',['Mosqueruela','Linares de Mora'],None,'https://www.dpteruel.es/DPTweb/tag/centros-escolares/feed/','Solo sede y Linares de Mora confirmadas. Resto pendiente de verificar.'),
('bajo-martin','CRA Bajo Martín','La Puebla de Híjar',['La Puebla de Híjar','Urrea de Gaén','Vinaceite'],None,'https://www.dpteruel.es/DPTweb/tag/centros-escolares/feed/','Localidades parciales: verificar el resto.'),
('campo-de-bello','CRA Campo de Bello','Bello',['Bello','Odón'],None,'https://www.dpteruel.es/DPTweb/tag/centros-escolares/feed/','Localidades parciales: verificar el resto.'),
('cuna-del-jiloca','CRA Cuna del Jiloca','Santa Eulalia del Campo',['Santa Eulalia del Campo','Villafranca del Campo'],'https://cracunadeljiloca.catedu.es/','https://cracunadeljiloca.catedu.es/wp-content/uploads/2021/04/PEC_2015.pdf','En 2015 se integró en él el CRA Alto Jiloca (sede Villafranca del Campo). Verificar localidades actuales.'),
]
SOLO_SEDE=[('arino-alloza','CRA Ariño-Alloza','Ariño'),('goya','CRA Goya','Caminreal'),('martin-del-rio','CRA de Martín del Río','Martín del Río'),('mezquin','CRA del Mezquín','Castelserás'),('palmira-pla','CRA Palmira Plá','Cedrillas'),('pablo-antonio-crespo','CRA Pablo Antonio Crespo','Aliaga'),('portico-de-aragon','CRA Pórtico de Aragón','Rubielos de Mora'),('regallo','CRA El Regallo','Puigmoreno'),('javalambre','CRA Javalambre','Manzanera')]
CRIE=[('crie-albarracin','CRIE Albarracín','Albarracín',None),('crie-alcorisa','CRIE Alcorisa','Alcorisa',None),('crie-calamocha','CRIE Calamocha','Calamocha','https://crietcalamocha.catedu.es/')]
FUENTE_LISTA='https://educa.aragon.es/documents/20126/315919/2+DATOS+TIEMPOS+ESCOLARES.pdf/3cd6574d-b567-2831-03f1-0d2905c18400?t=1565682702403'
FUENTE_CRIE='https://educa.aragon.es/documents/20126/0/CSVYH3DXIE6JQ190XFIL+RESOLUCI%C3%93N+DEFINITIVA+programa+CRIES.pdf/5eef0f93-f7a3-e89d-4d09-09d6394a4cdd?t=1761203513336'
out=[]
for i,n,s,l,w,f,nt in CRA:
    out.append(dict(id=i,nombre=n,tipo='CRA',sede=s,localidades=l,cursos=CRA_CURSOS,servicios=PEND,info=nt or PEND,web=w,fuente=f,estado='Localidades según la fuente indicada; verificar con el centro'))
for i,n,s in SOLO_SEDE:
    out.append(dict(id=i,nombre=n,tipo='CRA',sede=s,localidades=[s],cursos=CRA_CURSOS,servicios=PEND,info='Existe como CRA de la provincia (listados oficiales de centros). Localidades que lo forman: pendiente de verificar.',web=None,fuente=FUENTE_LISTA,estado='Solo sede confirmada'))
for i,n,s,w in CRIE:
    out.append(dict(id=i,nombre=n,tipo='CRIE',sede=s,localidades=[s],cursos=CRIE_CURSOS,servicios=PEND,info='Centro Rural de Innovación Educativa de Teruel. Albarracín y Alcorisa funcionan desde 1983 y Calamocha desde 1994.',web=w,fuente=FUENTE_CRIE,estado='Confirmado en la resolución del programa CRIE 2025-26'))
# Coordenadas: solo las conocidas con razonable fiabilidad; el resto null.
# aprox:true = estimadas. Ejecuta "python scripts/actualizar_datos.py geocodificar" para fijarlas.
AP={'Albarracín':(40.408,-1.442),'Gea de Albarracín':(40.405,-1.350),'Bronchales':(40.493,-1.536),'Orihuela del Tremedal':(40.570,-1.650),'Calamocha':(40.917,-1.299),'Alcorisa':(40.884,-0.379),'Cantavieja':(40.519,-0.407),'Beceite':(40.841,0.213),'Calaceite':(41.015,0.184),'La Fresneda':(40.946,0.049),'Cretas':(40.904,0.165),'Muniesa':(41.042,-0.788),'Rubielos de Mora':(40.200,-0.620),'Mosqueruela':(40.358,-0.445),'Castellote':(40.787,-0.318),'Aliaga':(40.668,-0.700),'Santa Eulalia del Campo':(40.578,-1.317),'Alfambra':(40.533,-1.022),'La Puebla de Híjar':(41.220,-0.455)}
names=sorted({x for c in out for x in c['localidades']})
loc={}
for n in names:
    if n=='Perales del Alfambra': loc[n]=dict(lat=40.63444,lon=-1.00330,aprox=False)
    elif n in AP: loc[n]=dict(lat=AP[n][0],lon=AP[n][1],aprox=True)
    else: loc[n]=dict(lat=None,lon=None,aprox=True)
loc['Villalba']['buscar']='Villalba Baja'
json.dump(out,open('data/cras.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
json.dump(loc,open('data/localidades.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
json.dump({},open('data/fotos.json','w'))
print(len(out),'centros',len(loc),'localidades',sum(1 for v in loc.values() if v['lat'] is not None),'con coordenadas')
