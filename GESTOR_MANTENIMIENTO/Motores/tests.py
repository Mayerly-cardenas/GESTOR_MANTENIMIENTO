from django.contrib.auth import get_user_model
from django.contrib.messages.storage.cookie import CookieStorage
from django.test import RequestFactory, TestCase

from .models import Motor
from .views import MotorUpdateView


class MotorAuditTest(TestCase):
	def test_update_records_authenticated_user_and_timestamp(self):
		user = get_user_model().objects.create_user(username="tecnico", password="clave-segura")
		motor = Motor.objects.create(identification_no="M-001", equipment_description="Motor de prueba")
		previous_updated_at = motor.updated_at

		form = type(
			"MotorFormStub",
			(),
			{"instance": motor, "save": lambda self: self.instance},
		)()
		request = RequestFactory().post("/")
		request.user = user
		request._messages = CookieStorage(request)
		view = MotorUpdateView()
		view.request = request

		MotorUpdateView.form_valid(view, form)

		motor.refresh_from_db()
		self.assertEqual(motor.actualizado_por, user)
		self.assertGreater(motor.updated_at, previous_updated_at)
