from fastapi import FastAPI, HTTPException
import logging
import httpx
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, registry, mapper
from sqlalchemy import Column, Integer, String, Table
from dataclasses import asdict

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

DATABASE_URL = "postgresql+asyncpg://pokeob:pokeob@localhost:5433/pokeob"
POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon/"

reg = registry()
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

pokemon_table = Table(
    "pokemons",
    reg.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("types", String, nullable=False),
    Column("sprite", String, nullable=False),
)

@reg.mapped_as_dataclass
class FavPoke:
    __tablename__ = "pokemons"
    id: int
    name: str
    types: str  
    sprite: str


@asynccontextmanager
async def lifeSpan(app):
    logger.info("Starting application")
    async with engine.begin() as conn:
        await conn.run_sync(reg.metadata.create_all)
    yield  
    logger.info("Shutting down application")
    async with engine.begin() as conn:
        await conn.run_sync(reg.metadata.drop_all)
    await engine.dispose()
    
app = FastAPI(lifespan=lifeSpan)


@app.get("/ping")
def ping():
    return {"ping": "pong"}

@app.get("/pokemon/{id}")
async def get_pokemon(id: int):
    """ Busca um Pokémon na PokéAPI pelo ID """
    logger.info(f"Iniciando busca pelo Pokémon com ID: {id}")

    if id < 1 or id > 300:
        logger.warning(f"ID {id} fora do intervalo permitido (1-300)")
        raise HTTPException(status_code=400, detail="ID fora do intervalo permitido (1-300)")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{POKEAPI_URL}{id}")

        if response.status_code != 200:
            logger.error(f"Falha ao buscar Pokémon com ID {id}, resposta {response.status_code}")
            raise HTTPException(status_code=404, detail="Pokémon não encontrado")

        data = response.json()
        logger.info(f"Pokémon encontrado: {data['name']}, ID: {data['id']}")
        
        return {
            "id": data["id"],
            "name": data["name"],
            "types": [t["type"]["name"] for t in data["types"]],
            "sprite": data["sprites"]["front_default"]
        }

    except httpx.RequestError as e:
        logger.error(f"Erro na requisição HTTP para Pokémon ID {id}: {e}")
        raise HTTPException(status_code=500, detail="Erro ao acessar a PokéAPI")


@app.post("/pokemon/{id}")
async def save_pokemon(id: int):
    """ Busca um Pokémon e salva no banco de dados """
    logger.info(f"Iniciando processo de salvar Pokémon com ID: {id}")
    
    try:
        pokemon_data = await get_pokemon(id)  # Usando o httpx para requisição assíncrona
        logger.info(f"Pokémon {pokemon_data['name']} encontrado. Salvando no banco de dados.")

        async with AsyncSessionLocal() as session:
            async with session.begin():
                pokemon = FavPoke(
                    id=pokemon_data["id"],
                    name=pokemon_data["name"],
                    types=",".join(pokemon_data["types"]),
                    sprite=pokemon_data["sprite"]
                )
                session.add(pokemon)

            await session.commit()
            logger.info(f"Pokémon {pokemon.name} salvo no DB com sucesso!")

        return asdict(pokemon)

    except HTTPException as e:
        logger.error(f"Erro ao buscar Pokémon com ID {id}: {e.detail}")
        raise

    except Exception as e:
        logger.error(f"Erro ao salvar Pokémon com ID {id} no DB: {e}")
        raise HTTPException(status_code=500, detail="Erro ao salvar Pokémon no banco de dados")

