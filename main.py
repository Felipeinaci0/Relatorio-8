from database import Database
from game_database import GameDatabase

# Cria uma instância da classe Database, passando os dados de conexão com o banco de dados Neo4j
db = Database("bolt://54.173.248.108:7687", "neo4j", "warships-stretches-names")
db.drop_all()

# Criando uma instância da classe GameDatabase para interagir com o banco de dados
game_db = GameDatabase(db)

# Criando jogadores
game_db.create_player("1", "Lucas")
game_db.create_player("2", "Ricardo")
game_db.create_player("3", "Maria")

# Atualizando o nome de um jogador
game_db.update_player("1", "Lucas Updated")

# Registrando uma partida
game_db.create_match("101", ["1", "2"], "Lucas 3 - 2 Ricardo")

# Registrando outra partida
game_db.create_match("102", ["2", "3"], "Ricardo 4 - 1 Maria")

# Obter informações de um jogador
player = game_db.get_player("1")
print("Player:", player)

# Obter informações de uma partida
match = game_db.get_match("101")
print("Match:", match)

# Obter histórico de partidas de um jogador
matches = game_db.get_player_matches("1")
print("Matches played by player 1:", matches)

# Obter todos os jogadores
players = game_db.get_all_players()
print("All players:", players)

# Excluir um jogador
game_db.delete_player("3")

# Fechando a conexão com o banco de dados
db.close()
