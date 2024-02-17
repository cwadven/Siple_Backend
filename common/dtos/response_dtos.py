from pydantic import (
    BaseModel,
    Field,
)


class HealthCheckResponse(BaseModel):
    message: str = Field(...)
