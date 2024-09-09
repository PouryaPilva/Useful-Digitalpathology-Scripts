import geojson
from tqdm import tqdm
import numpy as np
import os


type_mapping = {
    0: "nolabel",
    1: "neoplastic",
    2: "inflammatory",
    3: "connective",
    4: "necrosis",
    5: "non-neoplastic",
}



def write_geojson(instances,typel, outname,descriptions=None):
    colors = [[0, 0, 0],[150, 200, 150],[255, 0, 0],[0, 255, 0],[0, 0, 255],[255, 255, 0]]
    collection = []
    counter = 0
    for ik,key in enumerate(instances.keys()):
        for contour in instances[key]:
            Nuclei_type = typel[counter]
            

            dd = \
            {
                'type':'Feature',
                'geometry': {
                    'type':'Polygon',
                    'coordinates': np.array(contour)[None,:,:].tolist()
                    },

                'properties':{
                    'classification':{'name': type_mapping[Nuclei_type], 'color': colors[Nuclei_type]},
                    }
            }
            counter = counter + 1
            # if counter >20000:
            #     continue
            collection.append(dd)
    feature_collection = geojson.FeatureCollection(collection)

    with open(outname, 'w') as f:
        geojson.dump(feature_collection, f, indent=2, separators=(',', ': '))



directory = os.listdir("/homeStor1/json/")
for file in directory :        

    annotation_geojson_file = open("/homeStor1/json/" + file)
    collection = geojson.load(annotation_geojson_file)

    keys = list(collection['nuc'].keys())
    conts = []
    typel = []
    ## if 40 x 


    for k in tqdm(keys):
        cont = collection['nuc'][k]['contour']
        typel.append(collection['nuc'][k]['type'])
        ## 20x
    # cont = np.array(cont)/2
        ## 40x
        cont = np.array(cont)[::3]
        if "C3L" in file:
            cont = cont/2 
        # cont = cont.astype(int)
        cont = cont.tolist()
        cont.append(cont[0])
        conts.append(cont)
        
    instances = {'nuc':conts}
    write_geojson(instances, typel ,"/homeStor1/geojson/" + file.replace("json","geojson"),descriptions=None)
