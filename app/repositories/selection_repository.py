from sqlite3 import OperationalError
from typing import Dict, List
from uuid import UUID

from ..domain import Selection
from ..ext.database import get_db
from . import generate_query_filter
from .exceptions import RepositoryOperationalError, SelectionNotFoundException


class SelectionRepository:
    def __init__(self) -> None:
        self._db = get_db()

    def get_selections(self, filters: Dict = None) -> List[Selection]:
        selections = []
        parameters = ()

        query = "SELECT * FROM selection "

        if filters:
            query += generate_query_filter(filters)
            parameters = tuple(filters.values())

        try:
            result = self._db.execute(query, parameters).fetchall()
        except OperationalError as err:
            raise RepositoryOperationalError(str(err))
        
        for selection in result:
            selections.append(Selection(**selection))

        return selections

    def get_selection_by_uuid(self, uuid: UUID) -> Selection:
        result = self._db.execute(
            "SELECT * FROM selection WHERE uuid = ?",
            (str(uuid),),
        ).fetchone()

        if result is None:
            raise SelectionNotFoundException()

        return Selection(**result)

    def create_selection(self, selection: Selection):        
        self._db.execute(
            (
                "INSERT INTO selection (event_id, uuid, price, active, outcome)"
                "VALUES (?, ?, ?, ?, ?)"
            ),
            (
                selection.event_id,
                str(selection.uuid),
                selection.price,
                selection.active,
                selection.outcome.value,
            ),
        )
        self._db.commit()

    def update_selection(self, uuid: UUID, selection: Selection) -> Selection:
        self._db.execute(
            (
                "UPDATE selection "
                "SET event_id = ?, price = ?, active = ?, outcome = ? "
                "WHERE uuid = ?"
            ),
            (
                selection.event_id,
                selection.price,
                selection.active,
                selection.outcome.value,
                str(uuid),
            ),
        )

        self._db.commit()

        return self.get_selection_by_uuid(uuid)
