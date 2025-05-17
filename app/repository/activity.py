
from app.models import Activity
from app.repository._base import BaseRepository


class ActivityRepository(BaseRepository):

    def __init__(self, *args, **kwargs):
        super(ActivityRepository, self).__init__(*args, **kwargs)
        self.model = Activity
