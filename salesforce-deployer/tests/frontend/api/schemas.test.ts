import pactum from 'pactum';
import { SchemaExtractionRequest, SchemaComparisonRequest } from '../../../frontend/src/api';

describe('Schemas API', () => {
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

  it('should extract schema from Salesforce org', async () => {
    const extractRequest: SchemaExtractionRequest = {
      organizationId: '123e4567-e89b-12d3-a456-426614174000',
      components: ['Objects', 'Fields', 'Workflows']
    };

    await pactum.spec()
      .post('/api/v1/schemas/extract')
      .withBearerToken(authToken)
      .withJson(extractRequest)
      .expectStatus(200)
      .expectJsonSchema({
        type: 'object',
        required: ['schemaId', 'status'],
        properties: {
          schemaId: { type: 'string' },
          status: { type: 'string' }
        }
      });
  });

  it('should get schema by ID', async () => {
    const schemaId = '123e4567-e89b-12d3-a456-426614174000';
    
    await pactum.spec()
      .get(`/api/v1/schemas/${schemaId}`)
      .withBearerToken(authToken)
      .expectStatus(200)
      .expectJsonSchema({
        type: 'object',
        required: ['id', 'name', 'createdAt', 'components'],
      });
  });

  it('should compare schemas between environments', async () => {
    const comparisonRequest: SchemaComparisonRequest = {
      sourceSchemaId: '123e4567-e89b-12d3-a456-426614174000',
      targetSchemaId: '223e4567-e89b-12d3-a456-426614174001',
      components: ['Objects', 'Fields']
    };

    await pactum.spec()
      .post('/api/v1/schemas/compare')
      .withBearerToken(authToken)
      .withJson(comparisonRequest)
      .expectStatus(200)
      .expectJsonSchema({
        type: 'object',
        required: ['differences'],
      });
  });
  
  it('should list all schemas', async () => {
    await pactum.spec()
      .get('/api/v1/schemas')
      .withBearerToken(authToken)
      .expectStatus(200)
      .expectJsonSchema({
        type: 'array',
        items: {
          type: 'object',
          required: ['id', 'name', 'createdAt'],
        }
      });
  });
});