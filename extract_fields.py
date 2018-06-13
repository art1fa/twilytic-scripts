import json

def extract_fields(user):
  obj = user._json

  userdata = {
      "id_str": obj["id_str"],
      "screen_name": obj["screen_name"],
      "name": obj["name"],
      "protected": obj["protected"],
      "verified": obj["verified"],
      "default_profile_image": obj["default_profile_image"],
      "profile_image_url_https": obj["profile_image_url_https"],
      "geo_enabled": obj["geo_enabled"],
      "description": obj["description"],
      "url": obj["url"],
      "entities": obj["entities"],
      "location": obj["location"],
      "lang": obj["lang"],
      "time_zone": obj["time_zone"],
      "utc_offset": obj["utc_offset"],
      "created_at": obj["created_at"],
      "statuses_count": obj["statuses_count"],
      "followers_count": obj["followers_count"],
      "friends_count": obj["friends_count"],
      "favourites_count": obj["favourites_count"],
      "listed_count": obj["listed_count"],
      "list_tags": [],
  }
  return userdata