"""Smoke tests for swing.status views and packaging."""

# Import | Future
from __future__ import annotations

# Import | Standard Library
from importlib import import_module
import json
import sys
from types import ModuleType, SimpleNamespace

from django.db.utils import OperationalError
from django.http import HttpResponse
from django.test import RequestFactory


def _json(response):
    return json.loads(response.content)


def test_app_config_metadata() -> None:
    apps_module = import_module("swing.status.apps")

    assert apps_module.SwingStatusConfig.name == "swing.status"
    assert apps_module.SwingStatusConfig.label == "swing_status"


def test_main_entrypoint_calls_django(monkeypatch) -> None:
    main_module = import_module("swing.status.__main__")
    called = {"value": False}

    def fake_execute() -> None:
        called["value"] = True

    monkeypatch.setattr(main_module, "execute_from_command_line", fake_execute)

    main_module.main()

    assert called["value"] is True


def test_status_dashboard_renders_expected_template(monkeypatch) -> None:
    module = import_module("swing.status.views.view_status_dashboard")
    request = RequestFactory().get("/status/dashboard/")

    def fake_render(_request, template_name):
        return HttpResponse(template_name)

    monkeypatch.setattr(module, "render", fake_render)

    response = module.status_dashboard(request)

    assert response.content.decode() == "swing/status/status.html"


def test_database_status_reports_ok(monkeypatch) -> None:
    module = import_module("swing.status.views.view_status_database")
    request = RequestFactory().get("/status/database/")

    class FakeConnection:
        def cursor(self):
            return object()

    monkeypatch.setattr(module, "connections", {"default": FakeConnection()})

    response = module.database_status(request)

    assert _json(response)["status"] == "OK"


def test_database_status_reports_error(monkeypatch) -> None:
    module = import_module("swing.status.views.view_status_database")
    request = RequestFactory().get("/status/database/")

    class FakeConnection:
        def cursor(self):
            raise OperationalError()

    monkeypatch.setattr(module, "connections", {"default": FakeConnection()})

    response = module.database_status(request)

    assert _json(response)["status"] == "ERROR"


def test_celery_status_reports_ok(monkeypatch) -> None:
    module = import_module("swing.status.views.view_status_celery")
    request = RequestFactory().get("/status/celery/")
    celery_module = ModuleType("celery")
    celery_module.current_app = object()
    celery_result_module = ModuleType("celery.result")

    class FakeAsyncResult:
        def __init__(self, task_id, app):
            self.task_id = task_id
            self.app = app

        def ready(self):
            return True

    celery_result_module.AsyncResult = FakeAsyncResult
    monkeypatch.setitem(sys.modules, "celery", celery_module)
    monkeypatch.setitem(sys.modules, "celery.result", celery_result_module)

    response = module.celery_status(request)

    assert _json(response)["status"] == "OK"


def test_redis_status_reports_ok(monkeypatch, settings) -> None:
    module = import_module("swing.status.views.view_status_redis")
    request = RequestFactory().get("/status/redis/")
    redis_module = ModuleType("redis")

    class FakeRedisClient:
        def __init__(self, **_kwargs):
            pass

        def ping(self):
            return True

    redis_module.StrictRedis = FakeRedisClient
    redis_module.ConnectionError = RuntimeError
    monkeypatch.setitem(sys.modules, "redis", redis_module)
    settings.REDIS_HOST = "localhost"
    settings.REDIS_PORT = 6379

    response = module.redis_status(request)

    assert _json(response)["status"] == "OK"


def test_elasticsearch_status_reports_ok(monkeypatch, settings) -> None:
    module = import_module("swing.status.views.view_status_elasticsearch")
    request = RequestFactory().get("/status/elasticsearch/")
    elasticsearch_module = ModuleType("elasticsearch")

    class FakeElasticsearch:
        def __init__(self, _hosts):
            pass

        def ping(self):
            return True

    elasticsearch_module.Elasticsearch = FakeElasticsearch
    monkeypatch.setitem(sys.modules, "elasticsearch", elasticsearch_module)
    settings.ELASTICSEARCH_HOST = "localhost"
    settings.ELASTICSEARCH_PORT = 9200

    response = module.elasticsearch_status(request)

    assert _json(response)["status"] == "OK"


def test_external_api_status_reports_ok(monkeypatch) -> None:
    module = import_module("swing.status.views.view_status_external_api")
    request = RequestFactory().get("/status/external-api/")
    requests_module = ModuleType("requests")
    requests_module.exceptions = SimpleNamespace(RequestException=RuntimeError)

    class FakeResponse:
        status_code = 200

    def fake_get(_url, timeout):
        assert timeout == 5
        return FakeResponse()

    requests_module.get = fake_get
    monkeypatch.setitem(sys.modules, "requests", requests_module)

    response = module.external_api_status(request)

    assert _json(response)["status"] == "OK"


def test_memory_usage_status_reports_ok(monkeypatch) -> None:
    module = import_module("swing.status.views.view_status_memory_usage")
    request = RequestFactory().get("/status/memory-usage/")
    psutil_module = ModuleType("psutil")
    psutil_module.virtual_memory = lambda: SimpleNamespace(available=2 * (1024**3))
    monkeypatch.setitem(sys.modules, "psutil", psutil_module)

    response = module.memory_usage_status(request)

    assert _json(response)["status"] == "OK"


def test_cpu_load_status_reports_ok(monkeypatch) -> None:
    module = import_module("swing.status.views.view_status_cpu_load")
    request = RequestFactory().get("/status/cpu-load/")
    psutil_module = ModuleType("psutil")
    psutil_module.cpu_percent = lambda interval: 5
    monkeypatch.setitem(sys.modules, "psutil", psutil_module)

    response = module.cpu_load_status(request)

    assert _json(response)["status"] == "OK"


def test_disk_space_status_reports_ok(monkeypatch) -> None:
    module = import_module("swing.status.views.view_status_disk_space")
    request = RequestFactory().get("/status/disk-space/")
    monkeypatch.setattr(
        module.shutil, "disk_usage", lambda _path: (100, 50, 10 * (2**30))
    )

    response = module.disk_space_status(request)

    assert _json(response)["status"] == "OK"


def test_settings_check_reports_ok() -> None:
    module = import_module("swing.status.views.view_status_settings")
    request = RequestFactory().get("/status/settings/")

    response = module.settings_check(request)

    assert _json(response)["status"] == "OK"


def test_email_server_status_reports_ok(monkeypatch) -> None:
    module = import_module("swing.status.views.view_status_email_server")
    request = RequestFactory().get("/status/email-server/")
    monkeypatch.setattr(module, "send_mail", lambda *args, **kwargs: 1)

    response = module.email_server_status(request)

    assert _json(response)["status"] == "OK"
