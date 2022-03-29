from app.repositories import SportRepository


class ListSportsUsecase:
    def execute(
        self,
    ):
        repo = SportRepository()
        sports = repo.get_sport()
        return sports
