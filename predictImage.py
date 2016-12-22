from clarifai.rest import ClarifaiApp

capp = ClarifaiApp("ntSR-1T-q-UpmSHFrWlqfDB5MmB7Fji3dpQPbsDW", "iB16rYPAMEiXJ8E2DiHKAuJQk0SOjZMcGDJ5s_hi")

# get the general model
model = capp.models.get('general-v1.3')

def get_tags(filename):
    # predict with the model
    # model.predict_by_url(url='https://samples.clarifai.com/metro-north.jpg')
    search_results = model.predict_by_url(filename)

    response = []

    for concept in search_results['outputs'][0]['data']['concepts']:
        response.append(concept['name'])

    return response