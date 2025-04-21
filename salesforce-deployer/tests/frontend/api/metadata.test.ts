import pactum from 'pactum';

describe('Metadata API', () => {
  let authToken: string;

  beforeAll(async () => {
    pactum.request.setBaseUrl('http://localhost:8000');
    
    // Get auth token for subsequent requests
    const response = await pactum.spec()
      .post('/api/v1/auth/login')
      .withJson({
        username: 'user@example.com',
        password: 'password123'
      })
      .returns('accessToken');
      
    authToken = response;
  });

  it('should list available metadata types', async () => {
    const orgId = '123e4567-e89b-12d3-a456-426614174000';
    
    await pactum.spec()
      .get(`/api/v1/metadata/types?organizationId=${orgId}`)
      .withBearerToken(authToken)
      .expectStatus(200)
      .expectJsonSchema({
        type: 'array',
        items: {
          type: 'object',
          required: ['name', 'xmlName', 'directoryName'],
        }
      });
  });

  it('should list metadata components of a specific type', async () => {
    const orgId = '123e4567-e89b-12d3-a456-426614174000';
    const metadataType = 'CustomObject';
    
    await pactum.spec()
      .get(`/api/v1/metadata/components?organizationId=${orgId}&type=${metadataType}`)
      .withBearerToken(authToken)
      .expectStatus(200)
      .expectJsonSchema({
        type: 'array',
        items: {
          type: 'object',
          required: ['name', 'type'],
        }
      });
  });
  
  it('should get metadata component details', async () => {
    const orgId = '123e4567-e89b-12d3-a456-426614174000';
    const metadataType = 'CustomObject';
    const componentName = 'Account';
    
    await pactum.spec()
      .get(`/api/v1/metadata/components/${metadataType}/${componentName}?organizationId=${orgId}`)
      .withBearerToken(authToken)
      .expectStatus(200)
      .expectJsonSchema({
        type: 'object',
        required: ['name', 'type'],
      });
  });
});