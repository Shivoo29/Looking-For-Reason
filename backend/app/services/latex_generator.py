from typing import Dict, Any, List
import os
import subprocess
import tempfile
import logging

logger = logging.getLogger(__name__)


class LaTeXGenerator:
    """Generate professional LaTeX resumes"""

    def __init__(self):
        self.template = self._get_template()

    def generate_pdf(
        self,
        resume_data: Dict[str, Any],
        optimized_text: str = None
    ) -> bytes:
        """
        Generate PDF from resume data

        Returns:
            PDF file as bytes
        """
        try:
            # Generate LaTeX content
            latex_content = self.generate_latex(resume_data, optimized_text)

            # Compile to PDF
            pdf_bytes = self._compile_latex(latex_content)

            return pdf_bytes

        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            raise

    def generate_latex(
        self,
        resume_data: Dict[str, Any],
        optimized_text: str = None
    ) -> str:
        """Generate LaTeX code from resume data"""

        contact = resume_data.get('contact', {})
        skills = resume_data.get('skills', [])
        experience = resume_data.get('experience', [])
        education = resume_data.get('education', [])
        summary = resume_data.get('summary', '')
        certifications = resume_data.get('certifications', [])

        # Build LaTeX document
        latex = r"""\documentclass[11pt,a4paper,sans]{moderncv}

\moderncvstyle{banking}
\moderncvcolor{blue}

\usepackage[utf8]{inputenc}
\usepackage[scale=0.85]{geometry}
\usepackage{multicol}

% Personal info
"""

        # Add personal information
        name = contact.get('name', 'Your Name')
        latex += f"\\name{{{name.split()[0] if name else 'First'}}}{{{' '.join(name.split()[1:]) if len(name.split()) > 1 else 'Last'}}}\n"

        if contact.get('email'):
            latex += f"\\email{{{contact['email']}}}\n"

        if contact.get('phone'):
            latex += f"\\phone[mobile]{{{contact['phone']}}}\n"

        if contact.get('linkedin'):
            latex += f"\\social[linkedin]{{{contact['linkedin'].replace('linkedin.com/in/', '')}}}\n"

        if contact.get('github'):
            latex += f"\\social[github]{{{contact['github'].replace('github.com/', '')}}}\n"

        latex += r"""
\begin{document}
\makecvtitle

"""

        # Professional Summary
        if summary or optimized_text:
            latex += r"\section{Professional Summary}" + "\n"
            summary_text = summary if summary else "Experienced professional seeking new opportunities."
            latex += f"{self._escape_latex(summary_text)}\n\n"

        # Experience
        if experience:
            latex += r"\section{Experience}" + "\n"
            for exp in experience[:5]:  # Top 5 experiences
                desc = exp.get('description', '')
                company = exp.get('company', 'Company')
                duration = exp.get('duration', '')

                latex += r"\cventry"
                latex += f"{{{duration}}}"  # years
                latex += f"{{{company}}}"   # company
                latex += "{}"                # title (empty)
                latex += "{}"                # location (empty)
                latex += "{}"                # empty
                latex += f"{{{self._escape_latex(desc[:200])}}}"  # description
                latex += "\n\n"

        # Skills
        if skills:
            latex += r"\section{Skills}" + "\n"

            # Split into technical and soft skills (simple heuristic)
            technical_keywords = ['python', 'java', 'javascript', 'aws', 'sql', 'react', 'docker']
            technical_skills = [s for s in skills if any(t in s.lower() for t in technical_keywords)]
            soft_skills = [s for s in skills if s not in technical_skills]

            if technical_skills:
                latex += r"\cvitem{Technical}{" + ", ".join(technical_skills[:15]) + "}\n"

            if soft_skills:
                latex += r"\cvitem{Soft Skills}{" + ", ".join(soft_skills[:10]) + "}\n"

            latex += "\n"

        # Education
        if education:
            latex += r"\section{Education}" + "\n"
            for edu in education[:3]:  # Top 3
                degree = edu.get('degree', '')
                institution = edu.get('institution', '')
                year = edu.get('year', '')

                latex += r"\cventry"
                latex += f"{{{year}}}"
                latex += f"{{{self._escape_latex(degree)}}}"
                latex += f"{{{institution}}}"
                latex += "{}"
                latex += "{}"
                latex += "{}"
                latex += "\n\n"

        # Certifications
        if certifications:
            latex += r"\section{Certifications}" + "\n"
            for cert in certifications[:5]:
                latex += f"\\cvlistitem{{{self._escape_latex(cert)}}}\n"
            latex += "\n"

        latex += r"\end{document}"

        return latex

    def _escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters"""
        if not text:
            return ""

        replacements = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\^{}',
            '\\': r'\textbackslash{}',
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text

    def _compile_latex(self, latex_content: str) -> bytes:
        """
        Compile LaTeX to PDF

        Note: This requires pdflatex to be installed on the system
        For production, you might want to use a service like Overleaf API
        """

        # For now, return a simple implementation
        # In production, you would:
        # 1. Write latex_content to a .tex file
        # 2. Run pdflatex on it
        # 3. Read the resulting PDF
        # 4. Return PDF bytes

        # Since pdflatex might not be available, we'll use a fallback
        try:
            # Create temporary directory
            with tempfile.TemporaryDirectory() as tmpdir:
                tex_file = os.path.join(tmpdir, 'resume.tex')
                pdf_file = os.path.join(tmpdir, 'resume.pdf')

                # Write LaTeX content
                with open(tex_file, 'w', encoding='utf-8') as f:
                    f.write(latex_content)

                # Try to compile
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', '-output-directory', tmpdir, tex_file],
                    capture_output=True,
                    timeout=30
                )

                if result.returncode == 0 and os.path.exists(pdf_file):
                    with open(pdf_file, 'rb') as f:
                        return f.read()
                else:
                    raise Exception(f"pdflatex compilation failed: {result.stderr.decode()}")

        except FileNotFoundError:
            logger.warning("pdflatex not found. Using fallback method.")
            return self._generate_fallback_pdf(latex_content)

        except Exception as e:
            logger.error(f"Error compiling LaTeX: {e}")
            return self._generate_fallback_pdf(latex_content)

    def _generate_fallback_pdf(self, latex_content: str) -> bytes:
        """
        Generate a simple PDF without LaTeX
        Uses reportlab as fallback
        """
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.units import inch
            from io import BytesIO

            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            # Extract text from LaTeX (simple approach)
            # Remove LaTeX commands
            import re
            text = re.sub(r'\\[a-zA-Z]+(\{[^}]*\})*', '', latex_content)
            text = text.replace('{', '').replace('}', '').strip()

            # Add paragraphs
            for line in text.split('\n'):
                if line.strip():
                    p = Paragraph(line.strip(), styles['Normal'])
                    story.append(p)
                    story.append(Spacer(1, 0.1 * inch))

            doc.build(story)
            pdf_bytes = buffer.getvalue()
            buffer.close()

            return pdf_bytes

        except Exception as e:
            logger.error(f"Error generating fallback PDF: {e}")
            # Return empty PDF as last resort
            return b'%PDF-1.4\n'

    def _get_template(self) -> str:
        """Get LaTeX template"""
        # In production, you might have multiple templates
        return "moderncv"  # Using moderncv package
