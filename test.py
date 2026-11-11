# def create_all_house(house_id: int, house_data: dict):
#     parent_count = [1]
#
#     final_dict = {}
#     final_key = "house"
#
#     for (
#         key,
#         value,
#     ) in (
#         house_data.items()
#     ):  # Тут просто біжимо по house_data і дивимось що в ньому там записано і беремо це
#         children = []
#         amount_number = 0
#         real_number = 1
#         to_result = []
#         for parent_id in parent_count:  # Тут бігаємо по кожному батькові
#             for _ in range(value):  # А тут бігаємо по дітях
#                 to_result.append([key, parent_id, amount_number + 1, real_number])
#                 children.append(amount_number + 1)
#                 amount_number += 1
#                 real_number += 1
#             if key != "apartment":
#                 real_number = 1
#             parent_count = children  # Тепер дітки виросли і стають батьками
#         final_key = key
#         final_dict[final_key] = to_result
#
#     # print(final_dict)
#
#     return final_dict
#

# dict = {'name': '', parent_id: ''}
# def fake_db(item_data: dict):
#     print(f"Name == {item_data['name']}")
#     new_id = int(item_data['parent_id']) * random.randint(1, 15)
#     print(f"New Id == {new_id} | Parent Id == {item_data['parent_id']}")
#     return new_id


# def insert_real_id(
#     house_id: int,
#     house_data: dict,
# ):
#     new_ids_list = {1: house_id}  # сюда треба зберігати temp_id - real_id
#     for key, value in house_data.items():
#         child_ids_list = {}
#         list_to_db = []
#         temp_ids = []
#         for item in value:
#             item[1] = new_ids_list[item[1]]
#
#             final_dict = {"parent_id": item[1], "name": f"{item[3]} - {item[0]}"}
#
#             list_to_db.append(final_dict)
#
#             temp_ids.append(item[2])
#
#         new_ids = reak_db(list_to_db)
#
#         for key1, key2 in zip(temp_ids, new_ids, strict=False):
#             child_ids_list[key1] = key2
#
#         if len(new_ids) == len(child_ids_list):
#             new_ids_list = child_ids_list
#         else:
#             print(f"{len(new_ids)} -- {len(child_ids_list)}")
#             break
#
#
# items = create_all_house(
#     house_id=1488, house_data={"corps": 2, "section": 3, "storey": 5, "apartment": 3}
# )
#
# insert_real_id(house_id=15, house_data=items)
