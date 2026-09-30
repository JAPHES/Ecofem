"""Editable public content for the database-free EcoFem website.

Add images under ``static/images/`` and reference them with paths relative to
that directory, for example ``images/team/jane-doe.jpg``. Keep slugs unique.
The README contains complete copy-and-paste examples for every content type.
"""


SITE = {
    "name": "EcoFem",
    "short_description": (
        "Developing affordable, biodegradable sanitary pads using processed "
        "water hyacinth fibres."
    ),
    "project_story": (
        "EcoFem began with a practical question: could a problematic plant "
        "biomass be transformed into a useful material for a product women "
        "rely on every month?\n\nThat question led to research into water "
        "hyacinth fibres, absorbent-core development and sanitary pad "
        "prototyping. The work continues through comparison, testing and "
        "improvement--with affordability, comfort and environmental "
        "responsibility guiding each decision."
    ),
    "mission": (
        "To develop accessible, sustainable and high-performing menstrual "
        "hygiene solutions while transforming environmental waste into "
        "useful resources."
    ),
    "vision": (
        "A future where every woman and girl can access safe and affordable "
        "menstrual products without compromising the environment."
    ),
    "values": (
        "Innovation",
        "Sustainability",
        "Dignity",
        "Inclusivity",
        "Quality",
        "Community Impact",
    ),
    # Public contact details; leave optional values blank to hide them.
    "email": "octorvitalice@gmail.com",
    "phone": "",
    "location": "",
    "linkedin_url": "",
    "instagram_url": "",
    "facebook_url": "",
}


