from typing import Optional

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration


def init_sentry(dsn: str, environment: str = "development") -> Optional[None]:
    if not dsn:
        return None

    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        integrations=[FastApiIntegration(), StarletteIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=False,
    )
    return None
