class GameDatabase:
    def __init__(self, database):
        self.db = database

    def create_player(self, player_id, name):
        query = "CREATE (:Player {id: $player_id, name: $name})"
        parameters = {"player_id": player_id, "name": name}
        self.db.execute_query(query, parameters)

    def update_player(self, player_id, name):
        query = "MATCH (p:Player {id: $player_id}) SET p.name = $name"
        parameters = {"player_id": player_id, "name": name}
        self.db.execute_query(query, parameters)

    def delete_player(self, player_id):
        query = "MATCH (p:Player {id: $player_id}) DETACH DELETE p"
        parameters = {"player_id": player_id}
        self.db.execute_query(query, parameters)

    def create_match(self, match_id, players, result):
        query = (
            "CREATE (m:Match {id: $match_id, result: $result}) "
            "WITH m "
            "UNWIND $players AS player_id "
            "MATCH (p:Player {id: player_id}) "
            "CREATE (p)-[:PLAYED_IN]->(m)"
        )
        parameters = {"match_id": match_id, "players": players, "result": result}
        self.db.execute_query(query, parameters)

    def get_players(self):
        query = "MATCH (p:Player) RETURN p.id AS id, p.name AS name"
        results = self.db.execute_query(query)
        return [{"id": result["id"], "name": result["name"]} for result in results]

    def get_player(self, player_id):
        query = "MATCH (p:Player {id: $player_id}) RETURN p.id AS id, p.name AS name"
        parameters = {"player_id": player_id}
        results = self.db.execute_query(query, parameters)
        return results[0] if results else None

    def get_matches(self):
        query = "MATCH (m:Match) RETURN m.id AS id, m.result AS result"
        results = self.db.execute_query(query)
        return [{"id": result["id"], "result": result["result"]} for result in results]

    def get_match(self, match_id):
        query = "MATCH (m:Match {id: $match_id}) RETURN m.id AS id, m.result AS result"
        parameters = {"match_id": match_id}
        results = self.db.execute_query(query, parameters)
        return results[0] if results else None

    def get_player_matches(self, player_id):
        query = (
            "MATCH (p:Player {id: $player_id})-[:PLAYED_IN]->(m:Match) "
            "RETURN m.id AS id, m.result AS result"
        )
        parameters = {"player_id": player_id}
        results = self.db.execute_query(query, parameters)
        return [{"id": result["id"], "result": result["result"]} for result in results]

    def delete_match(self, match_id):
        query = "MATCH (m:Match {id: $match_id}) DETACH DELETE m"
        parameters = {"match_id": match_id}
        self.db.execute_query(query, parameters)
