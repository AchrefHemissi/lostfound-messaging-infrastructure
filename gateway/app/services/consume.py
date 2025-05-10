# 4. Consumer service
async def process_rabbitmq_message(message):
    # 5. Decode base64
    image_bytes = base64.b64decode(message["image_data"])
    
    # 6. Create multipart form data
    files = {
        'file': ('image.jpg', image_bytes, 'image/jpeg')
    }
    data = {
        'user_id': message['user_id'],
        'post_id': message['post_id'],
        'post_type': message['post_type'],
        'description': message['description'],
        'item_category': message['item_category']
    }
    
    # 7. Send HTTP request to storage proxy
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'http://storage-proxy/upload/',
            data=data,
            files=files,
            headers={'x-api-key': 'your-api-key'}
        ) as response:
            return await response.json()