
# engine = create_async_engine(
#     database_url,
#     pool_size=100,
#     max_overflow=10,
#     pool_timeout=30,
#     pool_recycle=1800,
#     pool_pre_ping=True,
#     echo=False,
# )
# Session=async_sessionmaker(bind=engine,autocommit=False,autoflush=False)

# async def get_db():
#     db=Session()
#     try:
#         yield db
#     finally:
#         db.close()
# # db_pool=pool.ThreadedConnectionPool(
# #     minconn=4,
# #     maxconn=12,
# #     dsn=database_url
# )
