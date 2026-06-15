#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import run

import database
import routes

server_port = 3000 # Порт, на котором будет работать сервер

# Server startup
if __name__ == '__main__':
    print("=" * 60)
    print("EXPRESS TEST SERVER")
    print("=" * 60)
    print("Server started on http://localhost:%d" %(server_port))
    print("\nMain Pages:")
    print("  • Main page:     http://localhost:%d" %(server_port))
    print("  • Login:         Click 'Login' button")
    print("  • Registration:  Click 'Registration' button")
    print("  • My results:    http://localhost:%d/my_results" %(server_port))
    print("  • Admin panel:   http://localhost:%d/admin" %(server_port))
    print("\nFrom main page you can:")
    print("  • Create survey")
    print("  • Take surveys")
    print("=" * 60)
    
    # Show initial database stats
    stats = database.db.get_database_stats()
    print(f"\nInitial Database Stats:")
    print(f"  Users: {stats.get('Users', 0)}")
    print(f"  Tasks: {stats.get('Tasks', 0)}")
    print(f"  Answers: {stats.get('Answers', 0)}")
    print("=" * 60)
    
    run(host='localhost', port=server_port, debug=True)
