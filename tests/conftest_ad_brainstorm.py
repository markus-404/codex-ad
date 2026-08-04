"""Fixture builders shared by the ad-brainstorm validator tests."""

FORMATS = [
    "UGC monologue", "Before/after timer", "Founder story", "Parody news",
    "Reddit reaction", "Listicle", "Expert breakdown", "Day-in-the-life",
    "Testimonial cut", "ASMR product moment",
]
ANGLES = [
    "Pain killer", "Status symbol", "Time saver", "Money saver", "Identity badge",
    "Secret weapon", "Category disruptor", "Peer recommendation",
    "Expert endorsement", "Contrarian truth",
]
PLATFORMS = [
    "Meta feed", "Meta Reels", "TikTok", "YouTube Shorts",
    "YouTube long-form", "Reddit", "LinkedIn", "Pinterest",
]
ANGLES_LIGHTING = [
    "hard directional key from the left with sharp falloff",
    "soft north window light wrapping the shoulder",
    "cold overhead studio strip with even fill",
    "warm low golden rim light from behind",
]
CAMERA_ANGLES = [
    "eye-level three-quarter view",
    "top-down flat-lay",
    "low hero angle",
    "tight macro on the dropper",
]
SHOT_TYPES = ["hero", "detail", "macro", "packaging"]


def build_analysis(image_count=4):
    images = []
    for i in range(image_count):
        images.append({
            "index": i + 1,
            "source_url": "https://cdn.example.com/img-{0}.jpg".format(i + 1),
            "shot_type": SHOT_TYPES[i % len(SHOT_TYPES)],
            "subject": "the amber dropper bottle standing alone centered in frame",
            "form_factor": "tall narrow amber glass bottle with matte white cap",
            "materials_finish": "amber glass with a soft matte label stock",
            "label_and_typography": "centered serif wordmark in wide letter spacing",
            "color_hexes": ["#f4ede3", "#8b6a3f"],
            "lighting": ANGLES_LIGHTING[i % len(ANGLES_LIGHTING)],
            "camera_angle": CAMERA_ANGLES[i % len(CAMERA_ANGLES)],
            "backdrop_surface": "cream seamless paper sweep behind the bottle",
            "humans": "no humans shown",
            "props": ["dried botanicals"],
            "mood": "quiet clinical calm",
        })
    return {
        "images": images,
        "rollup": {
            "form_factor": "tall narrow amber glass dropper bottle roughly thirty millilitres",
            "color_palette": ["#f4ede3", "#8b6a3f", "#ffffff"],
            "packaging_style": "minimal",
            "brand_aesthetic_read": "clinical premium, closer to a dermatology office than a beauty shelf",
            "who_is_in_the_photos": "no humans appear in any image",
            "settings_shown": "cream seamless backdrops and one macro of the dropper tip",
            "premium_or_playful": "premium",
            "whats_missing": [
                "no bathroom morning routine context",
                "no skin contact or application shots",
                "no demographic diversity among users",
                "no before and after on real faces",
            ],
            "suggested_visual_styles": [
                "cinematic macro on cream with single backlight",
                "warm morning bathroom with natural window light",
                "dermatologist office editorial with clipboard",
                "forty five degree top-down flat lay",
                "slow motion droplet on bare forearm",
            ],
            "ugc_opportunity": "the brand has never shown a real person using this product on camera at home",
        },
    }


def build_concepts(formats=None, angles=None):
    formats = formats or FORMATS
    angles = angles or ANGLES
    grounding_pool = [
        ["rollup.ugc_opportunity"],
        ["rollup.suggested_visual_styles[1]", "images[0].lighting"],
        ["images[1].backdrop_surface"],
        ["rollup.whats_missing[2]", "images[2].camera_angle"],
        ["images[3].mood"],
        ["rollup.suggested_visual_styles[4]", "rollup.whats_missing[0]"],
    ]
    concepts = []
    for fi, fmt in enumerate(formats, start=1):
        for ai, ang in enumerate(angles, start=1):
            n = (fi - 1) * len(angles) + ai
            concepts.append({
                "id": "F{0}-A{1}".format(fi, ai),
                "format_index": fi,
                "format": fmt,
                "angle_index": ai,
                "angle": ang,
                "hook": "Distinct opening line number {0} about {1}".format(n, ang.lower()),
                "summary": [
                    "Opening beat {0} establishes the scene and the tension quickly.".format(n),
                    "Closing beat {0} lands the product and the argument cleanly.".format(n),
                ],
                "visual_style": "Visual treatment variant {0} with specific lighting".format(n),
                "visual_grounding": grounding_pool[n % len(grounding_pool)],
                "platform": PLATFORMS[n % len(PLATFORMS)],
            })
    return {
        "product": {
            "title": "Lumora Vitamin C Brightening Serum",
            "brand": "Lumora",
            "price": "$48",
            "url": "https://lumora.co/products/vitamin-c-serum",
            "slug": "vitamin-c-serum",
        },
        "grid": {"formats": formats, "angles": angles},
        "concepts": concepts,
    }
