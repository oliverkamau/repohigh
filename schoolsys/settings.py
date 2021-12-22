"""
Django settings for schoolsys project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
import os

from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ls3*5$kwz$)_a!n@8h3zqt#aqq3#$s_ig)-+43sw_gio9=vab9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []



INSTALLED_APPS = [
    'rest_framework',
    'localities.apps.StudentsConfig',
    'setups.apps.SetupsConfig',
    'setups.academics.apps.AcademicsConfig',
    'staff.apps.StaffConfig',
    'staff.teachers.apps.TeachersConfig',
    'useradmin.apps.UseradminConfig',
    'useradmin.users.apps.UsersConfig',
    'setups.academics.classes.apps.ClassesConfig',
    'setups.academics.termdates.apps.TermdatesConfig',
    'studentmanager.apps.StudentmanagerConfig',
    'studentmanager.parents.apps.ParentsConfig',
    'studentmanager.parents.proffessions.apps.ProffessionsConfig',
    'studentmanager.student.apps.StudentConfig',
    'login.apps.LoginConfig',
    'setups.academics.documents.apps.DocumentsConfig',
    'setups.academics.documents.studentdocuments.apps.StudentdocumentsConfig',
    'setups.academics.campuses.apps.CampusesConfig',
    'setups.academics.denominations.apps.DenominationsConfig',
    'setups.academics.dorms.apps.DormsConfig',
    'setups.academics.sources.apps.SourcesConfig',
    'setups.academics.healthconditions.apps.HealthconditionsConfig',
    'setups.academics.studentstatus.apps.StudentstatusConfig',
    'setups.academics.years.apps.YearsConfig',
    'setups.academics.subjects.apps.SubjectsConfig',
    'feemanager.apps.FeemanagerConfig',
    'feemanager.feesetup.apps.FeesetupConfig',
    'feemanager.feesetup.feecategories.apps.FeecategoriesConfig',
    'studentmanager.studentsubjects.apps.StudentsubjectsConfig',
    'setups.academics.departments.apps.DepartmentsConfig',
    'setups.academics.responsibilities.apps.ResponsibilitiesConfig',
    'staff.teachersubjects.apps.TeachersubjectsConfig',
    'exams.apps.ExamsConfig',
    'exams.registration.apps.RegistrationConfig',
    'exams.examtype.apps.ExamtypeConfig',
    'setups.academics.gradingsystem.apps.GradingsystemConfig',
    'exams.processing.apps.ProcessingConfig',
    'setups.academics.gradingschemes.apps.GradingschemesConfig',
    'setups.accounts.apps.AccountsConfig',
    'setups.accounts.standardcharges.apps.StandardchargesConfig',
    'feemanager.feesetup.feegroups.apps.FeegroupsConfig',
    'feemanager.feesetup.feestructure.apps.FeestructureConfig',
    'feemanager.feesetup.feestructuredetails.apps.FeestructuredetailsConfig',
    'feemanager.managebalances.apps.ManagebalancesConfig',
    'feemanager.managebalances.singleinvoicing.apps.SingleinvoicingConfig',
    'feemanager.managebalances.bulkinvoicing.apps.BulkinvoicingConfig',
    'feemanager.managebalances.invoicedetails.apps.InvoicedetailsConfig',
    'setups.system.apps.SystemConfig',
    'setups.system.invoicesequence.apps.InvoicesequenceConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
    'django_currentuser.middleware.ThreadLocalUserMiddleware'
]
SESSION_EXPIRE_SECONDS = 300
SESSION_TIMEOUT_REDIRECT = '/login/loginpage'
ROOT_URLCONF = 'schoolsys.urls'
LOGIN_URL= '/login/loginpage'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'schoolsys.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'highschool',
        'USER': 'sa',
        'PASSWORD': 'kamau',
        'HOST': 'DESKTOP-AT48DO2\SQLEXPRESS',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
}



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'users.User'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static')
]
STATIC_ROOT = os.path.join(BASE_DIR,'assets');
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
