def create_index(es_client_object):
    es_client_object.indices.create(index="haberler")


def insert_document(es_client_object, nd):
    try:
        nd["date"] = nd["date"].isoformat()
    except Exception as e:
        print("Error on date parsing for elasticsearch, ignore inserting %s" % str(e))
        return

    es_client_object.index(
        index="haberler",
        document=nd
    )
