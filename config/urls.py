"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from api.views import chatterfy_webhook, hello_world, register, login, get_countries, transactions_list, transaction_create, update_profile, historial_pagos_list, historial_pagos_create, get_user_info, refresh_token, use_first_bonus, telegram_webhook, test_webhook, update_deposit, lookup_user_by_id, change_stage, payment_callback, debug_transactions, test_payment_callback, verify_email, resend_verification_email, cleanup_payment


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/hello/", hello_world, name="hello_world"),
    path("chatterfy-webhook/", chatterfy_webhook, name="chatterfy_webhook"),
    path("api/register/", register, name="register"),
    path("api/login/", login, name="login"),
    path("api/countries/", get_countries, name="get_countries"),
    path("api/transactions/", transactions_list, name="transactions_list"),
    path("api/transactions/create/", transaction_create, name="transaction_create"),
    path("api/profile/update/", update_profile, name="update_profile"),
    path("api/historial_pagos/", historial_pagos_list, name="historial_pagos_list"),
    path("api/historial_pagos/create/", historial_pagos_create, name="historial_pagos_create"),
    path("api/user/info/", get_user_info, name="get_user_info"),
    path("api/user/use-first-bonus/", use_first_bonus, name="use_first_bonus"),
    path("api/user/deposit/", update_deposit, name="update_deposit"),
    path("api/user/lookup/<str:user_id>/", lookup_user_by_id, name="lookup_user_by_id"),
    path("api/token/refresh/", refresh_token, name="refresh_token"),
    path("api/telegram-webhook/", telegram_webhook, name="telegram_webhook"),
    path("api/test-webhook/", test_webhook, name="test_webhook"),
    path("api/user/change-stage/", change_stage, name="change_stage"),
    path("api/payment-callback/", payment_callback, name="payment_callback"),
    path("api/debug/transactions/", debug_transactions, name="debug_transactions"),
    path("api/test/payment-callback/", test_payment_callback, name="test_payment_callback"),
    path("api/verify-email/<str:token>/", verify_email, name="verify_email"),
    path("api/resend-verification-email/", resend_verification_email, name="resend_verification_email"),
    path("api/cleanup-payment/", cleanup_payment, name="cleanup_payment"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
