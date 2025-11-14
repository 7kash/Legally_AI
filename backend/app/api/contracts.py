"""
Contracts API
Endpoints for contract upload and management
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from pathlib import Path
import uuid
import aiofiles
import os

from ..database import get_db
from ..models.user import User
from ..models.contract import Contract
from ..schemas.contract import ContractResponse, ContractList, ContractUpload
from ..core.deps import get_current_user, check_analysis_limit
from ..config import settings

router = APIRouter()


@router.post("/upload", response_model=ContractUpload, status_code=status.HTTP_201_CREATED)
async def upload_contract(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a contract file

    Args:
        file: Uploaded file (PDF or DOCX)
        current_user: Current authenticated user
        db: Database session

    Returns:
        Contract upload confirmation

    Raises:
        HTTPException: If file type not allowed or size exceeds limit
    """
    # Check analysis limit for free tier
    check_analysis_limit(current_user)

    # Validate file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file_ext} not allowed. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )

    # Read file content to check size
    content = await file.read()
    file_size = len(content)

    # Check file size
    max_size_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if file_size > max_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds {settings.MAX_FILE_SIZE_MB}MB limit"
        )

    # Create contract record
    contract_id = uuid.uuid4()
    contract = Contract(
        id=contract_id,
        user_id=current_user.id,
        filename=file.filename,
        mime_type=file.content_type or "application/octet-stream",
        file_size=file_size,
        file_path=f"{current_user.id}/{contract_id}{file_ext}"
    )

    # Save file to disk
    upload_dir = Path(settings.UPLOAD_DIR) / str(current_user.id)
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / f"{contract_id}{file_ext}"

    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(content)

    # Save contract to database
    db.add(contract)
    db.commit()
    db.refresh(contract)

    return ContractUpload(
        contract_id=contract.id,
        filename=contract.filename,
        status="uploaded"
    )


@router.get("/", response_model=ContractList)
async def list_contracts(
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List user's contracts

    Args:
        page: Page number (1-indexed)
        page_size: Number of contracts per page
        current_user: Current authenticated user
        db: Database session

    Returns:
        Paginated list of contracts
    """
    from ..models.analysis import Analysis

    # Calculate offset
    offset = (page - 1) * page_size

    # Get contracts
    contracts = db.query(Contract)\
        .filter(Contract.user_id == current_user.id)\
        .order_by(Contract.created_at.desc())\
        .offset(offset)\
        .limit(page_size)\
        .all()

    # Get total count
    total = db.query(Contract).filter(Contract.user_id == current_user.id).count()

    # Build response with latest analysis ID for each contract
    contract_responses = []
    for contract in contracts:
        # Get the latest analysis for this contract
        latest_analysis = db.query(Analysis)\
            .filter(Analysis.contract_id == contract.id)\
            .order_by(Analysis.created_at.desc())\
            .first()

        # Create response dict
        contract_dict = {
            "id": contract.id,
            "user_id": contract.user_id,
            "filename": contract.filename,
            "mime_type": contract.mime_type,
            "file_size_bytes": contract.file_size_bytes,
            "pages": contract.pages,
            "detected_language": contract.detected_language,
            "quality_score": contract.quality_score,
            "coverage_score": contract.coverage_score,
            "confidence_level": contract.confidence_level,
            "confidence_reason": contract.confidence_reason,
            "status": contract.status,
            "created_at": contract.created_at,
            "latest_analysis_id": latest_analysis.id if latest_analysis else None
        }
        contract_responses.append(ContractResponse(**contract_dict))

    return ContractList(
        contracts=contract_responses,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{contract_id}", response_model=ContractResponse)
async def get_contract(
    contract_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get contract details

    Args:
        contract_id: Contract ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Contract details

    Raises:
        HTTPException: If contract not found or access denied
    """
    contract = db.query(Contract).filter(
        Contract.id == contract_id,
        Contract.user_id == current_user.id
    ).first()

    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found"
        )

    return ContractResponse.model_validate(contract)


@router.delete("/{contract_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contract(
    contract_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a contract

    Args:
        contract_id: Contract ID
        current_user: Current authenticated user
        db: Database session

    Raises:
        HTTPException: If contract not found or access denied
    """
    contract = db.query(Contract).filter(
        Contract.id == contract_id,
        Contract.user_id == current_user.id
    ).first()

    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found"
        )

    # Delete file from disk
    file_path = Path(settings.UPLOAD_DIR) / contract.file_path
    if file_path.exists():
        os.remove(file_path)

    # Delete contract from database (cascade deletes analyses)
    db.delete(contract)
    db.commit()

    return None
