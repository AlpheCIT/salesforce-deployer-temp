import * as pactum from 'pactum';
import { LoginRequest } from '../../../frontend/src/api';

describe('Authentication API', () => {
  beforeAll(() => {
    pactum.request.setBaseUrl('http://localhost:8000');
  });

  it('should login with valid credentials', async () => {
    const loginRequest: LoginRequest = {
      username: 'user@example.com',
      password: 'password123'
    };

    await pactum.spec()
      .post('/api/v1/auth/login')
      .withJson(loginRequest)
      .expectStatus(200)
      .expectJsonSchema({
        type: 'object',
        required: ['accessToken', 'tokenType'],
        properties: {
          accessToken: { type: 'string' },
          tokenType: { type: 'string' },
          expiresIn: { type: 'number' }
        }
      });
  });

  it('should reject invalid credentials', async () => {
    await pactum.spec()
      .post('/api/v1/auth/login')
      .withJson({
        username: 'invalid@example.com',
        password: 'wrongpassword'
      })
      .expectStatus(401);
  });
});