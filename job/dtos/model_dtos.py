from pydantic import (
    BaseModel,
    Field,
)


class ProjectJobAvailabilities(BaseModel):
    id: int = Field(..., description='Job Id')
    display_name: str = Field(..., description='Display Name')
    is_available: str = Field(..., description='Is Available')
