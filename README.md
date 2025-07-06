# alx-backend-python

python-generators-0x00/
│
├── 0-stream_users.py           # Streams user rows one by one using a generator
├── 1-batch_processing.py       # Processes user data in batches (e.g., filters age > 25)
├── 2-main.py                   # Main runner script to test batch processing
├── user_data.py                # (Optional) Sample mock user dataset
├── README.md                   # Project description and instructions

# Run the streaming generator
python3 1-main.py

# Run batch processing
python3 2-main.py | head -n 5
