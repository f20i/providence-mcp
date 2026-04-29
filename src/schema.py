from pydantic import BaseModel

class BrowserConnectionSchema(BaseModel):
    cdp_url: str

class BrowserEndpointSchema(BaseModel):
    status: str
    connection: BrowserConnectionSchema | None = None

class ProfileSchema(BaseModel):
    id: str
    name: str
    description: str | None = None

class BrowserSchema(BaseModel):
    id: str
    name: str
    description: str | None = None
    profile: ProfileSchema
    browser_endpoint: BrowserEndpointSchema | None = None

class BrowserListSchema(BaseModel):
    items: list[BrowserSchema]
    total: int
    
class ProfileListSchema(BaseModel):
    items: list[ProfileSchema]
    total: int