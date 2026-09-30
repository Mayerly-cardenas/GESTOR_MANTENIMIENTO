from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages.storage.cookie import CookieStorage
from django.test import RequestFactory, TestCase, override_settings
from PIL import Image

from .models import MAX_IMAGE_SIZE, Motor, validate_image_size
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


class MotorImagePolicyTest(TestCase):
	def test_rejects_image_larger_than_100_mb(self):
		with self.assertRaises(ValidationError):
			validate_image_size(SimpleNamespace(size=MAX_IMAGE_SIZE + 1))

	def test_compresses_uploaded_jpeg(self):
		image_data = BytesIO()
		Image.new("RGB", (800, 800), (180, 50, 20)).save(image_data, format="JPEG", quality=100)
		original_size = image_data.tell()

		with TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
			motor = Motor.objects.create(
				identification_no="M-IMAGE-001",
				equipment_description="Motor de prueba",
				imagen_motor=SimpleUploadedFile(
					"motor.jpg", image_data.getvalue(), content_type="image/jpeg",
				),
			)
			self.assertLess(motor.imagen_motor.size, original_size)
			with Image.open(Path(motor.imagen_motor.path)) as saved_image:
				self.assertEqual(saved_image.size, (800, 800))
