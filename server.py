import socket, json

HOST = "0.0.0.0"
PORT = 5000

UNITS = {
    "CSC101": "Introduction to Programming",
    "CSC202": "Distributed Systems",
    "CSC203": "Database Systems",
    "CSC204": "Computer Networks",
}

def average_of(marks):
    if not isinstance(marks, list) or len(marks) == 0:
        raise ValueError("marks must be a non-empty list")
    for m in marks:
        if not 0 <= m <= 100:
            raise ValueError(f"Invalid mark {m}: must be between 0 and 100")
    return sum(marks) / len(marks)

def calculate_grade(req):
    marks = req["marks"]
    average = average_of(marks)
    if   average >= 70: grade = "A"
    elif average >= 60: grade = "B"
    elif average >= 50: grade = "C"
    elif average >= 40: grade = "D"
    else:               grade = "F"
    return {"student": req["student"], "total": sum(marks),
            "average": average, "grade": grade}

def calculate_pass_status(req):
    average = average_of(req["marks"])
    return {"student": req["student"], "average": average,
            "pass_status": "PASS" if average >= 40 else "FAIL"}

def get_unit_name(req):
    code = req["code"].strip().upper()
    if code not in UNITS:
        raise ValueError(f"Unknown unit code: {code}")
    return {"code": code, "unit_name": UNITS[code]}

METHODS = {
    "calculate_grade": calculate_grade,
    "calculate_pass_status": calculate_pass_status,
    "get_unit_name": get_unit_name,
}

def handle_request(raw):
    try:
        req = json.loads(raw)
        method = req["method"]
        if method not in METHODS:
            raise ValueError(f"Unknown method: {method}")
        return {"status": "success", **METHODS[method](req)}
    except KeyError as e:
        return {"status": "error", "message": f"Missing field: {e}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"Grade Calculation Server running on port {PORT}")
        print("Waiting for clients...")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"\nClient connected: {addr}")
                raw = conn.recv(4096).decode()
                print("Request:", raw)
                conn.sendall(json.dumps(handle_request(raw)).encode())
                print("Request completed.")

server()
