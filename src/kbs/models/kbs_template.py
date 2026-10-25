import logging

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class KnowledgeBaseTemplate(BaseModel):
    tag: str
    repository_name: str
    problem_description: str
    problem_solution: str
    new_information: str
    date_added: str
