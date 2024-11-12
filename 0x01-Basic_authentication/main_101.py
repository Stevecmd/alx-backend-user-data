#!/usr/bin/env python3
""" Main Auth
    13. Require auth with stars
"""
from api.v1.auth.auth import Auth

a = Auth()

print(a.require_auth("/api/v1/users", ["/api/v1/stat*"]))  # True
print(a.require_auth("/api/v1/status", ["/api/v1/stat*"]))  # False
print(a.require_auth("/api/v1/stats", ["/api/v1/stat*"]))  # False
print(a.require_auth("/api/v1/status/", ["/api/v1/stat*"]))  # False
print(a.require_auth("/api/v1/stats/", ["/api/v1/stat*"]))  # False
print(a.require_auth("/api/v1/statistics", ["/api/v1/stat*"]))  # False
print(a.require_auth("/api/v1/statistics/", ["/api/v1/stat*"]))  # False
print(a.require_auth("/api/v1/statistics/data", ["/api/v1/stat*"]))  # False
print(a.require_auth("/api/v1/statistics/data/", ["/api/v1/stat*"]))  # False
print(a.require_auth("/api/v1/statistics/data/1", ["/api/v1/stat*"]))  # False
print(a.require_auth("/api/v1/statistics/data/1/", ["/api/v1/stat*"]))  # False
