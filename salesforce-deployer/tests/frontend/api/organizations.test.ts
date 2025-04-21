import pactum from 'pactum';
import { OrganizationRequest } from '../../../frontend/src/api';

describe('Organizations API', () => {
  let authToken: string;

  beforeAll(async () => {
    pactum.request.setBaseUrl('http://localhost:8000');
    
    try {
      // Get auth token for subsequent requests
      const response = await pactum.spec()
        .post('/api/v1/auth/login')
        .withJson({
          username: 'user@example.com',
          password: 'password123'
        })
        .returns('accessToken');
        
      authToken = response;
    } catch (error) {
      console.error('Error in beforeAll:', error);
      // Use a dummy token for tests if authentication fails
      authToken = 'dummy-token-for-tests';
    }
  });

  it('should list all organizations', async () => {
    await pactum.spec()
      .get('/api/v1/organizations')
      .withBearerToken(authToken)
      .expectStatus(200)
      .expectJsonSchema({
        type: 'array',
        items: {
          type: 'object',
          required: ['id', 'name', 'type', 'instanceUrl'],
        }
      });
  });
  
  it('should get organization by ID', async () => {
    const orgId = '123e4567-e89b-12d3-a456-426614174000';
    
    await pactum.spec()
      .get(`/api/v1/organizations/${orgId}`)
      .withBearerToken(authToken)
      .expectStatus(200)
      .expectJsonSchema({
        type: 'object',
        required: ['id', 'name', 'type', 'instanceUrl'],
      });
  });
  
  it('should add new organization', async () => {
    const orgRequest: OrganizationRequest = {
      name: 'Test Organization',
      type: 'Sandbox',
      instanceUrl: 'https://test-sandbox.my.salesforce.com',
      username: 'test@example.com',
      password: 'password123',
      securityToken: 'TOKEN123'
    };

    await pactum.spec()
      .post('/api/v1/organizations')
      .withBearerToken(authToken)
      .withJson(orgRequest)
      .expectStatus(201)
      .expectJsonSchema({
        type: 'object',
        required: ['id', 'name', 'type', 'instanceUrl'],
      });
  });
  
  it('should update an organization', async () => {
    const orgId = '123e4567-e89b-12d3-a456-426614174000';
    const updateRequest: OrganizationRequest = {
      name: 'Updated Organization',
      type: 'Production',
      instanceUrl: 'https://prod.my.salesforce.com',
      username: 'updated@example.com',
      password: 'newpassword123',
      securityToken: 'NEWTOKEN123'
    };
    
    await pactum.spec()
      .put(`/api/v1/organizations/${orgId}`)
      .withBearerToken(authToken)
      .withJson(updateRequest)
      .expectStatus(200);
  });
  
  it('should delete an organization', async () => {
    const orgId = '123e4567-e89b-12d3-a456-426614174000';
    
    await pactum.spec()
      .delete(`/api/v1/organizations/${orgId}`)
      .withBearerToken(authToken)
      .expectStatus(204);
  });
});