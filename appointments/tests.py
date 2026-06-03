from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class ProfissionalTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='admin',
            password='123456'
        )

        response = self.client.post(
            '/api/token/',
            {
                'username': 'admin',
                'password': '123456'
            }
        )

        token = response.data['access']

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )

    def test_criar_profissional(self):

        data = {
            "nome_social": "Gabriella Lyra",
            "profissao": "Fisioterapeuta",
            "endereco": "Rua A",
            "contato": "81999999999"
        }

        response = self.client.post(
            '/api/profissionais/',
            data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_listar_profissionais(self):

        response = self.client.get('/api/profissionais/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_criar_profissional_invalido(self):

        data = {
            "nome_social": "A",
            "profissao": "Psicóloga",
            "endereco": "Rua A",
            "contato": "81999999999"
        }

        response = self.client.post(
            '/api/profissionais/',
            data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_atualizar_profissional(self):

        profissional = self.client.post(
            '/api/profissionais/',
            {
                "nome_social": "Maria Silva",
                "profissao": "Psicóloga",
                "endereco": "Rua A",
                "contato": "81999999999"
            },
            format='json'
        )

        profissional_id = profissional.data['id']

        response = self.client.patch(
            f'/api/profissionais/{profissional_id}/',
            {
                "profissao": "Psiquiatra"
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_deletar_profissional(self):

        profissional = self.client.post(
            '/api/profissionais/',
            {
                "nome_social": "Maria Silva",
                "profissao": "Psicóloga",
                "endereco": "Rua A",
                "contato": "81999999999"
            },
            format='json'
        )

        profissional_id = profissional.data['id']

        response = self.client.delete(
            f'/api/profissionais/{profissional_id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )



class ConsultaTests(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='admin',
            password='123456'
        )

        response = self.client.post(
            '/api/token/',
            {
                'username': 'admin',
                'password': '123456'
            }
        )

        token = response.data['access']

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )

        profissional_response = self.client.post(
            '/api/profissionais/',
            {
                "nome_social": "Maria Silva",
                "profissao": "Psicóloga",
                "endereco": "Rua A",
                "contato": "81999999999"
            },
            format='json'
        )

        self.profissional_id = profissional_response.data['id']

    def test_criar_consulta(self):

        response = self.client.post(
            '/api/consultas/',
            {
                "data": "2030-06-10T14:00:00Z",
                "profissional": self.profissional_id
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
    
    def test_listar_consultas(self):

        self.client.post(
            '/api/consultas/',
            {
                "data": "2030-06-10T14:00:00Z",
                "profissional": self.profissional_id
            },
            format='json'
        )

        response = self.client.get(
            '/api/consultas/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
    
    def test_atualizar_consulta(self):

        consulta = self.client.post(
            '/api/consultas/',
            {
                "data": "2030-06-10T14:00:00Z",
                "profissional": self.profissional_id
            },
            format='json'
        )

        consulta_id = consulta.data['id']

        response = self.client.patch(
            f'/api/consultas/{consulta_id}/',
            {
                "data": "2030-06-20T15:00:00Z"
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
            
    def test_deletar_consulta(self):

        consulta = self.client.post(
            '/api/consultas/',
            {
                "data": "2030-06-10T14:00:00Z",
                "profissional": self.profissional_id
            },
            format='json'
        )

        consulta_id = consulta.data['id']

        response = self.client.delete(
            f'/api/consultas/{consulta_id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        
    def test_criar_consulta_data_passada(self):

        response = self.client.post(
            '/api/consultas/',
            {
                "data": "2020-01-01T10:00:00Z",
                "profissional": self.profissional_id
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        
    def test_criar_consulta_profissional_inexistente(self):

        response = self.client.post(
            '/api/consultas/',
            {
                "data": "2030-06-10T14:00:00Z",
                "profissional": 9999
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )