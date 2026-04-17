from sqlalchemy import create_engine

engine = create_engine("postgresql://user:pass@localhost:5432/fx_db")