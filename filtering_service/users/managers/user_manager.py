from django.contrib.auth.base_user import BaseUserManager
from typing import Optional, Any
from django.db.transaction import atomic
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser
import logging
from django.db import IntegrityError

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    def _create_user(self, email: str, password: Optional[str] = None, **extra_fields: Any) -> AbstractBaseUser:
        """
        Creates and saves a User with the given email and password.
        :param email:
        :param password:
        :param extra_fields:
        :return user
        """
        if not email:
            logger.error("Попытка создать пользователя без email")
            raise ValueError("Users must have an email address")

        if not password:
            logger.error("Попытка создать пользователя без пароля")
            raise ValueError("Users must have a password")

        try:
            validate_email(email)
        except ValidationError:
            logger.error(f"Попытка создать пользоветеля с неверным форматом email: {email}")
            raise ValueError("Invalid email format")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        try:
            user.save(using=self._db)
            logger.info(f"Создан пользователь: {email}")
        except IntegrityError as e:
            logger.error(f"Ошибка при создании пользователя: {email} - {e}")
            raise ValueError("A user with this email already exists") from e

        return user

    @atomic
    def create_user(self, email: str, password: Optional[str] = None, **extra_fields: Any) -> AbstractBaseUser:
        """
        Creates and saves a User with the given email and password.
        :param email:
        :param password:
        :param extra_fields:
        :return:
        """
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_blocked", False)
        extra_fields.setdefault("is_verified", False)

        # предотвращаем переопределение ключевых полей при создании пользователя
        for field in ['is_active', 'is_superuser', 'is_staff', ]:
            if field in extra_fields:
                logger.warning(f"Переопределение поля {field} при создании обычного пользователя")
                extra_fields.pop(field)

        return self._create_user(email, password, **extra_fields)

    @atomic
    def create_superuser(self, email: str, password: Optional[str] = None, **extra_fields: Any) -> AbstractBaseUser:
        """
        Creates and saves a superuser with the given email and password.
        :param email:
        :param password:
        :param extra_fields:
        :return:
        """
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_blocked", False)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get('is_superuser') is not True:
            logger.error("Суперпользователь должен иметь is_superuser=True.")
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get('is_staff') is not True:
            logger.error("Суперпользователь должен иметь is_staff=True.")
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_active') is not True:
            logger.error("Суперпользователь должен иметь is_active=True.")
            raise ValueError("Superuser must have is_active=True.")

        return self._create_user(email, password, **extra_fields)