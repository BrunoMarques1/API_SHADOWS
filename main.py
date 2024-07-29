from fastapi import FastAPI
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, registry
from pydantic import BaseModel
import os

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:3306/{db_name}"

engine = create_engine(db_url)
mapper_registy = registry()
Base = mapper_registy.generate_base()
Session = sessionmaker(bind=engine)
session = Session()
app = FastAPI()

class Body(BaseModel):
    titulo: str
    genero: str
    ano: int

class Filmes(Base):
    __tablename__ = "filmes"

    titulo = Column(String, primary_key=True)
    genero = Column(String, nullable=False)
    ano = Column(Integer, nullable=False)

    def __repr__(self):
        return f"Filme [titulo={self.titulo}, ano={self.ano}]"

@app.get("/")
async def get():
    return "OLÁ MUNDO!"

@app.get("/get")
async def get():
    data = session.query(Filmes).all()
    return data

@app.post("/")
async def post(body: Body):
    data_insert = Filmes(titulo=body.titulo, genero=body.genero, ano=body.ano)
    session.add(data_insert)
    session.commit()

@app.delete("/")
async def delete(body: Body):
    session.query(Filmes).filter(Filmes.titulo == body.titulo).delete()
    session.commit()

@app.put("/titulo={titulo}")
async def put(body: Body, titulo):
    session.query(Filmes).filter(Filmes.titulo == titulo).update({"titulo": body.titulo, "genero": body.genero, "ano": body.ano})
    session.commit()
