import socket, json

SERVER_HOST = "127.0.0.1"   # change to Computer A's IP for the two-computer test
SERVER_PORT = 5000

def invoke_remote_method(method, **params):
    request = {"method": method, **params}
    try:
        with socket.create_connection((SERVER_HOST, SERVER_PORT), timeout=5) as s:
            s.sendall(json.dumps(request).encode())
            return json.loads(s.recv(4096).decode())
    except ConnectionRefusedError:
        return {"status": "error", "message": "Connection refused - is the server running?"}
    except TimeoutError:
        return {"status": "error", "message": "Timed out - wrong IP or firewall blocking?"}
    except OSError as e:
        return {"status": "error", "message": f"Network error: {e}"}

def read_marks():
    n = int(input("Enter number of units: "))
    return [float(input(f"Enter mark for unit {i+1}: ")) for i in range(n)]

print("REMOTE STUDENT GRADE CALCULATOR")
print("1) Grade   2) Pass/Fail   3) Unit lookup")
choice = input("Choose: ")

try:
    if choice == "1":
        r = invoke_remote_method("calculate_grade", student=input("Student name: "), marks=read_marks())
    elif choice == "2":
        r = invoke_remote_method("calculate_pass_status", student=input("Student name: "), marks=read_marks())
    elif choice == "3":
        r = invoke_remote_method("get_unit_name", code=input("Unit code: "))
    else:
        r = {"status": "error", "message": "Invalid choice"}
except ValueError:
    r = {"status": "error", "message": "Please enter numbers where numbers are expected"}

if r["status"] == "success":
    print("\n===== RESULT =====")
    for k, v in r.items():
        if k != "status":
            print(f"{k}: {v}")
else:
    print("Error:", r["message"])
