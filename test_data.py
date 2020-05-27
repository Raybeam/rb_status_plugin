import datetime

dummy_tests = [
    {"id": "example_dag.python_random_0", "name": "example_dag.python_random_0"},
    {
        "id": "example_dag.python_print_date_0",
        "name": "example_dag.python_print_date_0",
    },
    {"id": "example_dag.python_failing_1", "name": "example_dag.python_failing_1"},
    {
        "id": "example_dag.python_print_date_1",
        "name": "example_dag.python_print_date_1",
    },
    {"id": "example_dag.python_random_1", "name": "example_dag.python_random_1"},
]

dummy_reports = [
    {
        "id": 1,
        "passed": False,
        "updated": datetime.datetime.now(),
        "report_title": "Diary of a Madman",
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
        "report_title": "Atragon (Kaitei Gunkan)",
        "description": (
            "Morbi eget diam porta, auctor est a, hendrerit lorem. Nulla sit ",
            "amet tincidunt lacus, id varius tellus.",
        ),
        "owner_name": "Godard McOnie",
        "owner_email": "gmconie1@gizmodo.com",
    },
    {
        "id": 3,
        "passed": None,
        "updated": datetime.datetime.now(),
        "report_title": "Sweet Mud (Adama Meshuga'at)",
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
        "report_title": "Say It Isn't So",
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
        "report_title": "Soldier of Orange (a.k.a. Survival Run) (Soldaat van Oranje)",
        "description": (
            "Ut semper dolor sit amet diam ultrices, nec porttitor erat ",
            "viverra. Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        ),
        "owner_name": "Brad Edgeson",
        "owner_email": "bedgeson4@wikipedia.org",
    },
]
