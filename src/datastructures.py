class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 4
        self._members = [
            {
                "id": 1,
                "first_name": "John",
                "last_name": last_name,
                "age": 33,
                "lucky_numbers": [7, 13, 22]
            },
            {
                "id": 2,
                "first_name": "Jane",
                "last_name": last_name,
                "age": 35,
                "lucky_numbers": [10, 14, 3]
            },
            {
                "id": 3,
                "first_name": "Jimmy",
                "last_name": last_name,
                "age": 5,
                "lucky_numbers": [1]
            }
        ]

    def _generate_id(self):
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    def add_member(self, member):
        if "id" not in member:
            member["id"] = self._generate_id()
        member["last_name"] = self.last_name
        self._members.append(member)
        return member

    def delete_member(self, member_id):
        for i, member in enumerate(self._members):
            if member["id"] == member_id:
                self._members.pop(i)
                return True
        return False

    def get_member(self, member_id):
        for member in self._members:
            if member["id"] == member_id:
                return {
                    "id": member["id"],
                    "first_name": member["first_name"],
                    "age": member["age"],
                    "lucky_numbers": member["lucky_numbers"]
                }
        return None

    def get_all_members(self):
        return self._members