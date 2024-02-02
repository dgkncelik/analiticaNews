def create_index(es_client_object):
    es_client_object.indices.create(index="haberler")


def insert_document(es_client_object, nd):
    nd["date"] = nd["date"].isoformat()
    es_client_object.index(
        index="haberler",
        document=nd
    )