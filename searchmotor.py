import os
from model import Customer

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import ( 
    ComplexField, 
    CorsOptions, 
    SearchIndex, 
    ScoringProfile, 
    SearchFieldDataType, 
    SimpleField, 
    SearchableField 
)

index_name = "kund01"
# Get the service endpoint and API key from the environment
endpoint = "https://kund.search.windows.net"
key = "554B501BA895D8AB0BF996F882BF9F63"

# Create a client
credential = AzureKeyCredential(key)


client = SearchClient(endpoint=endpoint,
                      index_name=index_name,
                      credential=credential)

def createIndex():
    searchIndexClient = SearchIndexClient(endpoint=endpoint,
                        index_name=index_name,
                        credential=credential)

    fields = [
            SearchableField(name="Id", type=SearchFieldDataType.String, sortable=True, key=True),
            SearchableField(name="GivenName", type=SearchFieldDataType.String, sortable=True),
            SearchableField(name="Surname", type=SearchFieldDataType.String,sortable=True),
            SearchableField(name="Streetaddress", type=SearchFieldDataType.String,sortable=True),
            SearchableField(name="City", type=SearchFieldDataType.String,sortable=True),
            SearchableField(name="Country", type=SearchFieldDataType.String,sortable=True),
            SearchableField(name="EmailAddress", type=SearchFieldDataType.String,sortable=True),
            SearchableField(name="Telephone", type=SearchFieldDataType.String,sortable=True),
            SearchableField(name="Birthday", type=SearchFieldDataType.String,sortable=True)
        ]
    cors_options = CorsOptions(allowed_origins=["*"], max_age_in_seconds=60)
    scoring_profiles = []

    index = SearchIndex(
        name=index_name,
        fields=fields,
        scoring_profiles=scoring_profiles,
        cors_options=cors_options)

    result = searchIndexClient.create_index(index)                      


def addDocuments():

    docs = []
    for kund in Customer.query.all():
        d = {
               "Id" : int(kund.Id),
               "GivenName": kund.GivenName,
               "Surname": kund.Surname,
               "Streetaddress": kund.Streetaddress,
               "City": kund.City,
               "Country": kund.Country,
               "EmailAddress": kund.EmailAddress,
               "Telephone": str(kund.Telephone),
               "Birthday": str(kund.Birthday)
        }
        docs.append(d)
    result = client.upload_documents(documents=docs)
    

