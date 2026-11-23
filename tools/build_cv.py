#!/usr/bin/env python3
"""Build assets/docs/Ismail-Hussain-CV.pdf (one page, A4).

Usage:  python tools/build_cv.py

Edit the CONTENT block below, re-run, then commit the regenerated PDF.
House style: Helvetica (Arial equivalent), navy headings, no personal pronouns,
active verbs, one page.
"""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer

OUT = Path(__file__).resolve().parent.parent / "assets" / "docs" / "Ismail-Hussain-CV.pdf"
NAVY = colors.HexColor("#1F4E79")
TEAL = colors.HexColor("#0F766E")
GREY = colors.HexColor("#444444")

# --------------------------------------------------------------------------- #
# CONTENT: edit here.
# --------------------------------------------------------------------------- #
NAME = "Ismail Hussain"
CONTACT = (
    "ismail.h2589@gmail.com &nbsp;|&nbsp; linkedin.com/in/ismail-hussain22 "
    "&nbsp;|&nbsp; ismail-h01.github.io &nbsp;|&nbsp; West Midlands, UK"
)
PROFILE = (
    "Graduate Electrical Engineer at Amey Consulting with a First Class BEng (Hons) in Electrical and "
    "Electronic Engineering from Aston University and a year of industrial placement at Renishaw. "
    "Experience across infrastructure lighting design, electronics and product development, taking work "
    "from first concept through design and testing to delivery and production. Member of the IET (MIET)."
)
EDUCATION = [
    (
        "Aston University",
        "BEng (Hons) Electrical and Electronic Engineering, First Class Honours",
        "Graduated 2026",
        ["Includes a year in industry at Renishaw (2024 to 2025)."],
    ),
]
EXPERIENCE = [
    (
        "Amey Consulting",
        "Graduate Electrical Engineer, highway lighting design",
        "Sep 2026 to present",
        [
            "Owns client lighting proposals from brief to final deliverable, acting as the point of contact for "
            "client queries, for upgrades, new column installations and new developments.",
            "Assigns M, C or P lighting classes using BS 5489-1 and designs in Lighting Reality to meet BS EN 13201-2; "
            "produces AutoCAD drawings on Ordnance Survey mapping with every column placed at exact coordinates.",
            "Reviews statutory utility records (overhead lines, BT, HV and LV cables, water and gas mains) so designs "
            "are safe to build; works on Section 278 and Section 38 developer schemes (Highways Act 1980).",
        ],
    ),
    (
        "Renishaw plc",
        "Industrial Placement, Electronics, Encoder Product Division",
        "2024 to 2025",
        [
            "Redesigned a production test jig PCB from scratch in Zuken CR-8000, replacing obsolete parts "
            "and fitting the existing jig; reached board testing.",
            "Carried out a self-directed ESD qualification (contact discharge up to ±12 kV) on a replacement "
            "protection device; findings presented to senior engineers and approved for production.",
            "Ran structured pulse testing, including at elevated temperature, to assess a protection "
            "component; results signed off by stakeholders.",
            "Designed a PCB for a project at another company site, wrote test plans and completed "
            "professional soldering training down to 0402 parts.",
        ],
    ),
]
PROJECTS = [
    (
        "MACCS+: Matter-enabled curtain and lighting controller",
        "Final year project, 2025 to 2026",
        [
            "Designed a custom power PCB (reverse polarity protection, soft start, 12 V to 5 V buck stage), "
            "ESP32-C6 firmware (ESP-IDF, FreeRTOS), Matter control through Apple Home and a belt-driven "
            "mechanism in Fusion 360.",
            "Validated against a 92-test plan: 83 passed, 7 partial, 2 failed, with failures reported openly.",
        ],
    ),
    (
        "Three-phase AC-DC-AC converter and isolated gate drive (EE3PEC)",
        "Power electronics paper, 2025",
        [
            "Modelled the converter in MATLAB/Simulink with a 20 kW load; built and tested an isolated "
            "gate drive PCB, measuring a 30 V (+15 V to -15 V) swing and about 8 microseconds of dead-time.",
        ],
    ),
]
LEADERSHIP = [
    "<b>Mentor</b>, Graduate Engineering Engagement Programme (GEEP), Royal Academy of Engineering.",
    "<b>School Rep</b>, School of Engineering and Physical Sciences, Aston University: represented students "
    "from every course in the school in meetings with academic staff and faculty leadership, from day-to-day "
    "course concerns to serious matters. Also <b>Student Rep</b> for Electrical and Electronic Engineering.",
    "<b>STEM Ambassador</b>, Renishaw: engineering demonstrations and careers talks for visiting school groups.",
    "<b>Early Careers Network Challenge</b>, Renishaw: placed 2nd of 8 teams; designed the engagement "
    "survey and presented the events plan to a judging panel.",
]
SKILLS = [
    ("CAD and PCB", "Zuken CR-8000, Altium Designer, Proteus, Fusion 360, AutoCAD"),
    ("Simulation", "MATLAB/Simulink, LTspice, Lighting Reality"),
    ("Embedded", "C/C++, ESP-IDF, FreeRTOS, SoftConsole and Libero, Matter"),
    ("Lab and test", "ESD testing, PCB debugging, advanced soldering (0402), oscilloscope measurement"),
    ("Standards and tools", "BS 5489-1, BS EN 13201, Highways Act 1980 (S38 and S278), Git"),
]
TRAINING = (
    "Renishaw soldering training (basic 12 h, advanced 24 h); Zuken CR-8000 on-site training; "
    "C programming course (40 h)."
)
# --------------------------------------------------------------------------- #

