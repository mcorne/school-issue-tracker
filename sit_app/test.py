from enum import Enum
from flask_babel import lazy_gettext


class Role(Enum):
    admin = lazy_gettext("Administrator")
    teacher = lazy_gettext("Teacher")
    it_technician = lazy_gettext("IT Technician")
    it_manager = lazy_gettext("IT Manager")
    service_agent = lazy_gettext("Service Agent")
    service_manager = lazy_gettext("Service Manager")

    @staticmethod
    def get_choices():
        choices = [("", "-- Choose a role --")] + [
            (name, member.value) for name, member in Role.__members__.items()
        ]
        return choices

    @classmethod
    def coerce(cls, item):
        return Role[item]


# print(Role.admin.name)
# print(Role.admin.value)
# # print(Role.admin)
# # print(list(Role))
# # print(list(Role.__members__.items()))
# print([(name, member.value) for name, member in Role.__members__.items()])
# print(Role.__members__)
# print(Role.get_choices())

# for item in Role.__members__.items():
#     print(item[0], item[1])

# for value in Role.__members__.values():
#     print(value, value.value)


# for key, value in Role.__members__.items():
#     print(key, value, value.name, value.value)
print(Role.coerce("admin"))
