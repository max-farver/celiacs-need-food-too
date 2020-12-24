from database.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)  # type: ignore


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()