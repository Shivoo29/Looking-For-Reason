from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import FileResponse, Response
from sqlalchemy.orm import Session
from typing import List
import uuid
import os
import shutil

from app.database import get_db
from app.models import User, Resume
from app.schemas import ResumeResponse, ResumeCreate, ATSScoreResponse, OptimizationResponse
from app.api.v1.endpoints.auth import get_current_user
from app.services.resume_parser import ResumeParser
from app.services.ats_scorer import ATSScorer
from app.services.ai_optimizer import AIOptimizer
from app.services.latex_generator import LaTeXGenerator
from app.config import settings

router = APIRouter()

resume_parser = ResumeParser()
ats_scorer = ATSScorer()
ai_optimizer = AIOptimizer()
latex_generator = LaTeXGenerator()


@router.get("/", response_model=List[ResumeResponse])
def list_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all resumes for current user"""
    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).all()
    return resumes


@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    name: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload and parse a resume"""

    # Validate file type
    allowed_extensions = ['.pdf', '.docx', '.txt']
    file_ext = os.path.splitext(file.filename)[1].lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not supported. Allowed: {', '.join(allowed_extensions)}"
        )

    # Generate unique filename
    resume_id = str(uuid.uuid4())
    file_name = f"{resume_id}{file_ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, file_name)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Parse resume
        parsed_result = resume_parser.parse_file(file_path)

        # Calculate initial ATS score
        ats_result = ats_scorer.calculate_score(
            parsed_result['raw_text'],
            parsed_result['parsed_data']
        )

        # Create resume record
        resume = Resume(
            id=resume_id,
            user_id=current_user.id,
            name=name or file.filename,
            file_name=file.filename,
            file_url=f"/uploads/{file_name}",
            file_path=file_path,
            raw_text=parsed_result['raw_text'],
            parsed_data=parsed_result['parsed_data'],
            ats_score=ats_result['score'],
            ats_feedback=ats_result,
        )

        db.add(resume)
        db.commit()
        db.refresh(resume)

        return resume

    except Exception as e:
        # Clean up file on error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing resume: {str(e)}"
        )


@router.get("/{resume_id}", response_model=ResumeResponse)
def get_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get resume by ID"""
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    return resume


@router.delete("/{resume_id}")
def delete_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete resume"""
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    # Delete file
    if os.path.exists(resume.file_path):
        os.remove(resume.file_path)

    db.delete(resume)
    db.commit()

    return {"message": "Resume deleted successfully"}


@router.post("/{resume_id}/analyze", response_model=ATSScoreResponse)
def analyze_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze resume and get ATS score"""
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    # Recalculate ATS score
    ats_result = ats_scorer.calculate_score(
        resume.raw_text,
        resume.parsed_data
    )

    # Update resume
    resume.ats_score = ats_result['score']
    resume.ats_feedback = ats_result
    db.commit()

    return {
        'score': ats_result['score'],
        'feedback': ats_result['feedback'],
        'missing_keywords': ats_result['missing_keywords'],
        'suggestions': ats_result['suggestions'],
    }


@router.post("/{resume_id}/optimize")
async def optimize_resume(
    resume_id: str,
    job_description_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Optimize resume for specific job description"""

    from app.models import JobDescription

    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    job_desc = db.query(JobDescription).filter(
        JobDescription.id == job_description_id,
        JobDescription.user_id == current_user.id
    ).first()

    if not job_desc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found"
        )

    # Optimize resume
    try:
        optimization_result = ai_optimizer.optimize_resume(
            resume.raw_text,
            resume.parsed_data,
            job_desc.raw_text,
            job_desc.parsed_data
        )

        # Generate PDF
        optimized_data = resume.parsed_data.copy()
        optimized_data['optimized_text'] = optimization_result['optimized_text']

        pdf_bytes = latex_generator.generate_pdf(
            optimized_data,
            optimization_result['optimized_text']
        )

        # Save optimized PDF
        optimized_filename = f"{resume_id}_optimized_{job_description_id}.pdf"
        optimized_path = os.path.join(settings.UPLOAD_DIR, optimized_filename)

        with open(optimized_path, 'wb') as f:
            f.write(pdf_bytes)

        return {
            'optimized_resume_url': f"/uploads/{optimized_filename}",
            'improvements': optimization_result['improvements'],
            'before_score': resume.ats_score,
            'after_score': optimization_result['ats_score_estimate'],
            'keyword_additions': optimization_result['keyword_additions'],
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error optimizing resume: {str(e)}"
        )


@router.get("/{resume_id}/latex")
def download_latex(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download resume as LaTeX PDF"""
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    try:
        # Generate PDF
        pdf_bytes = latex_generator.generate_pdf(resume.parsed_data)

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={resume.name.replace(' ', '_')}.pdf"
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating PDF: {str(e)}"
        )
