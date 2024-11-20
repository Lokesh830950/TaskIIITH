import base64
import os

def decode_base64_images(data, output_folder):
    image_filenames = []

    for idx, row in data.iterrows():
        for col, value in row.items():
            if isinstance(value, str) and value.startswith('data:image'):
                try:
                    header, encoded = value.split(',', 1)
                    extension = header.split('/')[1].split(';')[0]
                    image_filename = f'image_{idx}_{col}.{extension}'
                    image_path = os.path.join(output_folder, image_filename)
                    
                    with open(image_path, 'wb') as img_file:
                        img_file.write(base64.b64decode(encoded))
                    image_filenames.append(image_filename)
                except Exception as e:
                    print(f"Error decoding image: {e}")
    
    return image_filenames
