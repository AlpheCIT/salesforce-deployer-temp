import pactum from 'pactum';
import { SchemaValidationRequest } from '../../../frontend/src/api';

describe('Validation API', () => {
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

  it('should validate a schema against an organization', async () => {
    const validationRequest: SchemaValidationRequest = {
      schemaId: '123e4567-e89b-12d3-a456-426614174000',
      targetOrganizationId: '223e4567-e89b-12d3-a456-426614174001',
      components: ['Objects', 'Fields']
    };

    await pactum.spec()
      .post('/api/v1/validation/schema')
      .withBearerToken(authToken)
      .withJson(validationRequest)
      .expectStatus(200)
      .expectJsonSchema({
        type: 'object',
        required: ['isValid', 'validationResults'],
        properties: {
          isValid: { type: 'boolean' },
          validationResults: { 
            type: 'array',
            items: { 
              type: 'object',
              required: ['component', 'valid', 'errors']
            }
          }
        }
      });
  });
  
  it('should validate deployability of components', async () => {
    const orgId = '123e4567-e89b-12d3-a456-426614174000';
    const components = [
      { type: 'CustomObject', name: 'Account' },
      { type: 'CustomField', name: 'Account.CustomField__c' }
    ];

    await pactum.spec()
      .post('/api/v1/validation/deployability')
      .withBearerToken(authToken)
      .withJson({
        organizationId: orgId,
        components: components
      })
      .expectStatus(200)
      .expectJsonSchema({
        type: 'object',
        required: ['deployable', 'results'],
      });
  });
});