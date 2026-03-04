from olcf_s3m_api.streaming import StreamingService

def test_streaming_init(client):
    service = StreamingService("rabbitmq", client)
    assert service._service_name == "rabbitmq"
    assert service._client == client