base = ParagraphStyle("base", fontName="Helvetica", fontSize=9.3, leading=12.3, textColor=GREY, alignment=TA_LEFT)
name_s = ParagraphStyle("name", parent=base, fontName="Helvetica-Bold", fontSize=22, leading=26, textColor=NAVY)
contact_s = ParagraphStyle("contact", parent=base, fontSize=9, textColor=GREY, spaceAfter=2)
h_s = ParagraphStyle("h", parent=base, fontName="Helvetica-Bold", fontSize=10.2, leading=13, textColor=NAVY, spaceBefore=8)
role_s = ParagraphStyle("role", parent=base, fontName="Helvetica-Bold", textColor=colors.black)
sub_s = ParagraphStyle("sub", parent=base, textColor=TEAL, fontName="Helvetica-Oblique")
bul_s = ParagraphStyle("bul", parent=base, leftIndent=9, bulletIndent=0, spaceBefore=0.6)


def heading(text):
    return [Paragraph(text.upper(), h_s), HRFlowable(width="100%", thickness=0.7, color=NAVY, spaceAfter=3)]


def bullets(items):
    return [Paragraph(t, bul_s, bulletText="•") for t in items]


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm, topMargin=12 * mm, bottomMargin=10 * mm,
        title="Ismail Hussain, CV", author="Ismail Hussain", subject="Curriculum vitae",
    )
    s = [Paragraph(NAME, name_s), Paragraph(CONTACT, contact_s)]
    s += heading("Profile") + [Paragraph(PROFILE, base)]

    s += heading("Education")
    for org, deg, when, pts in EDUCATION:
        s += [Paragraph(f"<b>{org}</b> &nbsp;|&nbsp; {deg} &nbsp;|&nbsp; {when}", role_s)] + bullets(pts)

    s += heading("Experience")
    for org, role, when, pts in EXPERIENCE:
        s += [Paragraph(f"<b>{org}</b> &nbsp;|&nbsp; {role} &nbsp;|&nbsp; {when}", role_s)] + bullets(pts) + [Spacer(1, 2)]

    s += heading("Selected projects")
    for title, when, pts in PROJECTS:
        s += [Paragraph(f"<b>{title}</b> &nbsp;|&nbsp; <i>{when}</i>", role_s)] + bullets(pts) + [Spacer(1, 2)]

    s += heading("Leadership and outreach") + bullets(LEADERSHIP)

    skills = []
    for k, v in SKILLS:
        skills.append(Paragraph(f"<b>{k}:</b> {v}", base))
    s += heading("Skills") + skills
    s += heading("Training and membership") + [
        Paragraph("<b>Member of the Institution of Engineering and Technology (MIET).</b> " + TRAINING, base)
    ]
    doc.build(s)
    print("wrote", OUT)


if __name__ == "__main__":
    build()
