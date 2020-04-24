import datetime

dummy_tests = [
    {"id": 1, "name": "Test 1"},
    {"id": 2, "name": "Test 2"},
    {"id": 3, "name": "Test 3"},
    {"id": 4, "name": "Test 4"},
    {"id": 5, "name": "Test 5"},
]

dummy_reports = [
    {
        "id": 1,
        "title": "Test Title 1",
        "description": "Test Title 1 Description",
        "schedule": "* * 4 * *",
        "emails": ["email1@mail.com", "email2@mail.com", "email3@mail.com"],
        "owner_name": "John Doe",
        "owner_email": "johndoe@mail.com",
        "tests": [dummy_tests[3], dummy_tests[0], dummy_tests[2]],
    },
    {
        "id": 2,
        "title": "Test Title 2",
        "description": "Test Title 2 Description",
        "schedule": "* 22 * * 6",
        "emails": ["email1@mail.com"],
        "owner_name": "John Doe",
        "owner_email": "johndoe@mail.com",
        "tests": [dummy_tests[4]],
    },
]

dummy_report_runs = [
    {
        "id": 1,
        "passed": False,
        "updated": datetime.datetime.now(),
        "title": "Diary of a Madman",
        "description": (
            "Donec posuere tincidunt metus sed dictum. Proin commodo nibh ",
            "magna, vitae tristique ex rhoncus vitae.",
        ),
        "owner_name": "Odele Barnewelle",
        "owner_email": "obarnewelle0@devhub.com",
        "errors": [
            {
                "id": 1,
                "title": "CD DiorSkin Forever Flawless Fusion Wear Makeup SPF 25 - 010",
                "description": "Unspecified open wound of left breast, initial encounter",
            },
            {
                "id": 2,
                "title": "Adoxa",
                "description": (
                    "Primary blast injury of unspecified ear, subsequent ",
                    "encounter",
                ),
            },
        ],
    },
    {
        "id": 2,
        "passed": True,
        "updated": datetime.datetime.now(),
        "title": "Atragon (Kaitei Gunkan)",
        "description": (
            "Morbi eget diam porta, auctor est a, hendrerit lorem. Nulla sit ",
            "amet tincidunt lacus, id varius tellus.",
        ),
        "owner_name": "Godard McOnie",
        "owner_email": "gmconie1@gizmodo.com",
    },
    {
        "id": 3,
        "passed": True,
        "updated": datetime.datetime.now(),
        "title": "Sweet Mud (Adama Meshuga'at)",
        "description": (
            "Nunc augue nulla, imperdiet eu ornare a, dignissim convallis ",
            "ipsum. Praesent tellus ipsum, malesuada at neque id, scelerisque consequat ",
            "magna.",
        ),
        "owner_name": "Camila Dickinson",
        "owner_email": "cdickinson2@1688.com",
    },
    {
        "id": 4,
        "passed": False,
        "updated": datetime.datetime.now(),
        "title": "Say It Isn't So",
        "description": "Nam hendrerit mauris est, laoreet pulvinar elit laoreet vel.",
        "owner_name": "Ian Iskower",
        "owner_email": "iiskower3@yahoo.com",
        "errors": [
            {
                "id": 4,
                "title": "Bacitracin Zinc and Polymyxin B Sulfate",
                "description": "Displaced transverse fracture of left patella",
            }
        ],
    },
    {
        "id": 5,
        "passed": True,
        "updated": datetime.datetime.now(),
        "title": "Soldier of Orange (a.k.a. Survival Run) (Soldaat van Oranje)",
        "description": (
            "Ut semper dolor sit amet diam ultrices, nec porttitor erat ",
            "viverra. Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        ),
        "owner_name": "Brad Edgeson",
        "owner_email": "bedgeson4@wikipedia.org",
    },
]
