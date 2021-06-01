from main.models import *
import csv
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def recomendacion_trabajador(servicio_id):
    datos_servicios = pd.read_csv('recomendation_data.csv', low_memory=False)
    tfidf_vector = TfidfVectorizer(stop_words='english')
    datos_servicios['observaciones'] = datos_servicios['observaciones'].fillna('')
    tfidf_matrix = tfidf_vector.fit_transform(datos_servicios['observaciones'])
    sim_matrix = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(datos_servicios.index, index=datos_servicios['id']).drop_duplicates()
    idx = indices[servicio_id]
    sim_scores = list(enumerate(sim_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)    
    sim_scores = sim_scores[1:21]
    servicios_indices = [i[0] for i in sim_scores]
    result="No es posible efectuar la recomendación del trabajador para este servicio"
    for d in datos_servicios['trabajador'].iloc[servicios_indices]:
        if str(d) != "nan":
            result = str(d)
            break
    return result

def datos_recomendacion_trabajador():
    servicios = Servicio.objects.all()
    print("Aprendiendo de los datos...")
    myfile = open('recomendation_data.csv','w')
    writer = csv.writer(myfile, delimiter=',', quotechar='"')
    writer.writerow(["id", "tratamiento", "trabajador", "observaciones"])
    for s in servicios:
        trabajador = s.trabajador
        if s.trabajador == None:
            writer.writerow([s.id, s.solicitudServicio.tratamiento.nombre, "", s.solicitudServicio.observaciones])
        else:
            writer.writerow([s.id, s.solicitudServicio.tratamiento.nombre, s.trabajador.persona.nombreCompleto(), s.solicitudServicio.observaciones])
        myfile.flush() # whenever you want, and/or
    myfile.close()
