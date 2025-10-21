# @app.on_event("startup")
# def startup_event():
#     """Initialize vector store on startup"""
#     print("🚀 Starting Laptop Chatbot API...")
#     db = next(get_db())
#     try:
#         # Check if we have laptops in DB
#         laptop_count = db.query(Laptop).count()
#         if laptop_count == 0:
#             print("⚠️ No laptops in database. Adding sample data...")
#             seed_sample_data(db)
        
#         # Build vector store
#         print("🔨 Building vector store...")
#         build_vector_store(db)
#         print("✅ Vector store ready!")
#     finally:
#         db.close()


# def seed_sample_data(db: Session):
#     """Add sample laptop data for testing"""
#     sample_laptops = [
#         Laptop(
#             name="MacBook Pro 14",
#             brand="Apple",
#             specs="M3 Pro chip, 18GB RAM, 512GB SSD, 14-inch Liquid Retina XDR display",
#             price=1999.00
#         ),
#         Laptop(
#             name="Dell XPS 13",
#             brand="Dell",
#             specs="Intel i7-1355U, 16GB RAM, 512GB SSD, 13.4-inch FHD+ display",
#             price=1299.00
#         ),
#         Laptop(
#             name="ThinkPad X1 Carbon",
#             brand="Lenovo",
#             specs="Intel i7-1365U, 32GB RAM, 1TB SSD, 14-inch WUXGA display",
#             price=1899.00
#         ),
#         Laptop(
#             name="ROG Zephyrus G14",
#             brand="ASUS",
#             specs="AMD Ryzen 9 7940HS, RTX 4060, 16GB RAM, 1TB SSD, 14-inch QHD display",
#             price=1599.00
#         ),
#         Laptop(
#             name="Surface Laptop 5",
#             brand="Microsoft",
#             specs="Intel i7-1255U, 16GB RAM, 512GB SSD, 13.5-inch PixelSense display",
#             price=1399.00
#         ),
#     ]
    
#     db.add_all(sample_laptops)
#     db.commit()
#     print(f"✅ Added {len(sample_laptops)} sample laptops")



# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./laptops.db"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()




# @app.get("/")
# def root():
#     return {
#         "message": "Laptop Chatbot API",
#         "endpoints": {
#             "search": "/chatbot/search",
#             "ask": "/chatbot/ask"
#         }
#     }