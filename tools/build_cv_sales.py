#!/usr/bin/env python3
"""Build assets/docs/Ismail-Hussain-CV-Sales.pdf: the web-safe sales CV (one page, A4).

Usage:  python tools/build_cv_sales.py

Based on Ismail's sales-targeted CV, with internal production details left out
because this copy is public (see docs/CONTENT-SOURCES.md). Styles are shared
with tools/build_cv.py.
"""
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from build_cv import base, bullets, contact_s, heading, name_s, role_s, sub_s

OUT = Path(__file__).resolve().parent.parent / "assets" / "docs" / "Ismail-Hussain-CV-Sales.pdf"

NAME = "Ismail Hussain"
CONTACT = (
    "BEng (Hons) Electrical and Electronic Engineering, First Class &nbsp;|&nbsp; MIET<br/>"
    "ismail.h2589@gmail.com &nbsp;|&nbsp; linkedin.com/in/ismail-hussain22 &nbsp;|&nbsp; ismail-h01.github.io/sales"
)
PROFILE = (
    "First Class Electrical and Electronic Engineering graduate (MIET) with client-facing experience at Amey "
    "Consulting and Renishaw plc. Looking to move from a technical role into a sales or commercially focused "
    "role, using an engineering background to understand customer needs."
)
EXPERIENCE = [
    ("Amey Consulting, Manchester", "Graduate Electrical Engineer, Highway and Street Lighting", "Sep 2026 to present", [
        "Take client lighting proposals from first brief to final deliverable, acting as the client's technical point of "
        "contact and resolving queries on scope, site area and requirements.",
        "Translate client needs into compliant designs, assigning M, C and P lighting classes to BS 5489-1 and running "
        "Lighting Reality calculations to prove BS EN 13201 performance levels.",
        "Identified early that a scheme's budget would not cover the work required. Built an evidence-based case showing "
        "where hours were being stretched and negotiated a budget extension, keeping delivery on time without "
        "compromising quality.",
        "Act as the link between clients and the senior design team, keeping clients updated and managing expectations "
        "on deliverables and deadlines.",
        "Gather utility records and site information up front so proposals are right first time, saving clients "
        "redesign costs and delays.",
    ]),
    ("Renishaw plc, Wotton-under-Edge", "Electronics Engineer (placement year), Encoder Products Division", "2024 to 2025", [
        "Helped customers select the right product for their application, reviewing their requirements and specifying "
        "the best RESOLUTE readhead configuration, from linear or rotary scale to serial interface and cable length and sizing.",
        "Recommended alternative Renishaw encoders where they suited the application better and introduced add-ons such "
        "as the Advanced Diagnostic Tool (ADT) to make readhead set-up and configuration quicker for the customer.",
        "Built and presented the business case to remove a protection IC fitted across most of the encoder interface "
        "connector range, winning stakeholder sign-off and cutting component cost across numerous products.",
        "Secured stakeholder approval for a replacement for an end-of-life part, keeping the ATOM and TONiC product "
        "lines available to customers.",
        "Led the redesign of an obsolete production test board for the RESOLUTE line, reducing a risk to production.",
        "Delivered for internal and external customers to tight deadlines, including a PCB built to exact specification "
        "for a lead photonics engineer and encoder cable assemblies turned round in one week for a US university "
        "running vacuum testing for space applications.",
    ]),
]
LEADERSHIP = [
    "<b>Team Lead, Early Careers Network Challenge</b>, Renishaw: surveyed early-career staff, used the results to "
    "shape an engagement proposal and pitched it to a senior judging panel, placing 2nd of 8. The ECN committee "
    "followed up to take the ideas forward.",
    "<b>Mentor, GEEP</b>, Royal Academy of Engineering: one-to-one career guidance for an engineering student from "
    "an under-represented background.",
    "<b>STEM Ambassador</b>, Renishaw: delivered engineering demonstrations and supported careers talks for visiting "
    "school groups.",
    "<b>School Representative</b>, Aston University: represented students to faculty leadership and negotiated "
    "issues through to resolution.",
]
EDUCATION = "<b>Aston University</b> &nbsp;|&nbsp; BEng (Hons) Electrical and Electronic Engineering, First Class, IET accredited"


def build():
    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm, topMargin=13 * mm, bottomMargin=11 * mm,
        title="Ismail Hussain, CV", author="Ismail Hussain", subject="Curriculum vitae",
    )
    s = [Paragraph(NAME, name_s), Paragraph(CONTACT, contact_s)]
    s += heading("Profile") + [Paragraph(PROFILE, base)]
    s += heading("Professional experience")
    for org, role, when, pts in EXPERIENCE:
        s += [Paragraph(f"<b>{org}</b> &nbsp;|&nbsp; {when}", role_s), Paragraph(role, sub_s)] + bullets(pts) + [Spacer(1, 4)]
    s += heading("Leadership and representation") + bullets(LEADERSHIP)
    s += heading("Education") + [Paragraph(EDUCATION, role_s)]
    doc.build(s)
    print("wrote", OUT)


if __name__ == "__main__":
    build()
