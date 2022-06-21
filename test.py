from app import app 
import unittest

class TestApiUsuarios(unittest.TestCase):

    def test_1_usuarios_status(self):
     tester = app.test_client(self)
     response = tester.get("/usuarios")
     status_code = response.status_code
     self.assertEqual(status_code,200)
     print('test_1_usuarios_status completado')

    def test_1_usuarios_return(self):
     tester = app.test_client(self)
     response = tester.get("/usuarios")
     self.assertEqual(response.content_type,"application/json")
     print('test_1_usuarios_return completado')


    def test_1_usuarios_data(self):
     tester = app.test_client(self)
     response = tester.get("/usuarios")
     self.assertTrue(b'usuario',response.data)
     print('test_1_usuarios_data completado')


if __name__ == '__main__':
 unittest.main()
   