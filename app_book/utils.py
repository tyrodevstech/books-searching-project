from geopy.distance import geodesic
from operator import itemgetter


# def getSortedBooksLocations(userLocation, book_qs):
#     start_time = time.time()
#     book_locs = []
#     for book in book_qs:
#         if book.store.location and userLocation:
#             distance = geodesic(userLocation, book.store.location.split(",")).kilometers
#             book_locs.append(
#                 {
#                     "id": book.id,
#                     "title": book.title,
#                     "author": book.author.author_name,
#                     "distance": round(distance,2),
#                 }
#             )
#     result = sorted(book_locs, key=itemgetter('id')) or None
#     end_time = time.time()
#     print(f"Time taken: {end_time - start_time:.6f} seconds")
#     return result


# def getSortedBooksLocations(userLocation, book_qs):
#     book_locs = []
#     for book in book_qs:
#         if book.store.location and userLocation:
#             distance = geodesic(userLocation, book.store.location.split(",")).ki
#             book_locs.append(
#                 {
#                     "id": book.id,
#                     "title": book.title,
#                     "author": book.author.author_name,
#                     "distance": round(distance,2),
#                 }
#             )
#     result = sorted(book_locs, key=itemgetter('id')) or None
#     return result


def getSortedBooksLocations(user_location, book_qs):
    book_locs = []
    user_location_coords = tuple(map(float, user_location.split(",")))
    for book in book_qs:
        store_location = book.store.location if book.store else None
        if store_location and user_location:
            store_location_coords = tuple(map(float, store_location.split(",")))
            distance = round(
                geodesic(user_location_coords, store_location_coords).kilometers, 2
            )
            book_locs.append(
                {
                    "id": book.id,
                    "title": book.title,
                    "author": book.author.author_name,
                    "category": book.category.category_name,
                    "store_id": book.store.id,
                    "store_name": book.store.name,
                    "store_phone": book.store.phone,
                    "store_street": book.store.street,
                    "store_city": book.store.city,
                    "store_location": book.store.location,
                    "distance": distance,
                }
            )
    return sorted(book_locs, key=itemgetter("distance")) or None
