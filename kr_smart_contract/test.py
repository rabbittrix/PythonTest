from elasticsearch import Elasticsearch

def test_elasticsearch_connection():
    try:
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        if es.ping():
            print("Elasticsearch está acessível!")
        else:
            print("Não foi possível conectar ao Elasticsearch.")
    except Exception as e:
        print(f"Erro ao conectar ao Elasticsearch: {e}")

test_elasticsearch_connection()
