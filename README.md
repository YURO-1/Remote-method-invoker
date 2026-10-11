#Remote Method Invoker
A client-server application in Python that demonstrates Remote Method Invocation. The client sends a student's marks to a server, and the server performs the calculation and returns the result. The client contains no grading logic.

How it works

The client builds a JSON request containing a method name and its arguments and sends it over TCP (port 5000). The server looks the method up in a dispatch table, runs it, and returns a JSON response.
