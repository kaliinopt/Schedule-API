from app.database import models
from app.core import oath2, utils
from app.database.database import get_db
from app.api.schemas import schemas
from app.core.utils import check_time_conflicts, get_next_occurrence_by_week