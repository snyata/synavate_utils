def access_secret_version(secret_version_id):
  client = secretmanager.SecretManagerServiceClient()
  response = client.access_secret_version(name=secret_version_id)
  return response.payload.data.decode('UTF-8')