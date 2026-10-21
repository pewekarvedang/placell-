from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.models.skill import SkillCategory

class SkillBase(BaseModel):
    name: str
    category: SkillCategory
    description: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class SkillResponse(SkillBase):
    id: str
    model_config = ConfigDict(from_attributes=True)

class StudentSkillItem(BaseModel):
    skill_id: str
    skill_name: str
    category: SkillCategory
    proficiency_level: str

class StudentSkillAdd(BaseModel):
    skill_id: str
    proficiency_level: str = "Intermediate"
