import * as pactum from 'pactum';
import { DeploymentRequest } from '../../../frontend/src/api';

describe('Deployment API', () => {
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
      authToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiaWF0IjoxNTE2MjM5MDIyfQ.test';
    }
  });

  it('should create deployment plan', async () => {
    const deploymentRequest: DeploymentRequest = {
      sourceSchemaId: '123e4567-e89b-12d3-a456-426614174000',
      targetOrganizationId: '223e4567-e89b-12d3-a456-426614174001',
      components: ['Objects', 'Fields', 'Workflows']
    };

    await pactum.spec()
      .post('/api/v1/deployments')
      .withBearerToken(authToken)
      .withJson(deploymentRequest)
      .expectStatus(201)
      .expectJsonSchema({
        type: 'object',
        required: ['id', 'status'],
      });
  });

  it('should list all deployments', async () => {
    await pactum.spec()
      .get('/api/v1/deployments')
      .withBearerToken(authToken)
      .expectStatus(200)
      .expectJsonSchema({
        type: 'array',
        items: {
          type: 'object',
          required: ['id', 'status', 'createdAt'],
        }
      });
  });

  it('should get deployment status', async () => {
    const deploymentId = '123e4567-e89b-12d3-a456-426614174002';

    await pactum.spec()
      .get(`/api/v1/deployments/${deploymentId}`)
      .withBearerToken(authToken)
      .expectStatus(200)
      .expectJsonSchema({
        type: 'object',
        required: ['id', 'status', 'createdAt'],
      });
  });
  
  it('should cancel a deployment', async () => {
    const deploymentId = '123e4567-e89b-12d3-a456-426614174002';
    
    await pactum.spec()
      .delete(`/api/v1/deployments/${deploymentId}`)
      .withBearerToken(authToken)
      .expectStatus(200)
      .expectJsonSchema({
        type: 'object',
        required: ['id', 'status'],
        properties: {
          status: { enum: ['CANCELLED'] }
        }
      });
  });
});