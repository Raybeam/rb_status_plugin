import pprint
import test_data

pp = pprint.PrettyPrinter(indent=2)


def get_test_data():
    data = {
        "summary": {"passed": False, "updated": test_data.dummy_reports[0]["updated"]},
        "reports": test_data.dummy_reports,
    }
    pp.pprint(data)
    return test_data.dummy_reports


get_test_data()
