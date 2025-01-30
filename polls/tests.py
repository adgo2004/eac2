from django.test import TestCase

# Create your tests here.

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
class MySeleniumTests(StaticLiveServerTestCase):
    # carregar una BD de test
    #fixtures = ['testdb.json',]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        # tanquem browser
        # comentar la propera línia si volem veure el resultat de l'execució al navegador
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):

	# Crearem un super usuari amb el que farem les proves:
        User.objects.create_superuser(username='isard',password='pirineus',email='isard@isard.com')

        # anem directament a la pàgina d'accés a l'admin panel:
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))

        # Comprovem que el títol de la pàgina és el que esperem:
        self.assertEqual(self.selenium.title , "Log in | Django site admin" )

        # Introduïm dades de login i cliquem el botó "Log in" per entrar:
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('isard')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()

	# Ens anem a l'adició del nou usuari:
        self.selenium.find_element(By.XPATH,'//a[@href="/admin/auth/user/add/"]').click()

        # Introduim dades de login i cliquem el botó "SAVE" per la creació de l'usuari:
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('super')
        password_input = self.selenium.find_element(By.NAME,"password1")
        password_input.send_keys('Super2025.')
        password_input = self.selenium.find_element(By.NAME,"password2")
        password_input.send_keys('Super2025.')
        self.selenium.find_element(By.XPATH,'//input[@value="Save"]').click()

        # Permisos de Staff:
        self.selenium.find_element(By.NAME,"is_staff").click()

	# Permisos de crear i visualitzar usuaris:
        self.selenium.find_element(By.XPATH,'//option[@value="21"]').click()
        self.selenium.find_element(By.ID,"id_user_permissions_add_link").click()

        self.selenium.find_element(By.XPATH,'//option[@value="22"]').click()
        self.selenium.find_element(By.ID,"id_user_permissions_add_link").click()

        self.selenium.find_element(By.XPATH,'//option[@value="24"]').click()
        self.selenium.find_element(By.ID,"id_user_permissions_add_link").click()

        self.selenium.find_element(By.XPATH,'//input[@value="Save"]').click()

        # --------------------------> VERIFICACIONS <--------------------------:

	# Creació d'usuaris amb l'usuari Staff:
        self.selenium.find_element(By.XPATH, "//button[text()='Log out']").click()
        self.selenium.find_element(By.XPATH,'//a[@href="/admin/"]').click()

        # Introduïm dades de login i cliquem el botó "Log in" per entrar:
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('super')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('Super2025.')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()

	# Veiem si pot crear usuaris:
        self.selenium.find_element(By.XPATH,'//a[@href="/admin/auth/user/add/"]').click()
        self.assertEqual(self.selenium.title , "Add user | Django site admin")

	# Veiem si no podem crear questions:
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/polls/question/add/'))
        self.assertEqual(self.selenium.title , "403 Forbidden")
