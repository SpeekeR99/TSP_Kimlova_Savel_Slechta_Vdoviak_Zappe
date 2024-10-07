import subprocess

def create_merge_request():
    try:
        command = [
            'git', 'push', 'origin', 'HEAD', '-u',
            '--push-option=merge_request.create',
        ]
        
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(result.stdout.decode('utf-8'))
    
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr.decode('utf-8')}")

if __name__ == "__main__":
    create_merge_request()
