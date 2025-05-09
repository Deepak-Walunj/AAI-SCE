from app.core.database import database
from app.repositories.auth import AuthRepository
from app.repositories.candidate import CandidateRepository
from app.core.collections import CollectionName
from app.services.auth import AuthService
from app.services.candidate import CandidateService

# Initialize database connection
db = None

async def initialize_db():
    """Initialize database connection."""
    global db
    await database.connect()
    db = database.db

class DependencyStorage:
    def __init__(self):
        if db is None:
            raise RuntimeError("Database not initialized")
        
        # Create repositories
        self._auth_repo = AuthRepository(db[CollectionName.AUTH_USERS.value])
        self._candidate_repo = CandidateRepository(db[CollectionName.CANDIDATES.value])
        
        # Create services
        self._auth_service = AuthService(auth_repository=self._auth_repo)
        self._candidate_service = CandidateService(candidate_repository=self._candidate_repo, auth_service=self._auth_service)
        
    def get_auth_repository(self) -> AuthRepository:
        return self._auth_repo

    def get_candidate_repository(self) -> CandidateRepository:
        return self._candidate_repo
    
    def get_auth_service(self) -> AuthService:
        return self._auth_service

    def get_candidate_service(self) -> CandidateService:
        return self._candidate_service
    
async def initialize_dependencies():
    """Initialize all dependencies."""
    global dependency_storage
    await initialize_db()
    dependency_storage = DependencyStorage()
    
# Dependency getter functions
def get_auth_repository() -> AuthRepository:
    if dependency_storage is None:
        raise RuntimeError("Dependencies not initialized")
    return dependency_storage.get_auth_repository()

def get_candidate_repository() -> CandidateRepository:
    if dependency_storage is None:
        raise RuntimeError("Dependencies not initialized")
    return dependency_storage.get_candidate_repository()

def get_auth_service() -> AuthService:
    if dependency_storage is None:
        raise RuntimeError("Dependencies not initialized")
    return dependency_storage.get_auth_service()

def get_candidate_service() -> CandidateService:
    if dependency_storage is None:
        raise RuntimeError("Dependencies not initialized")
    return dependency_storage.get_candidate_service()