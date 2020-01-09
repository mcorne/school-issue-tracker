from enum import Enum


class Role(Enum):
    admin = "Administrator"
    teacher = 2
    it_technician = 3
    it_manager = 4
    service_agent = 5
    service_manager = 6

    @staticmethod
    def get_choices():
        choices = [("--", "")] + [(name, member.value) for name, member in Role.__members__.items()]
        return choices


# print(Role.admin.name)
# print(Role.admin.value)
# # print(Role.admin)
# # print(list(Role))
# # print(list(Role.__members__.items()))
# print([(name, member.value) for name, member in Role.__members__.items()])
# print(Role.__members__)
print(Role.get_choices())
