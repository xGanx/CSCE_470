import requests

# Your Spotify API request
response = requests.get('YOUR_SPOTIFY_API_ENDPOINT')

# Check the rate limit information in the response headers
remaining_requests = response.headers.get('X-RateLimit-Remaining')
reset_time = response.headers.get('X-RateLimit-Reset')

print(f"Remaining requests: {remaining_requests}")
print(f"Reset time: {reset_time}")