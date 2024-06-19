# for key, items in data.items():
#     for item in items:
#         if isinstance(item, dict):
#             id_value = str(item.get('id', ''))
#             if id_value.isdigit() and len(id_value) == 14:
#                 # Check other search criteria
#                 if id_value.lower() == search_term or \
#                         item.get('username', '').lower() == search_term or \
#                         item.get('name', '').lower() == search_term:
#                     results[key].append(item)
#             else:
#                 # Append error message if 'id' is not exactly 14 digits
#                 item['error'] = 'ID must be 14 digits'
#
# return results
