class GameDatabase:
    def __init__(self, db):
        self.db = db

    def create_player(self, player_id, name):
        with self.db.driver.session() as session:
            session.write_transaction(self._create_player, player_id, name)

    @staticmethod
    def _create_player(tx, player_id, name):
        query = (
            "CREATE (p:Player {id: $player_id, name: $name}) "
            "RETURN p"
        )
        tx.run(query, player_id=player_id, name=name)

    def update_player(self, player_id, name):
        with self.db.driver.session() as session:
            session.write_transaction(self._update_player, player_id, name)

    @staticmethod
    def _update_player(tx, player_id, name):
        query = (
            "MATCH (p:Player {id: $player_id}) "
            "SET p.name = $name "
            "RETURN p"
        )
        tx.run(query, player_id=player_id, name=name)

    def delete_player(self, player_id):
        with self.db.driver.session() as session:
            session.write_transaction(self._delete_player, player_id)

    @staticmethod
    def _delete_player(tx, player_id):
        query = (
            "MATCH (p:Player {id: $player_id}) "
            "DETACH DELETE p"
        )
        tx.run(query, player_id=player_id)

    def create_match(self, match_id, players, result):
        with self.db.driver.session() as session:
            session.write_transaction(self._create_match, match_id, players, result)

    @staticmethod
    def _create_match(tx, match_id, players, result):
        query = (
            "CREATE (m:Match {id: $match_id, result: $result}) "
            "WITH m "
            "UNWIND $players as player_id "
            "MATCH (p:Player {id: player_id}) "
            "CREATE (p)-[:PLAYED_IN]->(m) "
            "RETURN m"
        )
        tx.run(query, match_id=match_id, players=players, result=result)

    def get_player(self, player_id):
        with self.db.driver.session() as session:
            result = session.read_transaction(self._get_player, player_id)
            return result.single()

    @staticmethod
    def _get_player(tx, player_id):
        query = (
            "MATCH (p:Player {id: $player_id}) "
            "RETURN p"
        )
        return tx.run(query, player_id=player_id)

    def get_match(self, match_id):
        with self.db.driver.session() as session:
            result = session.read_transaction(self._get_match, match_id)
            return result.single()

    @staticmethod
    def _get_match(tx, match_id):
        query = (
            "MATCH (m:Match {id: $match_id}) "
            "RETURN m"
        )
        return tx.run(query, match_id=match_id)

    def get_player_matches(self, player_id):
        with self.db.driver.session() as session:
            result = session.read_transaction(self._get_player_matches, player_id)
            return [record["m"] for record in result]

    @staticmethod
    def _get_player_matches(tx, player_id):
        query = (
            "MATCH (p:Player {id: $player_id})-[:PLAYED_IN]->(m:Match) "
            "RETURN m"
        )
        return tx.run(query, player_id=player_id)

    def get_all_players(self):
        with self.db.driver.session() as session:
            result = session.read_transaction(self._get_all_players)
            return [record["p"] for record in result]

    @staticmethod
    def _get_all_players(tx):
        query = (
            "MATCH (p:Player) "
            "RETURN p"
        )
        return tx.run(query)
