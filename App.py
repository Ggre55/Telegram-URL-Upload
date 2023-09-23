from flask import Flask, send_from_directory, request, jsonify, make_response
import os
import requests
from werkzeug.utils import secure_filename
from werkzeug.http import parse_options_header

app = Flask(__name__)

# Define the folder where downloaded files will be stored
DOWNLOAD_FOLDER = 'static'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER


# Function to check if the uploaded file is allowed (you can customize this)
def allowed_file(filename):
  allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
  return '.' in filename and filename.rsplit(
    '.', 1)[1].lower() in allowed_extensions


# Function to extract the clean filename from the content disposition header
def get_cleaned_filename(content_disposition):
  _, params = parse_options_header(content_disposition)
  return params.get('filename', '')


# Route for downloading files from a Google Drive link
@app.route('/download-link', methods=['POST'])
def download_file_from_link():
  try:
    # Extract the file ID from the shared link
    shared_link = request.json.get('google_drive_link')
    file_id = shared_link.split('/')[-2]
    # Construct the direct download link
    direct_download_link = f"https://drive.google.com/uc?id={file_id}&export=download"

    if not shared_link:
      return jsonify({'error': 'No link provided'})

    response = requests.get(direct_download_link)
    if response.status_code == 200:
      content_disposition = response.headers.get('content-disposition')
      if content_disposition:
        # Extract the filename from the content disposition header
        filename = get_cleaned_filename(content_disposition)

        # Remove unwanted characters and spaces from the filename
        cleaned_filename = secure_filename(filename)

        # Generate a unique filename using a timestamp (you can use a random string if preferred)
        import time
        timestamp = str(int(
          time.time()))  # Use a timestamp as part of the filename

        # Append the correct file extension to the unique filename
        file_extension = cleaned_filename.split('.')[-1]
        unique_filename = f"{cleaned_filename}"

        # Download the file
        file_path = os.path.join(app.config['DOWNLOAD_FOLDER'],
                                 unique_filename)
        with open(file_path, 'wb') as file:
          file.write(response.content)

        # Create the URL for the downloaded file
        file_url = f"https://gggghf.ggre55.repl.co/static/{unique_filename}"

        return jsonify({
          'message': 'File downloaded successfully',
          'file_path': file_path,
          'original_file_name': cleaned_filename,
          'file_name': unique_filename,
          'file_url': file_url
        })

    return jsonify(
      {'error': 'Failed to fetch the file from the provided link'})
  except Exception as e:
    return jsonify({'error': str(e)})


# Route for downloading files from a Google Drive link
@app.route('/download-link2', methods=['POST'])
def download_file_from_link2():
  try:
    # Extract the file ID from the shared link
    shared_link = request.json.get('google_drive_link')
    file_id = shared_link.split('/')[-2]
    # Construct the direct download link
    direct_download_link = f"https://drive.google.com/uc?id={file_id}&confirm=t&export=download"

    if not shared_link:
      return jsonify({'error': 'No link provided'})

    response = requests.get(direct_download_link)
    if response.status_code == 200:
      content_disposition = response.headers.get('content-disposition')
      if content_disposition:
        # Extract the filename from the content disposition header
        filename = content_disposition.split('filename=')[1]
        filename = filename.strip('"')

        # Remove unwanted characters and spaces from the filename
        cleaned_filename = secure_filename(filename)

        # Generate a unique filename using a timestamp (you can use a random string if preferred)
        import time
        timestamp = str(int(
          time.time()))  # Use a timestamp as part of the filename

        # Append the correct file extension to the unique filename
        file_extension = cleaned_filename.split('.')[-1]
        unique_filename = f"{timestamp}.{file_extension}"

        # Download the file
        file_path = os.path.join(app.config['DOWNLOAD_FOLDER'],
                                 unique_filename)
        with open(file_path, 'wb') as file:
          file.write(response.content)

        # Create the URL for the downloaded file
        file_url = f"https://gggghf.ggre55.repl.co/static/{unique_filename}"

        return jsonify({
          'message': 'File downloaded successfully',
          'file_path': file_path,
          'file_url': file_url
        })

    return jsonify(
      {'error': 'Failed to fetch the file from the provided link'})
  except Exception as e:
    return jsonify({'error': str(e)})


# Route to access the downloaded files
@app.route('/static/<path:filename>')
def download_files(filename):
  # Create a response that sets the Content-Disposition header to force download
  response = make_response(
    send_from_directory(app.config['DOWNLOAD_FOLDER'], filename))
  return response


if __name__ == '__main__':
  # Create the DOWNLOAD_FOLDER if it doesn't exist
  os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)
  app.run(debug=True, host='0.0.0.0', port=8080)