# Confirmed EcoFem team members. Profile photos remain blank until an approved
# portrait is added under static/images/team/.
TEAM_MEMBERS = [
    {
        "full_name": "Octor Vitalice",
        "slug": "octor-vitalice",
        "profile_photo": "images/team/octor-vitalice.jpeg",
        "role": "Innovator",
        "expertise": "Natural Material Expert",
        "short_bio": (
            "Octor serves as EcoFem's Innovator with expertise in natural "
            "materials."
        ),
        "professional_background": (
            "Experience with biomaterials engineering will be key in process "
            "design, experimental optimization, equipment design, and "
            "fabrication."
        ),
        "contribution": "",
        "leadership_story": "",
        "vision_for_ecofem": "",
        "email": "",
        "linkedin_url": "",
        "leadership_label": "Founder",
        "is_founder_or_lead": True,
        "is_featured": True,
        "is_active": True,
    },
    {
        "full_name": "Professor Alunda",
        "slug": "professor-alunda",
        "profile_photo": "images/team/professor-alunda.jpeg",
        "role": "Co-Founder",
        "expertise": "Profile details to be confirmed",
        "short_bio": "Professor Alunda serves as a Co-Founder of EcoFem.",
        "professional_background": "",
        "contribution": "",
        "leadership_story": "",
        "vision_for_ecofem": "",
        "email": "",
        "linkedin_url": "",
        "leadership_label": "Co-Founder",
        "is_founder_or_lead": True,
        "is_featured": True,
        "is_active": True,
    },
    {
        "full_name": "Dickens Agumba",
        "slug": "dickens-agumba",
        "profile_photo": "images/team/dickens-agumba.jpeg",
        "role": "Co-Innovator",
        "expertise": "Profile details to be confirmed",
        "short_bio": "Dickens serves as a Co-Innovator at EcoFem.",
        "professional_background": "",
        "contribution": "",
        "leadership_story": "",
        "vision_for_ecofem": "",
        "email": "",
        "linkedin_url": "",
        "is_founder_or_lead": False,
        "is_featured": True,
        "is_active": True,
    },
    {
        "full_name": "Yvonne Achieng’",
        "slug": "yvonne-achieng",
        "profile_photo": "images/team/yvonne-achieng.jpeg",
        "role": "Project Lead",
        "expertise": "Data Analysis",
        "short_bio": (
            "Yvonne serves as EcoFem's Project Lead and brings core expertise "
            "in data analysis."
        ),
        "professional_background": (
            "Experience as an applied statistician will be key in production "
            "and sales data analytics, product research and development, "
            "funds appropriation, and accounting."
        ),
        "contribution": "",
        "leadership_story": "",
        "vision_for_ecofem": "",
        "email": "",
        "linkedin_url": "",
        "is_founder_or_lead": False,
        "is_featured": True,
        "is_active": True,
    },
    {
        "full_name": "Koti Matata",
        "slug": "koti-matata",
        "profile_photo": "images/team/koti-matata.jpeg",
        "role": "Technologist",
        "expertise": "Chemistry Expert",
        "short_bio": (
            "Koti serves as an EcoFem Technologist with core expertise in "
            "chemistry."
        ),
        "professional_background": (
            "A seasoned experiments designer, chemical analyst, and lead "
            "researcher dedicated to STEM mentorship, supporting high product "
            "quality and adherence to standardization."
        ),
        "contribution": "",
        "leadership_story": "",
        "vision_for_ecofem": "",
        "email": "",
        "linkedin_url": "",
        "is_founder_or_lead": False,
        "is_featured": True,
        "is_active": True,
    },
    {
        "full_name": "Victor Orwa",
        "slug": "victor-orwa",
        "profile_photo": "images/team/victor-orwa.jpeg",
        "role": "Engineering Technologist",
        "expertise": "Equipment Designer",
        "short_bio": (
            "Victor serves as an Engineering Technologist and Equipment "
            "Designer at EcoFem."
        ),
        "professional_background": (
            "Brings practical expertise in equipment design, fabrication, "
            "testing, technical problem-solving, experimentation, data "
            "collection, and translating research concepts into practical, "
            "functional solutions."
        ),
        "contribution": "",
        "leadership_story": "",
        "vision_for_ecofem": "",
        "email": "",
        "linkedin_url": "",
        "is_founder_or_lead": False,
        "is_featured": True,
        "is_active": True,
    },
    {
        "full_name": "Simion Masika",
        "slug": "simion-masika",
        "profile_photo": "images/team/simion-masika.jpeg",
        "role": "Mechanical Engineering",
        "expertise": "Product Designer",
        "short_bio": (
            "Simion supports EcoFem through mechanical engineering and "
            "product design."
        ),
        "professional_background": (
            "An expert in prototyping, experimentation, product design, and "
            "testing for optimal product quality."
        ),
        "contribution": "",
        "leadership_story": "",
        "vision_for_ecofem": "",
        "email": "",
        "linkedin_url": "",
        "is_founder_or_lead": False,
        "is_featured": False,
        "is_active": True,
    },
    {
        "full_name": "Milcah Chari",
        "slug": "milcah-chari",
        "profile_photo": "images/team/milcah-chari.jpeg",
        "role": "Administrator",
        "expertise": "Business Development Expert",
        "short_bio": (
            "Milcah serves as EcoFem's Administrator with expertise in "
            "business development."
        ),
        "professional_background": (
            "An administrative account manager who supports scalable project "
            "implementation through project coordination, stakeholder "
            "engagement, synthesis of customer insights, and project "
            "commercialization."
        ),
        "contribution": "",
        "leadership_story": "",
        "vision_for_ecofem": "",
        "email": "",
        "linkedin_url": "",
        "is_founder_or_lead": False,
        "is_featured": False,
        "is_active": True,
    },
    {
        "full_name": "Japhes Murithi",
        "slug": "japhes-murithi",
        "profile_photo": "images/team/japhes-murithi.jpeg",
        "role": "IT Expert",
        "expertise": "Digital Marketing Expertise",
        "short_bio": (
            "Japhes supports EcoFem as an IT Expert with digital marketing "
            "expertise."
        ),
        "professional_background": (
            "Brings digital marketing expertise to grow EcoFem's visibility, "
            "engagement, customer reach, and awareness."
        ),
        "contribution": "",
        "leadership_story": "",
        "vision_for_ecofem": "",
        "email": "",
        "linkedin_url": "",
        "is_founder_or_lead": False,
        "is_featured": False,
        "is_active": True,
    },
    {
        "full_name": "Amina Ndinya",
        "slug": "amina-ndinya",
        "profile_photo": "",
        "role": "Mentor",
        "expertise": "Strategist and Marketer",
        "short_bio": (
            "Amina serves as an EcoFem Mentor with strategy and marketing "
            "expertise."
        ),
        "professional_background": (
            "Brings entrepreneurship, strategic management, and marketing "
            "skills and expertise for innovation design, differentiation "
            "strategy, sustainability intelligence, and environmental "
            "evaluation."
        ),
        "contribution": "",
        "leadership_story": "",
        "vision_for_ecofem": "",
        "email": "",
        "linkedin_url": "",
        "is_founder_or_lead": False,
        "is_featured": False,
        "is_active": True,
    },
    {
        "full_name": "Anne Kemunto",
        "slug": "anne-kemunto",
        "profile_photo": "",
        "role": "Project Accountant",
        "expertise": "Accounting & Finance Expert",
        "short_bio": (
            "Anne serves as EcoFem's Project Accountant with accounting and "
            "finance expertise."
        ),
        "professional_background": (
            "Brings accounting, finance, knowledge dissemination, and people "
            "skills, with expertise in product costing and pricing, "
            "bookkeeping, stakeholder engagement, and product "
            "commercialization."
        ),
        "contribution": "",
        "leadership_story": "",
        "vision_for_ecofem": "",
        "email": "",
        "linkedin_url": "",
        "is_founder_or_lead": False,
        "is_featured": False,
        "is_active": True,
    },
    {
        "full_name": "James Indiya",
        "slug": "james-indiya",
        "profile_photo": "images/team/james-indiya.jpeg",
        "role": "Analyst",
        "expertise": "Analysis Expert",
        "short_bio": (
            "James serves as an EcoFem Analyst with core expertise in "
            "analysis."
        ),
        "professional_background": (
            "Brings project management, technical, and analytical skills for "
            "detailed documentation, progress tracking, and operational "
            "accountability."
        ),
        "contribution": "",
        "leadership_story": "",
        "vision_for_ecofem": "",
        "email": "",
        "linkedin_url": "",
        "is_founder_or_lead": False,
        "is_featured": False,
        "is_active": True,
    },
]


# Add only confirmed organisations with approved logo usage.
PARTNERS = []


# Add only approved, factual project news. Newest entries should come first.
UPDATES = []


# Add approved project photography. Entries are displayed in this order.
GALLERY_IMAGES = []

